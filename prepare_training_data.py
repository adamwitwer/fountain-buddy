#!/usr/bin/env python3
"""
Training data preparation script for 19-class unified model.
Reorganizes existing training data and prepares for new species collection.
"""

import os
import shutil
import sqlite3
from datetime import datetime
from species_mapping import (
    UNIFIED_SPECIES_LIST, OLD_TO_NEW_MAPPING, NEW_SPECIES, 
    SPECIES_LOCATIONS, generate_metadata
)

def analyze_current_training_data():
    """Analyze the existing training data structure."""
    
    print("🔍 Analyzing current training data...")
    
    training_dir = "training_data"
    if not os.path.exists(training_dir):
        print(f"❌ Training directory not found: {training_dir}")
        return {}
    
    species_counts = {}
    total_images = 0
    
    for item in os.listdir(training_dir):
        species_path = os.path.join(training_dir, item)
        if os.path.isdir(species_path):
            # Count images in this species directory
            image_files = [f for f in os.listdir(species_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            count = len(image_files)
            species_counts[item] = count
            total_images += count
            
            print(f"   📁 {item}: {count} images")
    
    print(f"📊 Total: {total_images} images across {len(species_counts)} species")
    return species_counts

def create_unified_training_structure():
    """Create the new unified training data structure."""
    
    print("🏗️ Creating unified training data structure...")
    
    # Create new training directory structure
    new_training_dir = "training_data_unified"
    os.makedirs(new_training_dir, exist_ok=True)
    
    # Create directories for all 19 species
    for species in UNIFIED_SPECIES_LIST:
        species_dir = os.path.join(new_training_dir, species.replace(" ", "_"))
        os.makedirs(species_dir, exist_ok=True)
        print(f"   📁 Created: {species_dir}")
    
    print(f"✅ Created {len(UNIFIED_SPECIES_LIST)} species directories")
    return new_training_dir

def migrate_existing_training_data(new_training_dir):
    """Migrate existing training data to the new structure."""
    
    print("🚚 Migrating existing training data...")
    
    old_training_dir = "training_data"
    migration_log = []
    
    for old_species, new_species in OLD_TO_NEW_MAPPING.items():
        if new_species is None:
            print(f"   ⚠️ Skipping {old_species} (being removed)")
            continue
        
        old_dir = os.path.join(old_training_dir, old_species.replace(" ", "_"))
        new_dir = os.path.join(new_training_dir, new_species.replace(" ", "_"))
        
        if not os.path.exists(old_dir):
            print(f"   ⚠️ Old directory not found: {old_dir}")
            continue
        
        # Get list of images to migrate
        image_files = [f for f in os.listdir(old_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not image_files:
            print(f"   ⚠️ No images found in {old_dir}")
            continue
        
        # Copy images to new directory
        copied_count = 0
        for image_file in image_files:
            old_path = os.path.join(old_dir, image_file)
            new_path = os.path.join(new_dir, image_file)
            
            try:
                shutil.copy2(old_path, new_path)
                copied_count += 1
            except Exception as e:
                print(f"   ❌ Failed to copy {image_file}: {e}")
        
        migration_log.append({
            'old_species': old_species,
            'new_species': new_species,
            'images_migrated': copied_count
        })
        
        print(f"   ✅ {old_species} → {new_species}: {copied_count} images")
    
    return migration_log

def identify_missing_species_data(new_training_dir):
    """Identify which new species need training data."""
    
    print("🔍 Identifying missing species data...")
    
    missing_species = []
    species_status = {}
    
    for species in UNIFIED_SPECIES_LIST:
        species_dir = os.path.join(new_training_dir, species.replace(" ", "_"))
        image_files = [f for f in os.listdir(species_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        count = len(image_files)
        
        species_status[species] = count
        
        if count == 0:
            missing_species.append(species)
            print(f"   ❌ {species}: No training data")
        elif count < 10:
            print(f"   ⚠️ {species}: Only {count} images (needs more)")
        else:
            print(f"   ✅ {species}: {count} images")
    
    return missing_species, species_status

def extract_training_data_from_database(new_training_dir):
    """Extract potential training data from identified bird images in database."""
    
    print("📊 Extracting training data from database...")
    
    db_name = "fountain_buddy.db"
    if not os.path.exists(db_name):
        print(f"❌ Database not found: {db_name}")
        return
    
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Get all bird visits with human-verified species
        cursor.execute("""
            SELECT species, image_path, location, confidence 
            FROM bird_visits 
            WHERE species IS NOT NULL 
            AND species != 'Unknown Bird' 
            AND confidence = 1.0
            ORDER BY species, timestamp
        """)
        
        verified_birds = cursor.fetchall()
        conn.close()
        
        print(f"📋 Found {len(verified_birds)} human-verified bird identifications")
        
        extraction_log = {}
        
        for species, image_path, location, confidence in verified_birds:
            # Check if this species is in our unified list
            if species not in UNIFIED_SPECIES_LIST:
                print(f"   ⚠️ Skipping {species} (not in unified species list)")
                continue
            
            # Check if image file exists
            if not os.path.exists(image_path):
                print(f"   ⚠️ Image not found: {image_path}")
                continue
            
            # Prepare target directory
            species_dir = os.path.join(new_training_dir, species.replace(" ", "_"))
            
            # Create a unique filename for training data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_filename = os.path.basename(image_path)
            base_name, ext = os.path.splitext(original_filename)
            
            # Include location in training filename
            training_filename = f"{species.replace(' ', '_')}_{location}_{timestamp}{ext}"
            training_path = os.path.join(species_dir, training_filename)
            
            # Copy image to training directory
            try:
                shutil.copy2(image_path, training_path)
                
                if species not in extraction_log:
                    extraction_log[species] = 0
                extraction_log[species] += 1
                
            except Exception as e:
                print(f"   ❌ Failed to copy {image_path}: {e}")
        
        # Report extraction results
        print(f"\n📊 Training data extraction results:")
        for species, count in extraction_log.items():
            print(f"   {species}: {count} images extracted")
        
        return extraction_log
        
    except Exception as e:
        print(f"❌ Database extraction failed: {e}")
        return {}

def generate_training_report(new_training_dir):
    """Generate a comprehensive training data report."""
    
    print("📋 Generating training data report...")
    
    species_status = {}
    total_images = 0
    ready_species = 0
    insufficient_species = 0
    missing_species = 0
    
    for species in UNIFIED_SPECIES_LIST:
        species_dir = os.path.join(new_training_dir, species.replace(" ", "_"))
        image_files = [f for f in os.listdir(species_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        count = len(image_files)
        
        species_status[species] = count
        total_images += count
        
        if count >= 20:
            ready_species += 1
        elif count >= 5:
            insufficient_species += 1
        else:
            missing_species += 1
    
    # Generate report
    report = {
        'total_species': len(UNIFIED_SPECIES_LIST),
        'total_images': total_images,
        'ready_species': ready_species,  # >= 20 images
        'insufficient_species': insufficient_species,  # 5-19 images
        'missing_species': missing_species,  # < 5 images
        'species_breakdown': species_status,
        'fountain_species': len([s for s in UNIFIED_SPECIES_LIST if 'fountain' in SPECIES_LOCATIONS[s]]),
        'peanut_species': len([s for s in UNIFIED_SPECIES_LIST if 'peanut' in SPECIES_LOCATIONS[s]]),
        'cross_location_species': len([s for s in UNIFIED_SPECIES_LIST if len(SPECIES_LOCATIONS[s]) > 1])
    }
    
    return report

def print_training_report(report):
    """Print a formatted training data report."""
    
    print("\n📊 TRAINING DATA REPORT")
    print("=" * 50)
    print(f"Total Species: {report['total_species']}")
    print(f"Total Images: {report['total_images']}")
    print(f"Ready for Training (≥20 images): {report['ready_species']}")
    print(f"Need More Data (5-19 images): {report['insufficient_species']}")
    print(f"Missing Data (<5 images): {report['missing_species']}")
    
    print(f"\n📍 Location Breakdown:")
    print(f"   Fountain species: {report['fountain_species']}")
    print(f"   Peanut species: {report['peanut_species']}")
    print(f"   Cross-location: {report['cross_location_species']}")
    
    print(f"\n📋 Species Status:")
    for species, count in report['species_breakdown'].items():
        locations = ", ".join(SPECIES_LOCATIONS[species])
        status = "🟢 Ready" if count >= 20 else "🟡 Insufficient" if count >= 5 else "🔴 Missing"
        print(f"   {species:25} ({locations:15}): {count:3d} images {status}")

def main():
    """Main training data preparation function."""
    
    print("🚀 Fountain Buddy Training Data Preparation")
    print("=" * 60)
    
    # Step 1: Analyze current data
    current_data = analyze_current_training_data()
    
    # Step 2: Create new structure
    new_training_dir = create_unified_training_structure()
    
    # Step 3: Migrate existing data
    migration_log = migrate_existing_training_data(new_training_dir)
    
    # Step 4: Extract from database
    extraction_log = extract_training_data_from_database(new_training_dir)
    
    # Step 5: Identify missing data
    missing_species, species_status = identify_missing_species_data(new_training_dir)
    
    # Step 6: Generate report
    report = generate_training_report(new_training_dir)
    print_training_report(report)
    
    # Step 7: Save metadata
    metadata = generate_metadata()
    metadata_path = os.path.join(new_training_dir, "model_metadata_v2.json")
    
    with open(metadata_path, 'w') as f:
        import json
        json.dump(metadata, f, indent=2)
    
    print(f"\n💾 Metadata saved to: {metadata_path}")
    
    # Summary and next steps
    print(f"\n🎯 NEXT STEPS:")
    if missing_species:
        print(f"1. Collect training data for {len(missing_species)} missing species:")
        for species in missing_species:
            print(f"   - {species}")
    
    if report['ready_species'] >= 10:
        print(f"2. Start training with {report['ready_species']} species that have sufficient data")
        print(f"3. Add new species as data becomes available")
    else:
        print(f"2. Collect more data - only {report['ready_species']} species ready for training")
    
    print(f"4. Update camera managers to start collecting peanut feeder data")
    print(f"5. Monitor both locations for new species appearances")

if __name__ == "__main__":
    main()