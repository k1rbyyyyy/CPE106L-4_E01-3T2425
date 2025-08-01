# Quick test script for CPE106L Lab 5
# This tests the basic functionality without the interactive menu

import sys
import os
import sqlite3

def test_basic_setup():
    """Test basic database setup"""
    print("Testing CPE106L Lab 5 Database Setup...")
    
    # Test database creation
    db_path = os.path.join('database', 'colonial_adventure.db')
    os.makedirs('database', exist_ok=True)
    
    try:
        # Create a simple test table
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
        """)
        
        cursor.execute("INSERT INTO test_table (name) VALUES (?);", ("Test Record",))
        conn.commit()
        
        cursor.execute("SELECT * FROM test_table;")
        result = cursor.fetchall()
        
        conn.close()
        
        print(f"✅ Database test successful! Created record: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_prelab_import():
    """Test if prelab module can be imported"""
    try:
        sys.path.append('prelab')
        import prelab_activities
        print("✅ PreLab module imported successfully!")
        return True
    except Exception as e:
        print(f"❌ PreLab import failed: {e}")
        return False

def test_inlab_import():
    """Test if inlab module can be imported"""
    try:
        sys.path.append('inlab')
        import inlab_activities
        print("✅ InLab module imported successfully!")
        return True
    except Exception as e:
        print(f"❌ InLab import failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("CPE106L Lab 5 - Quick Test")
    print("=" * 50)
    
    test_basic_setup()
    test_prelab_import()
    test_inlab_import()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("If all tests passed, you can run 'python main.py'")
    print("=" * 50)
