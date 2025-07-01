#!/usr/bin/env python3
"""
Database migration script to add species and confidence columns to existing bird_visits table.
Run this on production to fix the schema mismatch.
"""

import sqlite3
import os

def migrate_database():
    """Add species and confidence columns to existing bird_visits table."""
    
    db_name = "fountain_buddy.db"
    
    if not os.path.exists(db_name):
        print(f"❌ Database {db_name} not found")
        return False
    
    print(f"🔄 Migrating database: {db_name}")
    
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Check current schema
        cursor.execute("PRAGMA table_info(bird_visits)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"📋 Current columns: {columns}")
        
        # Add species column if it doesn't exist
        if 'species' not in columns:
            print("➕ Adding 'species' column...")
            cursor.execute("ALTER TABLE bird_visits ADD COLUMN species TEXT")
            print("   ✅ Added 'species' column")
        else:
            print("   ✅ 'species' column already exists")
        
        # Add confidence column if it doesn't exist
        if 'confidence' not in columns:
            print("➕ Adding 'confidence' column...")
            cursor.execute("ALTER TABLE bird_visits ADD COLUMN confidence REAL")
            print("   ✅ Added 'confidence' column")
        else:
            print("   ✅ 'confidence' column already exists")
        
        # Verify new schema
        cursor.execute("PRAGMA table_info(bird_visits)")
        new_columns = [row[1] for row in cursor.fetchall()]
        print(f"📋 Updated columns: {new_columns}")
        
        # Check how many records exist
        cursor.execute("SELECT COUNT(*) FROM bird_visits")
        record_count = cursor.fetchone()[0]
        print(f"📊 Total records in database: {record_count}")
        
        conn.commit()
        conn.close()
        
        print("✅ Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🗃️  Database Migration for Bird Species Feature")
    print("=" * 50)
    
    success = migrate_database()
    
    if success:
        print("\n🎉 Migration complete! You can now restart the fountain-buddy service.")
        print("   The species identification feature should work correctly.")
    else:
        print("\n💥 Migration failed. Please check the error messages above.")