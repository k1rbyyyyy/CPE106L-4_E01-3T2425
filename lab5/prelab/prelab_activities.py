"""
CPE106L Laboratory 5 - PreLab Activities
Colonial Adventure Tours Database - ADVENTURE_TRIP Table Operations
"""

import sqlite3
import os
import time
from typing import Optional

def create_database_connection(database_name: str = "adventure_trip.db") -> Optional[sqlite3.Connection]:
    """
    Create a database connection to SQLite database with enhanced error handling.
    
    This function implements proper database connection management following
    CPE106L lab requirements and handles common connection issues.
    
    Args:
        database_name (str): Name of the database file
        
    Returns:
        sqlite3.Connection: Connection object or None if error
    """
    try:
        # Create database directory if it doesn't exist
        db_dir = os.path.join(os.path.dirname(__file__), '..', 'database')
        os.makedirs(db_dir, exist_ok=True)
        
        # Full path to database file
        db_path = os.path.join(db_dir, database_name)
        
        # Enhanced connection with timeout and retry mechanism
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                # Set timeout to handle locked database
                connection = sqlite3.connect(db_path, timeout=10.0)
                
                # Test the connection with a simple query
                cursor = connection.cursor()
                cursor.execute("SELECT sqlite_version();")
                version = cursor.fetchone()
                
                print(f"✅ Connected to database: {database_name}")
                print(f"   SQLite version: {version[0]}")
                print(f"   Database path: {db_path}")
                
                return connection
                
            except sqlite3.OperationalError as op_error:
                if "database is locked" in str(op_error).lower() and attempt < max_retries - 1:
                    print(f"⚠️  Database locked, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    raise op_error
        
        # If we reach here, all retries failed
        raise sqlite3.OperationalError("Database remains locked after all retry attempts")
        
    except sqlite3.OperationalError as operational_error:
        print(f"❌ Database operational error: {operational_error}")
        print("   Possible solutions:")
        print("   • Close DB Browser for SQLite if it's open")
        print("   • Check if another Python script is using the database")
        print("   • Verify database file permissions")
        return None
        
    except sqlite3.Error as database_error:
        print(f"❌ Database error: {database_error}")
        return None
        
    except Exception as general_error:
        print(f"❌ Unexpected error connecting to database: {general_error}")
        return None

def create_adventure_trip_table(connection: sqlite3.Connection) -> bool:
    """
    Create the ADVENTURE_TRIP table with proper structure and enhanced error handling.
    
    This function implements Lab Activity A requirements with proper SQL formatting
    and comprehensive error handling for database operations.
    
    Args:
        connection: Database connection object
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = connection.cursor()
        
        # Check if table already exists to provide better user feedback
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='ADVENTURE_TRIP'
        """)
        
        if cursor.fetchone():
            print("ℹ️  ADVENTURE_TRIP table already exists, skipping creation")
            return True
        
        # SQL command to create ADVENTURE_TRIP table with proper formatting
        create_table_sql = """
        CREATE TABLE ADVENTURE_TRIP (
            TRIP_ID INTEGER PRIMARY KEY,
            TRIP_NAME VARCHAR(100) NOT NULL,
            START_LOCATION VARCHAR(100) NOT NULL,
            STATE VARCHAR(50) NOT NULL,
            DISTANCE INTEGER NOT NULL,
            MAX_GRP_SIZE INTEGER NOT NULL,
            TYPE VARCHAR(50) NOT NULL,
            SEASON VARCHAR(20) NOT NULL
        )
        """
        
        # Execute table creation with transaction handling
        cursor.execute(create_table_sql)
        connection.commit()
        
        # Verify table was created successfully
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='ADVENTURE_TRIP'
        """)
        
        if cursor.fetchone():
            print("✅ ADVENTURE_TRIP table created successfully")
            
            # Display table structure for verification
            cursor.execute("PRAGMA table_info(ADVENTURE_TRIP)")
            columns = cursor.fetchall()
            
            print("   Table structure:")
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                not_null = "NOT NULL" if col[3] else "NULL"
                pk = "PRIMARY KEY" if col[5] else ""
                print(f"   • {col_name}: {col_type} {not_null} {pk}".strip())
            
            return True
        else:
            print("❌ Table creation verification failed")
            return False
        
    except sqlite3.OperationalError as operational_error:
        print(f"❌ Database operational error creating table: {operational_error}")
        print("   This might indicate:")
        print("   • Database is still locked by another process")
        print("   • Insufficient permissions to modify database")
        return False
        
    except sqlite3.Error as database_error:
        print(f"❌ Database error creating ADVENTURE_TRIP table: {database_error}")
        return False
        
    except Exception as general_error:
        print(f"❌ Unexpected error during table creation: {general_error}")
        return False

def insert_sample_record(connection: sqlite3.Connection) -> bool:
    """
    Insert the sample Jay Peak record into ADVENTURE_TRIP table.
    
    This function implements Lab Activity B requirements using parameterized
    queries to prevent SQL injection and ensure data integrity.
    
    Args:
        connection: Database connection object
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = connection.cursor()
        
        # Check if record already exists to prevent duplicates
        cursor.execute("SELECT COUNT(*) FROM ADVENTURE_TRIP WHERE TRIP_ID = ?", (45,))
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            print("ℹ️  Jay Peak record (ID: 45) already exists, skipping insertion")
            return True
        
        # Parameterized INSERT statement for security (prevents SQL injection)
        insert_sql = """
        INSERT INTO ADVENTURE_TRIP (
            TRIP_ID, TRIP_NAME, START_LOCATION, STATE, 
            DISTANCE, MAX_GRP_SIZE, TYPE, SEASON
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Sample data: Jay Peak trip as specified in lab requirements
        jay_peak_data = (45, "Jay Peak", "Jay", "VT", 8, 8, "Hiking", "Summer")
        
        # Execute insertion with transaction handling
        cursor.execute(insert_sql, jay_peak_data)
        connection.commit()
        
        # Verify insertion was successful
        cursor.execute("SELECT COUNT(*) FROM ADVENTURE_TRIP WHERE TRIP_ID = ?", (45,))
        if cursor.fetchone()[0] == 1:
            print("✅ Sample record (Jay Peak) inserted successfully")
            print(f"   Record details:")
            print(f"   • Trip ID: {jay_peak_data[0]}")
            print(f"   • Trip Name: {jay_peak_data[1]}")
            print(f"   • Location: {jay_peak_data[2]}, {jay_peak_data[3]}")
            print(f"   • Distance: {jay_peak_data[4]} miles")
            print(f"   • Max Group Size: {jay_peak_data[5]} people")
            print(f"   • Type: {jay_peak_data[6]}")
            print(f"   • Season: {jay_peak_data[7]}")
            return True
        else:
            print("❌ Record insertion verification failed")
            return False
        
    except sqlite3.IntegrityError as integrity_error:
        print(f"❌ Data integrity error: {integrity_error}")
        print("   This might occur if:")
        print("   • A record with the same TRIP_ID already exists")
        print("   • Data violates table constraints")
        return False
        
    except sqlite3.OperationalError as operational_error:
        print(f"❌ Database operational error during insertion: {operational_error}")
        return False
        
    except sqlite3.Error as database_error:
        print(f"❌ Database error inserting sample record: {database_error}")
        return False
        
    except Exception as general_error:
        print(f"❌ Unexpected error during record insertion: {general_error}")
        return False

def display_table_contents(connection: sqlite3.Connection) -> None:
    """
    Display all contents of the ADVENTURE_TRIP table with formatted output.
    
    This function provides a clear, formatted display of table contents
    following proper database query practices.
    
    Args:
        connection: Database connection object
    """
    try:
        cursor = connection.cursor()
        
        # Query to select all records with ordering for consistent display
        select_sql = "SELECT * FROM ADVENTURE_TRIP ORDER BY TRIP_ID"
        cursor.execute(select_sql)
        
        records = cursor.fetchall()
        
        print("\n📊 ADVENTURE_TRIP Table Contents:")
        print("=" * 90)
        
        if records:
            # Display formatted header
            header_format = (
                f"{'ID':<5} {'NAME':<15} {'LOCATION':<12} {'STATE':<6} "
                f"{'DIST':<6} {'SIZE':<6} {'TYPE':<10} {'SEASON':<10}"
            )
            print(header_format)
            print("-" * 90)
            
            # Display each record with consistent formatting
            for record in records:
                row_format = (
                    f"{record[0]:<5} {record[1]:<15} {record[2]:<12} {record[3]:<6} "
                    f"{record[4]:<6} {record[5]:<6} {record[6]:<10} {record[7]:<10}"
                )
                print(row_format)
            
            print("-" * 90)
            print(f"Total records displayed: {len(records)}")
        else:
            print("📝 No records found in ADVENTURE_TRIP table")
        
        print("=" * 90)
        
    except sqlite3.Error as database_error:
        print(f"❌ Database error displaying table contents: {database_error}")
        
    except Exception as general_error:
        print(f"❌ Unexpected error during table display: {general_error}")

def delete_adventure_trip_table(connection: sqlite3.Connection) -> bool:
    """
    Delete the ADVENTURE_TRIP table with proper verification.
    
    This function implements Lab Activity C requirements with enhanced
    error handling and verification of table deletion.
    
    Args:
        connection: Database connection object
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = connection.cursor()
        
        # Check if table exists before attempting deletion
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='ADVENTURE_TRIP'
        """)
        
        if not cursor.fetchone():
            print("ℹ️  ADVENTURE_TRIP table does not exist, nothing to delete")
            return True
        
        # Get record count before deletion for user feedback
        cursor.execute("SELECT COUNT(*) FROM ADVENTURE_TRIP")
        record_count = cursor.fetchone()[0]
        
        # SQL command to drop table with IF EXISTS for safety
        drop_table_sql = "DROP TABLE IF EXISTS ADVENTURE_TRIP"
        
        cursor.execute(drop_table_sql)
        connection.commit()
        
        # Verify table was successfully deleted
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='ADVENTURE_TRIP'
        """)
        
        if cursor.fetchone() is None:
            print("✅ ADVENTURE_TRIP table deleted successfully")
            print(f"   Removed table containing {record_count} record(s)")
            return True
        else:
            print("❌ Table deletion verification failed - table still exists")
            return False
        
    except sqlite3.OperationalError as operational_error:
        print(f"❌ Database operational error during deletion: {operational_error}")
        print("   This might occur if:")
        print("   • Database is locked by another process")
        print("   • Table is referenced by foreign key constraints")
        return False
        
    except sqlite3.Error as database_error:
        print(f"❌ Database error deleting ADVENTURE_TRIP table: {database_error}")
        return False
        
    except Exception as general_error:
        print(f"❌ Unexpected error during table deletion: {general_error}")
        return False

def check_database_status(database_name: str = "adventure_trip.db") -> bool:
    """
    Check if database is accessible and not locked by other processes.
    
    Args:
        database_name (str): Name of the database file to check
        
    Returns:
        bool: True if database is accessible, False otherwise
    """
    try:
        db_dir = os.path.join(os.path.dirname(__file__), '..', 'database')
        db_path = os.path.join(db_dir, database_name)
        
        if not os.path.exists(db_path):
            print(f"ℹ️  Database file does not exist: {db_path}")
            return True  # Not existing is okay, will be created
        
        # Try a quick connection test
        test_connection = sqlite3.connect(db_path, timeout=1.0)
        cursor = test_connection.cursor()
        cursor.execute("SELECT 1")
        test_connection.close()
        
        print(f"✅ Database is accessible: {database_name}")
        return True
        
    except sqlite3.OperationalError as op_error:
        if "database is locked" in str(op_error).lower():
            print(f"❌ Database is currently locked: {database_name}")
            print("   Please close DB Browser for SQLite or other database connections")
            return False
        else:
            print(f"❌ Database operational error: {op_error}")
            return False
    except Exception as error:
        print(f"❌ Error checking database status: {error}")
        return False

def run_prelab_activities():
    """
    Main function to execute all PreLab activities with enhanced error handling.
    
    This function implements the complete CPE106L Lab 5 PreLab sequence:
    1. Create ADVENTURE_TRIP table
    2. Insert Jay Peak record
    3. Display table contents
    4. Delete ADVENTURE_TRIP table
    """
    print("\n🔬 Starting CPE106L PreLab Activities")
    print("=" * 55)
    print("Lab Activities:")
    print("  A. Create ADVENTURE_TRIP table")
    print("  B. Insert Jay Peak record and display contents")
    print("  C. Delete ADVENTURE_TRIP table")
    print("=" * 55)
    
    # Pre-flight check: ensure database is accessible
    print("\n🔍 Pre-flight database check...")
    if not check_database_status():
        print("❌ Database accessibility check failed.")
        print("   Please ensure no other applications are using the database.")
        return
    
    # Create database connection using context manager for proper resource management
    connection = create_database_connection()
    
    if connection is None:
        print("❌ Failed to establish database connection. Exiting PreLab.")
        return
    
    try:
        with connection:  # Automatic commit/rollback handling
            print("\n📋 Executing PreLab Activity Sequence:")
            
            # Activity A: Create ADVENTURE_TRIP table
            print("\n🏗️  Activity A: Creating ADVENTURE_TRIP table...")
            table_created = create_adventure_trip_table(connection)
            if not table_created:
                print("❌ Failed to create table. Stopping PreLab activities.")
                return
            
            # Activity B: Insert sample record and display contents
            print("\n📝 Activity B: Inserting sample record (Jay Peak)...")
            record_inserted = insert_sample_record(connection)
            if not record_inserted:
                print("⚠️  Failed to insert sample record, but continuing with display...")
            
            print("\n📊 Activity B: Displaying table contents...")
            display_table_contents(connection)
            
            # Activity C: Delete the table
            print("\n🗑️  Activity C: Deleting ADVENTURE_TRIP table...")
            table_deleted = delete_adventure_trip_table(connection)
            if not table_deleted:
                print("❌ Failed to delete table.")
                return
        
        print("\n✅ All PreLab activities completed successfully!")
        print("=" * 55)
        
    except Exception as unexpected_error:
        print(f"❌ Unexpected error during PreLab execution: {unexpected_error}")
        print("   Rolling back any incomplete transactions...")
        
    finally:
        # Ensure connection is properly closed
        if connection:
            connection.close()
            print("🔒 Database connection closed safely")

if __name__ == "__main__":
    run_prelab_activities()
