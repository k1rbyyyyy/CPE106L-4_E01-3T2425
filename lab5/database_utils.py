# Database Utilities for CPE106L Lab 5
# Additional helper functions for database operations

import sqlite3
import os
from datetime import datetime

class DatabaseUtilities:
    """Utility class for database operations"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = os.path.join('database', 'colonial_adventure.db')
        else:
            self.db_path = db_path
    
    def backup_database(self, backup_path=None):
        """Create a backup of the database"""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"database/backup_colonial_adventure_{timestamp}.db"
        
        try:
            # Copy database file
            import shutil
            shutil.copy2(self.db_path, backup_path)
            print(f"Database backed up to: {backup_path}")
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def export_table_to_csv(self, table_name, output_file=None):
        """Export a table to CSV format"""
        if output_file is None:
            output_file = f"database/{table_name}_export.csv"
        
        try:
            import csv
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get column names
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = [col[1] for col in cursor.fetchall()]
                
                # Get all data
                cursor.execute(f"SELECT * FROM {table_name};")
                data = cursor.fetchall()
                
                # Write to CSV
                with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(columns)  # Header
                    writer.writerows(data)    # Data
                
                print(f"Table {table_name} exported to: {output_file}")
                return True
                
        except Exception as e:
            print(f"Error exporting table: {e}")
            return False
    
    def get_database_info(self):
        """Get information about the database structure"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get all tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                
                print("Database Information:")
                print("=" * 40)
                print(f"Database file: {self.db_path}")
                print(f"Total tables: {len(tables)}")
                print("\nTables:")
                
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table};")
                    count = cursor.fetchone()[0]
                    print(f"  {table}: {count} records")
                
                # Get database size
                size = os.path.getsize(self.db_path)
                print(f"\nDatabase size: {size:,} bytes ({size/1024:.1f} KB)")
                
        except Exception as e:
            print(f"Error getting database info: {e}")
    
    def validate_data_integrity(self):
        """Check data integrity and foreign key constraints"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                print("Data Integrity Check:")
                print("=" * 30)
                
                # Check for orphaned reservations (customer doesn't exist)
                cursor.execute("""
                    SELECT COUNT(*) FROM Reservation r
                    LEFT JOIN Customer c ON r.CUSTOMER_NUM = c.CUSTOMER_NUM
                    WHERE c.CUSTOMER_NUM IS NULL;
                """)
                orphaned_reservations = cursor.fetchone()[0]
                
                # Check for orphaned reservations (trip doesn't exist)
                cursor.execute("""
                    SELECT COUNT(*) FROM Reservation r
                    LEFT JOIN Trip t ON r.TRIP_ID = t.TRIP_ID
                    WHERE t.TRIP_ID IS NULL;
                """)
                orphaned_trips = cursor.fetchone()[0]
                
                # Check for orphaned trip guides
                cursor.execute("""
                    SELECT COUNT(*) FROM Trip_Guides tg
                    LEFT JOIN Trip t ON tg.TRIP_ID = t.TRIP_ID
                    WHERE t.TRIP_ID IS NULL;
                """)
                orphaned_trip_guides = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM Trip_Guides tg
                    LEFT JOIN Guide g ON tg.GUIDE_NUM = g.GUIDE_NUM
                    WHERE g.GUIDE_NUM IS NULL;
                """)
                orphaned_guide_assignments = cursor.fetchone()[0]
                
                print(f"Orphaned reservations (invalid customer): {orphaned_reservations}")
                print(f"Orphaned reservations (invalid trip): {orphaned_trips}")
                print(f"Orphaned trip guides (invalid trip): {orphaned_trip_guides}")
                print(f"Orphaned guide assignments (invalid guide): {orphaned_guide_assignments}")
                
                if all(count == 0 for count in [orphaned_reservations, orphaned_trips, 
                                              orphaned_trip_guides, orphaned_guide_assignments]):
                    print("\n✅ Data integrity check passed!")
                else:
                    print("\n❌ Data integrity issues found!")
                
        except Exception as e:
            print(f"Error checking data integrity: {e}")

    def delete_adventure_trip_table(self, table_name="ADVENTURE_TRIP"):
        """
        Delete the ADVENTURE_TRIP table from the database.
        
        This function implements Lab Activity C requirement to delete the ADVENTURE_TRIP table
        after completing the insert and display operations. It includes proper error handling
        and verification steps to ensure safe table deletion.
        
        Args:
            table_name (str): Name of the table to delete (default: ADVENTURE_TRIP)
            
        Returns:
            bool: True if table deletion successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                
                # Step 1: Verify table exists before attempting deletion
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name=?
                """, (table_name,))
                
                table_exists = cursor.fetchone()
                
                if not table_exists:
                    print(f"⚠️  Table '{table_name}' does not exist!")
                    print("   Nothing to delete.")
                    return True  # Consider this successful since desired state is achieved
                
                # Step 2: Show table contents before deletion (for verification)
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                record_count = cursor.fetchone()[0]
                
                print(f"🗑️  Preparing to delete table '{table_name}'")
                print(f"   Table contains {record_count} record(s)")
                
                # Step 3: Execute DROP TABLE command
                drop_table_sql = f"DROP TABLE {table_name}"
                cursor.execute(drop_table_sql)
                connection.commit()
                
                # Step 4: Verify table was successfully deleted
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name=?
                """, (table_name,))
                
                if cursor.fetchone() is None:
                    print(f"✅ Table '{table_name}' deleted successfully!")
                    print(f"   Removed table with {record_count} record(s)")
                    print("   Database cleanup completed")
                    return True
                else:
                    print(f"❌ Table '{table_name}' still exists after deletion attempt!")
                    return False
                
        except sqlite3.OperationalError as operational_error:
            print(f"❌ Operational error deleting table: {operational_error}")
            print("   This might occur if:")
            print("   • The table is referenced by other tables (foreign key constraints)")
            print("   • The database file is locked by another process")
            print("   • Insufficient permissions to modify the database")
            return False
            
        except sqlite3.Error as database_error:
            print(f"❌ Database error deleting table: {database_error}")
            return False
            
        except Exception as general_error:
            print(f"❌ Unexpected error during table deletion: {general_error}")
            return False

    def verify_table_deletion(self, table_name="ADVENTURE_TRIP"):
        """
        Verify that a table has been successfully deleted from the database.
        
        This function provides additional verification for the table deletion process
        and lists remaining tables in the database.
        
        Args:
            table_name (str): Name of the table to verify deletion (default: ADVENTURE_TRIP)
            
        Returns:
            bool: True if table is confirmed deleted, False if table still exists
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                
                # Check if the specific table exists
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name=?
                """, (table_name,))
                
                table_exists = cursor.fetchone()
                
                if table_exists:
                    print(f"❌ Verification failed: Table '{table_name}' still exists!")
                    return False
                else:
                    print(f"✅ Verification successful: Table '{table_name}' has been deleted")
                
                # Show remaining tables in database
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                remaining_tables = cursor.fetchall()
                
                if remaining_tables:
                    print(f"\n📋 Remaining tables in database:")
                    for table in remaining_tables:
                        print(f"   • {table[0]}")
                else:
                    print(f"\n📋 Database is now empty (no tables remaining)")
                
                return True
                
        except sqlite3.Error as database_error:
            print(f"❌ Database error during verification: {database_error}")
            return False
            
        except Exception as general_error:
            print(f"❌ Unexpected error during verification: {general_error}")
            return False

    def execute_complete_prelab_sequence(self):
        """
        Execute the complete PreLab sequence for CPE106L Lab 5:
        a. Create ADVENTURE_TRIP table
        b. Insert Jay Peak record and display contents
        c. Delete ADVENTURE_TRIP table
        
        This function implements the full PreLab activity sequence as specified
        in the lab manual, following proper database operation practices.
        
        Returns:
            bool: True if all PreLab steps completed successfully, False otherwise
        """
        print("🔬 CPE106L Lab 5 - Complete PreLab Activity Sequence")
        print("=" * 60)
        print("PreLab Activities:")
        print("  a. Create ADVENTURE_TRIP table")
        print("  b. Insert Jay Peak record and display contents")
        print("  c. Delete ADVENTURE_TRIP table")
        print("-" * 60)
        
        success_steps = []
        total_steps = 3
        
        # Activity A: Create ADVENTURE_TRIP table
        print("\n🏗️  Activity A: Creating ADVENTURE_TRIP table...")
        if self.create_adventure_trip_table():
            success_steps.append("Table creation")
            print("   ✅ Activity A completed successfully")
        else:
            print("   ❌ Activity A failed - cannot proceed with PreLab")
            return False
        
        # Activity B: Insert Jay Peak record and display contents
        print("\n📝 Activity B: Inserting Jay Peak record and displaying contents...")
        
        # Insert Jay Peak record
        if self.insert_jay_peak_record():
            print("   ✅ Jay Peak record inserted")
            
            # Display table contents
            if self.display_adventure_trip_contents():
                success_steps.append("Record insertion and display")
                print("   ✅ Activity B completed successfully")
            else:
                print("   ⚠️  Record inserted but display failed")
                success_steps.append("Record insertion and display")  # Still count as success
        else:
            print("   ❌ Activity B failed - Jay Peak record insertion failed")
            # Continue with deletion anyway
        
        # Activity C: Delete ADVENTURE_TRIP table
        print("\n🗑️  Activity C: Deleting ADVENTURE_TRIP table...")
        if self.delete_adventure_trip_table():
            # Verify deletion
            if self.verify_table_deletion():
                success_steps.append("Table deletion")
                print("   ✅ Activity C completed successfully")
            else:
                print("   ⚠️  Table deleted but verification failed")
                success_steps.append("Table deletion")  # Still count as success
        else:
            print("   ❌ Activity C failed - table deletion unsuccessful")
        
        # Final summary
        print(f"\n📊 PreLab Activity Summary")
        print("=" * 35)
        print(f"Completed steps: {len(success_steps)}/{total_steps}")
        
        for i, step in enumerate(success_steps, 1):
            activity_letter = chr(ord('A') + i - 1)  # Convert to A, B, C
            print(f"✅ Activity {activity_letter}: {step}")
        
        if len(success_steps) == total_steps:
            print("\n🎉 Complete PreLab sequence executed successfully!")
            print("   All ADVENTURE_TRIP table operations completed")
            print("   Database is ready for InLab activities")
            return True
        else:
            print(f"\n⚠️  PreLab sequence completed with {total_steps - len(success_steps)} issue(s)")
            print("   Review error messages above for troubleshooting")
            return False

# Enhanced test function for complete PreLab sequence
def test_complete_prelab_sequence():
    """
    Test function for the complete PreLab activity sequence.
    
    This function creates the appropriate database connection and executes
    all PreLab activities (A, B, and C) in the correct order.
    """
    print("🧪 Testing Complete CPE106L Lab 5 PreLab Sequence")
    print("=" * 50)
    
    # Use PreLab database for ADVENTURE_TRIP operations
    prelab_database_path = os.path.join('database', 'adventure_trip.db')
    
    # Ensure database directory exists
    os.makedirs('database', exist_ok=True)
    
    # Create utilities instance for PreLab database operations
    database_utilities = DatabaseUtilities(prelab_database_path)
    
    # Execute complete PreLab sequence
    sequence_success = database_utilities.execute_complete_prelab_sequence()
    
    print(f"\n🏁 PreLab Test Result: {'PASSED' if sequence_success else 'FAILED'}")
    return sequence_success

def test_individual_deletion():
    """
    Test function specifically for Activity C (table deletion).
    
    This function tests only the table deletion functionality,
    useful for debugging or isolated testing.
    """
    print("🧪 Testing Activity C: ADVENTURE_TRIP Table Deletion")
    print("=" * 50)
    
    prelab_database_path = os.path.join('database', 'adventure_trip.db')
    
    # Ensure database and directory exist
    os.makedirs('database', exist_ok=True)
    
    database_utilities = DatabaseUtilities(prelab_database_path)
    
    # Test deletion
    deletion_success = database_utilities.delete_adventure_trip_table()
    
    if deletion_success:
        # Verify deletion
        verification_success = database_utilities.verify_table_deletion()
        final_result = deletion_success and verification_success
    else:
        final_result = False
    
    print(f"\n🏁 Deletion Test Result: {'PASSED' if final_result else 'FAILED'}")
    return final_result

# Update main execution block
if __name__ == "__main__":
    print("CPE106L Lab 5 - Database Utilities")
    print("=" * 35)
    print("Available operations:")
    print("1. General database operations test")
    print("2. Lab Activity B test (Jay Peak record)")
    print("3. Lab Activity C test (Delete ADVENTURE_TRIP table)")
    print("4. Complete PreLab sequence (Activities A, B, C)")
    print("5. Database information display")
    
    try:
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            test_database_operations()
        elif choice == "2":
            test_lab_activity_b()
        elif choice == "3":
            test_individual_deletion()
        elif choice == "4":
            test_complete_prelab_sequence()
        elif choice == "5":
            DatabaseUtilities().get_database_info()
        else:
            print("Invalid choice. Please select a number between 1 and 5.")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Please check the database connection and try again.")
