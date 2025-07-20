#!/usr/bin/env python3
"""
Automated Photo Cleanup Scheduler for Fountain Buddy
Runs photo organization and cleanup on a schedule while protecting training data.
"""

import schedule
import time
import logging
from photo_organizer import PhotoOrganizer
from datetime import datetime
import os

# Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_dir}/photo_cleanup.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PhotoCleanupScheduler:
    def __init__(self):
        self.organizer = PhotoOrganizer()
    
    def daily_organization(self):
        """Run daily photo organization (move recent photos to active)."""
        logger.info("Starting daily photo organization...")
        try:
            # Only organize and update paths, don't delete anything
            moved, skipped = self.organizer.organize_photos()
            updated = self.organizer.update_database_paths()
            
            logger.info(f"Daily organization complete: {moved} moved, {skipped} skipped, {updated} paths updated")
            return True
        except Exception as e:
            logger.error(f"Daily organization failed: {e}")
            return False
    
    def weekly_cleanup(self):
        """Run weekly cleanup (remove old archived photos)."""
        logger.info("Starting weekly cleanup...")
        try:
            deleted = self.organizer.cleanup_old_archives()
            logger.info(f"Weekly cleanup complete: {deleted} old photos deleted")
            return True
        except Exception as e:
            logger.error(f"Weekly cleanup failed: {e}")
            return False
    
    def monthly_full_organization(self):
        """Run complete monthly reorganization."""
        logger.info("Starting monthly full organization...")
        try:
            results = self.organizer.run_full_organization()
            logger.info(f"Monthly organization complete: {results}")
            return True
        except Exception as e:
            logger.error(f"Monthly organization failed: {e}")
            return False
    
    def setup_schedule(self):
        """Set up the cleanup schedule."""
        # Daily organization at 2 AM
        schedule.every().day.at("02:00").do(self.daily_organization)
        
        # Weekly cleanup on Sunday at 3 AM
        schedule.every().sunday.at("03:00").do(self.weekly_cleanup)
        
        # Monthly full organization on the 1st at 4 AM
        schedule.every().month.do(self.monthly_full_organization)
        
        logger.info("Photo cleanup schedule configured:")
        logger.info("  - Daily organization: 2:00 AM")
        logger.info("  - Weekly cleanup: Sunday 3:00 AM")
        logger.info("  - Monthly full organization: 1st of month 4:00 AM")
    
    def run_scheduler(self):
        """Run the scheduler continuously."""
        self.setup_schedule()
        
        logger.info("Photo cleanup scheduler started...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def run_now(self, operation="full"):
        """Run organization immediately for testing."""
        logger.info(f"Running {operation} organization now...")
        
        if operation == "daily":
            return self.daily_organization()
        elif operation == "weekly":
            return self.weekly_cleanup()
        elif operation == "monthly" or operation == "full":
            return self.monthly_full_organization()
        else:
            logger.error(f"Unknown operation: {operation}")
            return False

def main():
    import sys
    
    scheduler = PhotoCleanupScheduler()
    
    if len(sys.argv) > 1:
        # Run specific operation immediately
        operation = sys.argv[1]
        if operation in ["daily", "weekly", "monthly", "full"]:
            success = scheduler.run_now(operation)
            sys.exit(0 if success else 1)
        else:
            print("Usage: python photo_cleanup_scheduler.py [daily|weekly|monthly|full]")
            sys.exit(1)
    else:
        # Run scheduler continuously
        try:
            scheduler.run_scheduler()
        except KeyboardInterrupt:
            logger.info("Photo cleanup scheduler stopped by user")
            sys.exit(0)

if __name__ == "__main__":
    main()