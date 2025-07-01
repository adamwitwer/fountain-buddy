#!/usr/bin/env python3
"""
Test script for human feedback system.
Tests database updates and image renaming functionality.
"""

import os
import shutil
import sqlite3
from run import update_bird_species_from_human, parse_human_response, COMMON_BIRDS, DB_NAME

def create_test_database():
    """Create a test database entry for testing."""
    
    # Create a test image file
    test_image_dir = "test_bird_images"
    os.makedirs(test_image_dir, exist_ok=True)
    
    test_image_name = "bird_2025-07-01_14-30-15.jpg"
    test_image_path = os.path.join(test_image_dir, test_image_name)
    
    # Create a dummy image file
    with open(test_image_path, 'w') as f:
        f.write("dummy image content")
    
    # Add entry to database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO bird_visits (timestamp, bird_type, species, confidence, image_path)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "2025-07-01 14:30:15",
        "bird", 
        "Common Grackle",  # AI guess
        0.75,
        test_image_path
    ))
    
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    
    print(f"✅ Created test database entry with ID: {record_id}")
    print(f"✅ Created test image: {test_image_path}")
    
    return test_image_name, test_image_path

def test_parsing():
    """Test the response parsing functionality."""
    
    print("\n🧪 Testing Response Parsing")
    print("=" * 30)
    
    test_cases = [
        ("1", "Northern Cardinal"),
        ("3", "Common Grackle"), 
        ("10", "Gray Catbird"),
        ("15", None),  # Invalid number
        ("Blue Jay", "Blue Jay"),
        ("gray catbird", "Gray Catbird"),
        ("HOUSE SPARROW", "House Sparrow"),
        ("x", None),  # Invalid input
    ]
    
    for input_text, expected in test_cases:
        result = parse_human_response(input_text)
        status = "✅" if result == expected else "❌"
        print(f"   {status} '{input_text}' → {result} (expected: {expected})")

def test_database_update():
    """Test the database update functionality."""
    
    print("\n🧪 Testing Database Update")
    print("=" * 30)
    
    # Create test data
    test_filename, test_path = create_test_database()
    
    try:
        # Test updating with human identification
        success = update_bird_species_from_human(test_filename, "Northern Cardinal")
        
        if success:
            print("✅ Database update successful")
            
            # Verify the update
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT species, confidence FROM bird_visits WHERE image_path LIKE ?", 
                          (f"%{test_filename}%",))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                species, confidence = result
                print(f"✅ Verified update: {species} (confidence: {confidence})")
                
                # Check if image was renamed
                old_name = test_filename
                new_name = test_filename.replace("bird_", "bird_Northern_Cardinal_")
                new_path = test_path.replace(old_name, new_name)
                
                if os.path.exists(new_path):
                    print(f"✅ Image renamed: {old_name} → {new_name}")
                else:
                    print(f"⚠️ Image not renamed (might be expected)")
            else:
                print("❌ Could not verify database update")
        else:
            print("❌ Database update failed")
            
    finally:
        # Cleanup
        cleanup_test_data()

def cleanup_test_data():
    """Clean up test data."""
    
    print("\n🧹 Cleaning up test data...")
    
    # Remove test images
    if os.path.exists("test_bird_images"):
        shutil.rmtree("test_bird_images")
        print("✅ Removed test images")
    
    # Remove test database entries
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bird_visits WHERE image_path LIKE 'test_bird_images%'")
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            print(f"✅ Removed {deleted_count} test database entries")
    except Exception as e:
        print(f"⚠️ Could not clean database: {e}")

def show_common_birds():
    """Display the common birds list."""
    
    print("\n📋 Common Birds List")
    print("=" * 20)
    
    for number, species in COMMON_BIRDS.items():
        print(f"   {number}. {species}")

if __name__ == "__main__":
    print("🧪 Human Feedback System Test")
    print("=" * 35)
    
    show_common_birds()
    test_parsing()
    test_database_update()
    
    print("\n✅ All tests complete!")
    print("\n💡 Next steps:")
    print("   1. Create Discord bot and get bot token")
    print("   2. Add bot to your Discord server")  
    print("   3. Get channel ID for #bird-id")
    print("   4. Add credentials to .env file")
    print("   5. Run discord_bot.py alongside main app")