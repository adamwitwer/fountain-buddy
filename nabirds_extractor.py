#!/usr/bin/env python3
"""
NABirds Data Extractor for Fountain Buddy
Extracts images for specific backyard bird species from the NABirds dataset
"""

import os
import shutil
import sqlite3
from collections import defaultdict, Counter
import json
import random
from pathlib import Path

class NABirdsExtractor:
    def __init__(self, nabirds_path='nabirds', output_dir='nabirds_training_data'):
        self.nabirds_path = nabirds_path
        self.output_dir = output_dir
        self.db_path = 'fountain_buddy.db'
        
        # Target backyard species with their priorities (higher = more needed)
        self.target_species = {
            'Blue Jay': {'priority': 10, 'current_samples': 8, 'target_samples': 80},
            'Gray Catbird': {'priority': 9, 'current_samples': 30, 'target_samples': 80},
            'Common Grackle': {'priority': 8, 'current_samples': 33, 'target_samples': 80},
            'American Robin': {'priority': 3, 'current_samples': 90, 'target_samples': 120},
            'Northern Cardinal': {'priority': 4, 'current_samples': 81, 'target_samples': 100},
            'House Sparrow': {'priority': 6, 'current_samples': 60, 'target_samples': 80},
            'Mourning Dove': {'priority': 5, 'current_samples': 59, 'target_samples': 80},
            'European Starling': {'priority': 2, 'current_samples': 94, 'target_samples': 100}
        }
        
        # NABirds class mappings (from our earlier analysis)
        self.nabirds_class_map = {
            'Blue Jay': [286, 950],  # Blue Jay and Blue Jay (alternative)
            'American Robin': [718, 753, 960],  # American Robin variants
            'European Starling': [439, 748, 856, 1005],  # European Starling variants
            'Northern Cardinal': [310, 772, 979],  # Northern Cardinal variants
            'House Sparrow': [445, 796, 1003],  # House Sparrow variants
            'Common Grackle': [429, 912],  # Common Grackle variants
            'Gray Catbird': [275, 851],  # Gray Catbird variants
            'Mourning Dove': [171, 529]  # Mourning Dove variants
        }
        
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_nabirds_metadata(self):
        """Load NABirds metadata files"""
        print("Loading NABirds metadata...")
        
        # Load class names
        classes = {}
        with open(os.path.join(self.nabirds_path, 'classes.txt'), 'r') as f:
            for line in f:
                class_id, class_name = line.strip().split(' ', 1)
                classes[int(class_id)] = class_name
        
        # Load image class labels
        image_labels = {}
        with open(os.path.join(self.nabirds_path, 'image_class_labels.txt'), 'r') as f:
            for line in f:
                image_id, class_id = line.strip().split()
                image_labels[image_id] = int(class_id)
        
        # Load train/test split
        train_test_split = {}
        with open(os.path.join(self.nabirds_path, 'train_test_split.txt'), 'r') as f:
            for line in f:
                image_id, is_train = line.strip().split()
                train_test_split[image_id] = int(is_train) == 1
        
        # Load image file paths
        image_paths = {}
        with open(os.path.join(self.nabirds_path, 'images.txt'), 'r') as f:
            for line in f:
                image_id, image_path = line.strip().split(' ', 1)
                image_paths[image_id] = image_path
        
        return classes, image_labels, train_test_split, image_paths
    
    def find_target_images(self):
        """Find images for target species in NABirds dataset"""
        classes, image_labels, train_test_split, image_paths = self.load_nabirds_metadata()
        
        target_images = defaultdict(list)
        
        # Find images for each target species
        for species, class_ids in self.nabirds_class_map.items():
            print(f"\nSearching for {species} (classes: {class_ids})...")
            
            for image_id, class_id in image_labels.items():
                if class_id in class_ids and image_id in image_paths:
                    image_path = os.path.join(self.nabirds_path, 'images', 
                                            image_paths[image_id])
                    
                    if os.path.exists(image_path):
                        is_train = train_test_split.get(image_id, False)
                        target_images[species].append({
                            'image_id': image_id,
                            'path': image_path,
                            'class_id': class_id,
                            'class_name': classes[class_id],
                            'is_train': is_train
                        })
            
            print(f"Found {len(target_images[species])} images for {species}")
        
        return target_images
    
    def extract_balanced_samples(self, target_images):
        """Extract a balanced set of samples based on priority and need"""
        extracted_stats = {}
        
        for species, info in self.target_species.items():
            if species not in target_images:
                print(f"Warning: No images found for {species}")
                continue
            
            available_images = target_images[species]
            current_samples = info['current_samples']
            target_samples = info['target_samples']
            needed_samples = max(0, target_samples - current_samples)
            
            # Prioritize training images, but use test images if needed
            train_images = [img for img in available_images if img['is_train']]
            test_images = [img for img in available_images if not img['is_train']]
            
            # Select images to extract
            selected_images = []
            if len(train_images) >= needed_samples:
                selected_images = random.sample(train_images, needed_samples)
            else:
                # Use all training images + some test images
                selected_images = train_images.copy()
                remaining_needed = needed_samples - len(train_images)
                if remaining_needed > 0 and test_images:
                    additional = random.sample(test_images, 
                                             min(remaining_needed, len(test_images)))
                    selected_images.extend(additional)
            
            # Create species directory
            species_dir = os.path.join(self.output_dir, species.replace(' ', '_'))
            os.makedirs(species_dir, exist_ok=True)
            
            # Copy selected images
            copied_count = 0
            for i, img_info in enumerate(selected_images):
                src_path = img_info['path']
                if os.path.exists(src_path):
                    # Create descriptive filename
                    ext = os.path.splitext(src_path)[1]
                    dst_filename = f"nabirds_{img_info['image_id']}{ext}"
                    dst_path = os.path.join(species_dir, dst_filename)
                    
                    try:
                        shutil.copy2(src_path, dst_path)
                        copied_count += 1
                    except Exception as e:
                        print(f"Error copying {src_path}: {e}")
            
            extracted_stats[species] = {
                'available': len(available_images),
                'needed': needed_samples,
                'extracted': copied_count,
                'new_total': current_samples + copied_count
            }
            
            print(f"\n{species}:")
            print(f"  Available in NABirds: {len(available_images)}")
            print(f"  Currently have: {current_samples}")
            print(f"  Target: {target_samples}")
            print(f"  Extracted: {copied_count}")
            print(f"  New total: {current_samples + copied_count}")
        
        return extracted_stats
    
    def create_extraction_report(self, stats):
        """Create a detailed extraction report"""
        report = {
            'extraction_date': str(Path(__file__).stat().st_mtime),
            'nabirds_path': self.nabirds_path,
            'output_directory': self.output_dir,
            'species_stats': stats,
            'total_extracted': sum(s['extracted'] for s in stats.values()),
            'total_new_samples': sum(s['new_total'] for s in stats.values())
        }
        
        # Save report
        report_path = os.path.join(self.output_dir, 'extraction_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n" + "="*60)
        print("NABIRDS EXTRACTION SUMMARY")
        print("="*60)
        print(f"Total images extracted: {report['total_extracted']}")
        print(f"Total training samples now: {report['total_new_samples']}")
        print(f"Report saved to: {report_path}")
        
        # Show before/after comparison
        print(f"\nBEFORE vs AFTER:")
        for species, stat in stats.items():
            before = stat['new_total'] - stat['extracted']
            after = stat['new_total']
            improvement = f"+{stat['extracted']}" if stat['extracted'] > 0 else "0"
            print(f"  {species:20} {before:3d} → {after:3d} ({improvement})")
        
        return report

def main():
    """Main extraction process"""
    print("NABirds Training Data Extractor")
    print("="*50)
    
    # Check if nabirds directory exists
    if not os.path.exists('nabirds'):
        print("Error: nabirds directory not found!")
        print("Please ensure the NABirds dataset is available in the 'nabirds' directory.")
        return
    
    extractor = NABirdsExtractor()
    
    # Set random seed for reproducibility
    random.seed(42)
    
    try:
        # Find target images
        target_images = extractor.find_target_images()
        
        if not any(target_images.values()):
            print("No target images found! Check NABirds dataset structure.")
            return
        
        # Extract balanced samples
        stats = extractor.extract_balanced_samples(target_images)
        
        # Create report
        report = extractor.create_extraction_report(stats)
        
        print("\nExtraction completed successfully!")
        print(f"Next steps:")
        print(f"1. Review extracted images in: {extractor.output_dir}")
        print(f"2. Run the enhanced training script")
        print(f"3. Monitor training performance improvements")
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()