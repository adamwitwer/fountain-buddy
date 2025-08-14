import sqlite3

def add_ai_species_column():
    db_path = 'fountain_buddy.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if the column already exists
        cursor.execute("PRAGMA table_info(bird_visits)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'ai_species' not in columns:
            print("Adding 'ai_species' column to 'bird_visits' table...")
            # Add the new column
            cursor.execute("ALTER TABLE bird_visits ADD COLUMN ai_species TEXT")
            
            # Back-fill the new column with existing species data where confidence is not 1.0
            # This assumes that if confidence is not 1.0, 'species' holds the original AI prediction.
            print("Back-filling 'ai_species' column for existing AI predictions...")
            cursor.execute("UPDATE bird_visits SET ai_species = species WHERE confidence < 1.0")
            
            conn.commit()
            print("Column 'ai_species' added and back-filled successfully.")
        else:
            print("Column 'ai_species' already exists.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_ai_species_column()
