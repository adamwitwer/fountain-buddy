#!/usr/bin/env python3
"""
Photo Organization System for Fountain Buddy
Manages bird photo storage with intelligent archival and cleanup while protecting training data.
"""

import os
import shutil
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Configuration
DB_NAME = "fountain_buddy.db"
BIRD_IMAGES_DIR = "bird_images"
TRAINING_DATA_DIR = "training_data"
ACTIVE_DAYS = 30  # Keep photos in active for 30 days
ARCHIVE_MONTHS = 6  # Keep archived photos for 6 months
HIGH_CONFIDENCE_THRESHOLD = 0.8

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PhotoOrganizer:
    def __init__(self):
        self.db_name = DB_NAME
        self.bird_images_dir = Path(BIRD_IMAGES_DIR)
        self.training_data_dir = Path(TRAINING_DATA_DIR)
        self.active_dir = self.bird_images_dir / "active"
        self.archive_dir = self.bird_images_dir / "archive"
        self.training_candidates_dir = self.bird_images_dir / "training_candidates"
        
        # Ensure directories exist
        self.active_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.training_candidates_dir.mkdir(parents=True, exist_ok=True)
    
    def get_photo_metadata(self, image_path):
        """Get metadata for a photo from the database."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT timestamp, species, confidence, bird_type
                FROM bird_visits 
                WHERE image_path = ? OR image_path LIKE ?
                ORDER BY timestamp DESC LIMIT 1
            """, (str(image_path), f"%{image_path.name}%"))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'timestamp': result[0],
                    'species': result[1],
                    'confidence': result[2],
                    'bird_type': result[3]
                }
            return None
        except Exception as e:
            logger.error(f"Error getting metadata for {image_path}: {e}")
            return None
    
    def is_training_protected(self, image_path):
        """Check if a photo is protected as training data."""
        # Check if the image exists in training_data directory
        if self.training_data_dir.exists():
            for species_dir in self.training_data_dir.iterdir():
                if species_dir.is_dir():
                    for training_image in species_dir.iterdir():
                        if training_image.name == image_path.name:
                            return True
        return False
    
    def get_photo_age_days(self, image_path):
        """Calculate age of photo in days based on filename timestamp."""
        try:
            # Extract timestamp from filename: bird_Species_YYYY-MM-DD_HH-MM-SS.jpg
            filename = image_path.stem
            if '_' in filename:
                # Try to find date pattern in filename
                parts = filename.split('_')
                for i, part in enumerate(parts):
                    if len(part) == 10 and part.count('-') == 2:  # YYYY-MM-DD format
                        date_str = part
                        if i + 1 < len(parts):
                            time_str = parts[i + 1].replace('-', ':')
                            datetime_str = f"{date_str} {time_str}"
                            photo_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                            return (datetime.now() - photo_time).days
            
            # Fallback to file modification time
            stat = image_path.stat()
            file_time = datetime.fromtimestamp(stat.st_mtime)
            return (datetime.now() - file_time).days
        except Exception as e:
            logger.warning(f"Could not determine age for {image_path}: {e}")
            return 0
    
    def organize_photos(self):
        """Organize photos based on age and confidence."""
        logger.info("Starting photo organization...")
        
        moved_count = 0
        skipped_count = 0
        
        # Collect all image paths to process
        image_paths_to_process = []
        
        # Process all photos in the main bird_images directory
        for image_path in self.bird_images_dir.iterdir():
            if image_path.is_file() and image_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                # Skip if already in organized subdirectories
                if image_path.parent.name not in ['active', 'archive', 'training_candidates']:
                    image_paths_to_process.append(image_path)
        
        # Also process unclassified photos in fountain/ subdirectory
        fountain_dir = self.bird_images_dir / "fountain"
        if fountain_dir.exists():
            logger.info(f"Processing unclassified photos in fountain/ directory...")
            for image_path in fountain_dir.iterdir():
                if image_path.is_file() and image_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    image_paths_to_process.append(image_path)
        
        logger.info(f"Found {len(image_paths_to_process)} photos to organize")
        
        # Process all collected image paths
        for image_path in image_paths_to_process:
            
            # Skip if training protected
            if self.is_training_protected(image_path):
                logger.info(f"Skipping training-protected image: {image_path.name}")
                skipped_count += 1
                continue
            
            # Get photo metadata and age
            metadata = self.get_photo_metadata(image_path)
            age_days = self.get_photo_age_days(image_path)
            
            # Determine destination based on age and confidence
            if age_days <= ACTIVE_DAYS:
                # Recent photos go to active
                destination = self.active_dir / image_path.name
            else:
                # Older photos go to monthly archive
                if metadata and metadata['timestamp']:
                    try:
                        photo_date = datetime.fromisoformat(metadata['timestamp'].replace('Z', '+00:00'))
                        month_dir = self.archive_dir / f"{photo_date.year}-{photo_date.month:02d}"
                    except:
                        month_dir = self.archive_dir / f"{datetime.now().year}-{datetime.now().month:02d}"
                else:
                    month_dir = self.archive_dir / f"{datetime.now().year}-{datetime.now().month:02d}"
                
                month_dir.mkdir(exist_ok=True)
                destination = month_dir / image_path.name
            
            # Move the photo
            try:
                shutil.move(str(image_path), str(destination))
                logger.info(f"Moved {image_path.name} to {destination.parent.name}")
                moved_count += 1
            except Exception as e:
                logger.error(f"Error moving {image_path.name}: {e}")
        
        logger.info(f"Organization complete: {moved_count} photos moved, {skipped_count} skipped")
        return moved_count, skipped_count
    
    def cleanup_old_archives(self):
        """Remove archived photos older than ARCHIVE_MONTHS."""
        logger.info("Starting cleanup of old archives...")
        
        cutoff_date = datetime.now() - timedelta(days=ARCHIVE_MONTHS * 30)
        deleted_count = 0
        
        if not self.archive_dir.exists():
            return deleted_count
        
        for month_dir in self.archive_dir.iterdir():
            if not month_dir.is_dir():
                continue
            
            try:
                # Parse month directory name (YYYY-MM format)
                year, month = month_dir.name.split('-')
                month_date = datetime(int(year), int(month), 1)
                
                if month_date < cutoff_date:
                    # Delete entire month directory
                    shutil.rmtree(month_dir)
                    logger.info(f"Deleted archived month: {month_dir.name}")
                    deleted_count += len(list(month_dir.glob('*.jpg'))) if month_dir.exists() else 0
                else:
                    # Clean individual files in this month if needed
                    for image_file in month_dir.iterdir():
                        if image_file.is_file():
                            age_days = self.get_photo_age_days(image_file)
                            if age_days > ARCHIVE_MONTHS * 30:
                                # Check if it's training protected before deletion
                                if not self.is_training_protected(image_file):
                                    image_file.unlink()
                                    logger.info(f"Deleted old archived photo: {image_file.name}")
                                    deleted_count += 1
            except Exception as e:
                logger.error(f"Error processing archive directory {month_dir.name}: {e}")
        
        logger.info(f"Cleanup complete: {deleted_count} old photos deleted")
        return deleted_count
    
    def update_database_paths(self):
        """Update database to reflect new photo locations."""
        logger.info("Updating database paths...")
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Get all records with image paths
            cursor.execute("SELECT id, image_path FROM bird_visits WHERE image_path IS NOT NULL")
            records = cursor.fetchall()
            
            updated_count = 0
            
            for record_id, old_path in records:
                if not old_path:
                    continue
                
                old_path_obj = Path(old_path)
                filename = old_path_obj.name
                
                # Find the new location
                new_path = None
                
                # Check active directory
                active_path = self.active_dir / filename
                if active_path.exists():
                    new_path = str(active_path)
                else:
                    # Check archive directories
                    for month_dir in self.archive_dir.iterdir():
                        if month_dir.is_dir():
                            archive_path = month_dir / filename
                            if archive_path.exists():
                                new_path = str(archive_path)
                                break
                
                # Update database if new path found and different
                if new_path and new_path != old_path:
                    cursor.execute("UPDATE bird_visits SET image_path = ? WHERE id = ?", (new_path, record_id))
                    updated_count += 1
            
            conn.commit()
            conn.close()
            
            logger.info(f"Database update complete: {updated_count} paths updated")
            return updated_count
        
        except Exception as e:
            logger.error(f"Error updating database paths: {e}")
            return 0
    
    def run_full_organization(self):
        """Run complete photo organization process."""
        logger.info("Starting full photo organization process...")
        
        # Step 1: Organize current photos
        moved, skipped = self.organize_photos()
        
        # Step 2: Update database paths
        updated = self.update_database_paths()
        
        # Step 3: Clean up old archives
        deleted = self.cleanup_old_archives()
        
        # Summary
        logger.info(f"Organization complete:")
        logger.info(f"  - Photos moved: {moved}")
        logger.info(f"  - Photos skipped (training protected): {skipped}")
        logger.info(f"  - Database paths updated: {updated}")
        logger.info(f"  - Old photos deleted: {deleted}")
        
        return {
            'moved': moved,
            'skipped': skipped,
            'updated': updated,
            'deleted': deleted
        }

if __name__ == "__main__":
    organizer = PhotoOrganizer()
    results = organizer.run_full_organization()
    print(f"Organization results: {results}")