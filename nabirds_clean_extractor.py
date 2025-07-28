#!/usr/bin/env python3
"""
Clean NABirds Training Data Extractor
Creates balanced, professional training dataset from NABirds for Fountain Buddy species
"""

import os
import shutil
import json
from pathlib import Path
from collections import defaultdict

# Target species mapping: species_name -> list of NABirds class IDs
SPECIES_MAPPING = {
    "American_Robin": [718, 753, 960],  # Regular, Adult, Juvenile
    "Black-capped_Chickadee": [278, 812],  # Regular, Adult
    "Blue_Jay": [286, 950],  # Regular, Adult
    "Common_Grackle": [429, 912],  # Regular, Adult
    "Downy_Woodpecker": [188, 559],  # Regular, Adult
    "European_Starling": [439, 748, 856, 1005],  # Regular, Breeding, Nonbreeding, Juvenile
    "Gray_Catbird": [275, 851],  # Regular, Adult
    "House_Finch": [419, 790, 997],  # Regular, Adult Male, Female/Immature
    "House_Sparrow": [445, 796, 1003],  # Regular, Male, Female/Juvenile
    "Mourning_Dove": [171, 529],  # Regular, Adult
    "Northern_Cardinal": [310, 772, 979],  # Regular, Adult Male, Female/Juvenile
    "Red-bellied_Woodpecker": [95, 553],  # Regular, Adult
    "Red-winged_Blackbird": [268, 780, 987],  # Regular, Male, Female/Juvenile
    "Song_Sparrow": [686, 902],  # Regular, Adult
    "Tufted_Titmouse": [717, 819],  # Regular, Adult
    "White-breasted_Nuthatch": [413, 824]  # Regular, Adult
}

# Configuration
NABIRDS_DIR = "nabirds"
OUTPUT_DIR = "nabirds_clean_training"
MAX_IMAGES_PER_SPECIES = 100  # Balanced dataset
MIN_IMAGES_PER_SPECIES = 20   # Minimum threshold

class NABirdsCleanExtractor:
    def __init__(self):
        self.nabirds_path = Path(NABIRDS_DIR)
        self.output_path = Path(OUTPUT_DIR)
        self.image_labels = {}
        self.class_names = {}
        
    def load_metadata(self):
        """Load NABirds metadata files"""
        print("📖 Loading NABirds metadata...")
        
        # Load image class labels
        with open(self.nabirds_path / "image_class_labels.txt", 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    image_id = parts[0]
                    class_id = int(parts[1])
                    self.image_labels[image_id] = class_id
        
        print(f"✅ Loaded {len(self.image_labels)} image labels")
        
    def create_clean_dataset(self):
        """Create clean, balanced training dataset"""
        print("🧹 Creating clean NABirds training dataset...")
        
        # Remove existing output directory
        if self.output_path.exists():
            shutil.rmtree(self.output_path)
        self.output_path.mkdir(parents=True)
        
        extraction_stats = {}
        
        for species_name, class_ids in SPECIES_MAPPING.items():
            print(f"\n🐦 Processing {species_name.replace('_', ' ')}...")
            
            # Create species output directory
            species_dir = self.output_path / species_name
            species_dir.mkdir(exist_ok=True)
            
            # Collect all images for this species across all class variants
            species_images = []
            
            for class_id in class_ids:
                # Find all images for this class ID
                class_images = []
                for image_id, img_class_id in self.image_labels.items():
                    if img_class_id == class_id:
                        class_images.append(image_id)
                
                print(f"  📊 Class {class_id}: {len(class_images)} images")
                species_images.extend(class_images)
            
            print(f"  📈 Total available: {len(species_images)} images")
            
            # Balance dataset - limit to MAX_IMAGES_PER_SPECIES
            if len(species_images) > MAX_IMAGES_PER_SPECIES:
                # Randomly sample to balance
                import random
                random.seed(42)  # Reproducible sampling
                species_images = random.sample(species_images, MAX_IMAGES_PER_SPECIES)
                print(f"  ⚖️ Balanced to: {len(species_images)} images")
            
            # Check minimum threshold
            if len(species_images) < MIN_IMAGES_PER_SPECIES:
                print(f"  ⚠️ Warning: Only {len(species_images)} images (below minimum of {MIN_IMAGES_PER_SPECIES})")
            
            # Copy images to species directory
            copied_count = 0
            for image_id in species_images:
                # Find the image file in NABirds directory structure
                source_path = self.find_image_file(image_id)
                if source_path and source_path.exists():
                    # Copy with clean naming
                    dest_filename = f"nabirds_{image_id}.jpg"
                    dest_path = species_dir / dest_filename
                    shutil.copy2(source_path, dest_path)
                    copied_count += 1
            
            extraction_stats[species_name] = copied_count
            print(f"  ✅ Extracted: {copied_count} images")
        
        # Generate extraction report
        self.generate_report(extraction_stats)
        
    def find_image_file(self, image_id):
        """Find the actual image file path for a given image ID"""
        images_dir = self.nabirds_path / "images"
        
        # Remove hyphens from UUID (labels have hyphens, files don't)
        clean_image_id = image_id.replace('-', '')
        
        # Search through all subdirectories for the UUID-named file
        for subdir in images_dir.iterdir():
            if subdir.is_dir():
                image_path = subdir / f"{clean_image_id}.jpg"
                if image_path.exists():
                    return image_path
        
        return None
    
    def generate_report(self, stats):
        """Generate extraction report"""
        print("\n📊 Clean NABirds Extraction Report")
        print("=" * 50)
        
        total_images = 0
        for species, count in stats.items():
            species_display = species.replace('_', ' ')
            print(f"{species_display:25}: {count:3d} images")
            total_images += count
        
        print("-" * 50)
        print(f"{'Total':25}: {total_images:3d} images")
        print(f"{'Species':25}: {len(stats):3d}")
        
        # Save report to JSON
        report_data = {
            'extraction_date': str(Path().cwd()),
            'total_images': total_images,
            'total_species': len(stats),
            'max_per_species': MAX_IMAGES_PER_SPECIES,
            'min_per_species': MIN_IMAGES_PER_SPECIES,
            'species_stats': stats
        }
        
        with open(self.output_path / "extraction_report.json", 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n✅ Clean dataset created in: {self.output_path}")
        print(f"📄 Report saved: {self.output_path}/extraction_report.json")
        
        # Check for any low-sample species
        low_sample_species = [s for s, c in stats.items() if c < MIN_IMAGES_PER_SPECIES]
        if low_sample_species:
            print(f"\n⚠️ Low sample species (may need supplementing):")
            for species in low_sample_species:
                print(f"   - {species.replace('_', ' ')}: {stats[species]} images")

def main():
    print("🧹 NABirds Clean Training Data Extractor")
    print("Creating professional, balanced dataset for Fountain Buddy")
    print("=" * 60)
    
    extractor = NABirdsCleanExtractor()
    extractor.load_metadata()
    extractor.create_clean_dataset()
    
    print("\n🎉 Clean extraction complete!")
    print("Ready for fresh model training with professional NABirds data")

if __name__ == "__main__":
    main()