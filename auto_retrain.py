#!/usr/bin/env python3
"""
Automated Retraining System
Monitors for new human corrections and triggers model retraining
"""

import os
import sqlite3
import json
from datetime import datetime
import subprocess
import logging

class AutoRetrainer:
    def __init__(self, db_path='fountain_buddy.db', min_new_samples=15):
        self.db_path = db_path
        self.min_new_samples = min_new_samples
        self.training_log_file = 'training_log.json'
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('auto_retrain.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def get_last_training_date(self):
        """Get the date of the last training session"""
        if not os.path.exists(self.training_log_file):
            return None
        
        try:
            with open(self.training_log_file, 'r') as f:
                log_data = json.load(f)
            return log_data.get('last_training_date')
        except:
            return None
    
    def count_new_corrections(self):
        """Count new human corrections since last training"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        last_training_date = self.get_last_training_date()
        
        if last_training_date:
            cursor.execute("""
                SELECT COUNT(*) FROM bird_visits 
                WHERE species IS NOT NULL 
                AND confidence = 1.0 
                AND species NOT IN ('Unknown; Not A Bird', 'Not A Bird')
                AND timestamp > ?
            """, (last_training_date,))
        else:
            cursor.execute("""
                SELECT COUNT(*) FROM bird_visits 
                WHERE species IS NOT NULL 
                AND confidence = 1.0 
                AND species NOT IN ('Unknown; Not A Bird', 'Not A Bird')
            """)
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def get_species_distribution(self):
        """Get current species distribution for logging"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT species, COUNT(*) as count 
            FROM bird_visits 
            WHERE species IS NOT NULL 
            AND confidence = 1.0 
            AND species NOT IN ('Unknown; Not A Bird', 'Not A Bird')
            GROUP BY species 
            ORDER BY count DESC
        """)
        
        distribution = dict(cursor.fetchall())
        conn.close()
        
        return distribution
    
    def should_retrain(self):
        """Check if retraining should be triggered"""
        new_corrections = self.count_new_corrections()
        
        self.logger.info(f"Found {new_corrections} new corrections since last training")
        
        if new_corrections >= self.min_new_samples:
            return True, new_corrections
        
        return False, new_corrections
    
    def trigger_retraining(self):
        """Trigger the retraining process"""
        try:
            self.logger.info("Starting model retraining...")
            
            # Run the enhanced training script
            result = subprocess.run(
                ['./venv/bin/python', 'bird_trainer_enhanced.py'],
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            if result.returncode == 0:
                self.logger.info("Model retraining completed successfully")
                self.update_training_log(success=True)
                return True
            else:
                self.logger.error(f"Retraining failed: {result.stderr}")
                self.update_training_log(success=False, error=result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Retraining timed out")
            self.update_training_log(success=False, error="Timeout")
            return False
        except Exception as e:
            self.logger.error(f"Retraining error: {e}")
            self.update_training_log(success=False, error=str(e))
            return False
    
    def update_training_log(self, success=True, error=None):
        """Update the training log file"""
        log_data = {
            'last_training_date': datetime.now().isoformat(),
            'success': success,
            'species_distribution': self.get_species_distribution(),
            'new_corrections_count': self.count_new_corrections()
        }
        
        if error:
            log_data['error'] = error
        
        with open(self.training_log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def check_and_retrain(self):
        """Main function to check and potentially retrain"""
        self.logger.info("Checking for retraining necessity...")
        
        should_retrain, new_count = self.should_retrain()
        
        if should_retrain:
            self.logger.info(f"Triggering retraining with {new_count} new corrections")
            success = self.trigger_retraining()
            
            if success:
                self.logger.info("Automatic retraining completed successfully")
                return True
            else:
                self.logger.error("Automatic retraining failed")
                return False
        else:
            self.logger.info(f"No retraining needed ({new_count}/{self.min_new_samples} new corrections)")
            return False
    
    def force_retrain(self):
        """Force retraining regardless of sample count"""
        self.logger.info("Force retraining requested...")
        return self.trigger_retraining()

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated Bird Model Retraining')
    parser.add_argument('--force', action='store_true', help='Force retraining')
    parser.add_argument('--min-samples', type=int, default=15, 
                       help='Minimum new samples to trigger retraining')
    parser.add_argument('--check-only', action='store_true', 
                       help='Only check if retraining is needed')
    
    args = parser.parse_args()
    
    retrainer = AutoRetrainer(min_new_samples=args.min_samples)
    
    if args.force:
        retrainer.force_retrain()
    elif args.check_only:
        should_retrain, count = retrainer.should_retrain()
        print(f"Should retrain: {should_retrain} ({count} new corrections)")
    else:
        retrainer.check_and_retrain()

if __name__ == "__main__":
    main()