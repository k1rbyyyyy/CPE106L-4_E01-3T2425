"""
CPE106L Laboratory 5 - Colonial Adventure Tours Database Manager
Utility functions for managing the complete Colonial Adventure database
"""

import sqlite3
import os
from typing import Optional, List, Tuple

class ColonialDatabaseManager:
    """
    Database manager for Colonial Adventure Tours database operations.
    
    This class provides comprehensive database management functionality
    following CPE106L lab requirements and coding guidelines.
    """
    
    def __init__(self, database_name: str = "colonial_adventure.db"):
        """
        Initialize the database manager with proper path resolution.
        
        Args:
            database_name (str): Name of the database file
        """
        self.db_dir = os.path.join(os.path.dirname(__file__))
        self.db_path = os.path.join(self.db_dir, database_name)
        self.ensure_database_directory()
    
    def ensure_database_directory(self) -> None:
        """Create database directory if it doesn't exist."""
        os.makedirs(self.db_dir, exist_ok=True)
    
    def execute_sql_script(self, script_path: str = "SQLServerColonial.sql") -> bool:
        """
        Execute the SQLServerColonial.sql script to create and populate database.
        
        This function reads and executes the SQL script file, handling
        SQLite-specific requirements and providing comprehensive error handling.
        
        Args:
            script_path (str): Path to the SQL script file
            
        Returns:
            bool: True if script execution successful, False otherwise
        """
        try:
            # Construct full path to SQL script
            full_script_path = os.path.join(self.db_dir, script_path)
            
            if not os.path.exists(full_script_path):
                print(f"❌ SQL script not found: {full_script_path}")
                return False
            
            # Read SQL script content
            with open(full_script_path, 'r', encoding='utf-8') as script_file:
                sql_content = script_file.read()
            
            print(f"📖 Reading SQL script: {script_path}")
            print(f"📁 Database location: {self.db_path}")
            
            # Execute SQL script using context manager for proper resource management
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                
                # Enable foreign key constraints (important for referential integrity)
                cursor.execute("PRAGMA foreign_keys = ON")
                
                # Split script into individual statements and execute
                # SQLite executescript() handles multiple statements properly
                cursor.executescript(sql_content)
                
                print("✅ SQL script executed successfully")
                print("✅ Database tables created and populated")
                
                return True
                
        except sqlite3.Error as database_error:
            print(f"❌ Database error executing script: {database_error}")
            return False
            
        except FileNotFoundError as file_error:
            print(f"❌ Script file not found: {file_error}")
            return False
            
        except Exception as general_error:
            print(f"❌ Unexpected error executing script: {general_error}")
            return False
    
    def verify_database_integrity(self) -> bool:
        """
        Verify that all tables were created correctly and contain expected data.
        
        This function performs comprehensive validation of the database
        structure and data integrity following lab requirements.
        
        Returns:
            bool: True if verification successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                
                print("\n🔍 Verifying Database Integrity")
                print("=" * 40)
                
                # Expected tables and their minimum record counts
                expected_tables = {
                    'Customer': 9,
                    'Guide': 6,
                    'Trip': 14,
                    'Reservation': 15,
                    'TripGuides': 28,
                    'Paddling': 9
                }
                
                verification_success = True
                
                for table_name, min_records in expected_tables.items():
                    # Check if table exists
                    cursor.execute("""
                        SELECT name FROM sqlite_master 
                        WHERE type='table' AND name=?
                    """, (table_name,))
                    
                    if not cursor.fetchone():
                        print(f"❌ Table '{table_name}' not found")
                        verification_success = False
                        continue
                    
                    # Check record count
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    actual_count = cursor.fetchone()[0]
                    
                    if actual_count >= min_records:
                        print(f"✅ {table_name}: {actual_count} records")
                    else:
                        print(f"❌ {table_name}: {actual_count} records (expected at least {min_records})")
                        verification_success = False
                
                # Verify foreign key relationships
                print("\n🔗 Verifying Foreign Key Relationships:")
                
                # Test reservation-customer relationship
                cursor.execute("""
                    SELECT COUNT(*) FROM Reservation r
                    LEFT JOIN Customer c ON r.CustomerNum = c.CustomerNum
                    WHERE c.CustomerNum IS NULL
                """)
                orphaned_reservations = cursor.fetchone()[0]
                
                if orphaned_reservations == 0:
                    print("✅ Reservation-Customer relationships intact")
                else:
                    print(f"❌ {orphaned_reservations} orphaned reservations found")
                    verification_success = False
                
                # Test tripguides-trip relationship
                cursor.execute("""
                    SELECT COUNT(*) FROM TripGuides tg
                    LEFT JOIN Trip t ON tg.TripID = t.TripID
                    WHERE t.TripID IS NULL
                """)
                orphaned_tripguides = cursor.fetchone()[0]
                
                if orphaned_tripguides == 0:
                    print("✅ TripGuides-Trip relationships intact")
                else:
                    print(f"❌ {orphaned_tripguides} orphaned trip guide assignments found")
                    verification_success = False
                
                return verification_success
                
        except sqlite3.Error as database_error:
            print(f"❌ Database error during verification: {database_error}")
            return False
            
        except Exception as general_error:
            print(f"❌ Unexpected error during verification: {general_error}")
            return False
    
    def display_database_summary(self) -> None:
        """
        Display a comprehensive summary of the database contents.
        
        This function provides an overview of all tables and their relationships
        for lab verification and demonstration purposes.
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                
                print("\n📊 Colonial Adventure Tours Database Summary")
                print("=" * 60)
                
                # Display table statistics
                tables = ['Customer', 'Guide', 'Trip', 'Reservation', 'TripGuides', 'Paddling']
                
                for table_name in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"📋 {table_name}: {count} records")
                
                # Display sample business insights
                print(f"\n💼 Business Insights:")
                
                # Total revenue calculation
                cursor.execute("""
                    SELECT 
                        SUM(TripPrice + OtherFees) as total_revenue,
                        COUNT(*) as total_reservations,
                        AVG(TripPrice + OtherFees) as avg_trip_cost
                    FROM Reservation
                """)
                revenue_data = cursor.fetchone()
                
                print(f"💰 Total Revenue: ${revenue_data[0]:.2f}")
                print(f"📝 Total Reservations: {revenue_data[1]}")
                print(f"📊 Average Trip Cost: ${revenue_data[2]:.2f}")
                
                # Most popular trip types
                cursor.execute("""
                    SELECT 
                        t.Type,
                        COUNT(*) as reservation_count
                    FROM Trip t
                    JOIN Reservation r ON t.TripID = r.TripID
                    GROUP BY t.Type
                    ORDER BY reservation_count DESC
                """)
                trip_types = cursor.fetchall()
                
                print(f"\n🏔️  Popular Trip Types:")
                for trip_type, count in trip_types:
                    print(f"   • {trip_type}: {count} reservations")
                
        except sqlite3.Error as database_error:
            print(f"❌ Database error displaying summary: {database_error}")
            
        except Exception as general_error:
            print(f"❌ Unexpected error displaying summary: {general_error}")

    def list_all_tables(self) -> List[str]:
        """
        Retrieve a list of all tables in the database.
        
        This function queries the SQLite master table to get all user-created
        tables, following proper database connection management practices.
        
        Returns:
            List[str]: List of table names, empty list if error occurs
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                
                # Query sqlite_master to get all table names
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                    ORDER BY name
                """)
                
                tables = [row[0] for row in cursor.fetchall()]
                
                print(f"\n📋 Tables in Colonial Adventure Database:")
                print("=" * 45)
                
                if tables:
                    for i, table_name in enumerate(tables, 1):
                        print(f"  {i}. {table_name}")
                else:
                    print("  No tables found in database")
                
                return tables
                
        except sqlite3.Error as database_error:
            print(f"❌ Database error listing tables: {database_error}")
            return []
            
        except Exception as general_error:
            print(f"❌ Unexpected error listing tables: {general_error}")
            return []

    def display_table_structure(self, table_name: str) -> bool:
        """
        Display the structure and schema of a specific table.
        
        This function shows column information, data types, constraints,
        and other table metadata for database design verification.
        
        Args:
            table_name (str): Name of the table to examine
            
        Returns:
            bool: True if structure displayed successfully, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                
                # Verify table exists
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name=?
                """, (table_name,))
                
                if not cursor.fetchone():
                    print(f"❌ Table '{table_name}' does not exist")
                    return False
                
                print(f"\n🏗️  Table Structure: {table_name}")
                print("=" * 50)
                
                # Get table schema using PRAGMA table_info
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                # Display column information in formatted table
                header = f"{'Column':<20} {'Type':<15} {'NotNull':<8} {'Default':<10} {'PK':<3}"
                print(header)
                print("-" * 60)
                
                for column in columns:
                    col_id = column[0]
                    col_name = column[1]
                    col_type = column[2]
                    not_null = "YES" if column[3] else "NO"
                    default_val = column[4] if column[4] is not None else "NULL"
                    primary_key = "YES" if column[5] else "NO"
                    
                    row = f"{col_name:<20} {col_type:<15} {not_null:<8} {str(default_val):<10} {primary_key:<3}"
                    print(row)
                
                # Get foreign key information
                cursor.execute(f"PRAGMA foreign_key_list({table_name})")
                foreign_keys = cursor.fetchall()
                
                if foreign_keys:
                    print(f"\n🔗 Foreign Key Constraints:")
                    for fk in foreign_keys:
                        print(f"   • {fk[3]} → {fk[2]}.{fk[4]}")
                
                # Get table record count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                record_count = cursor.fetchone()[0]
                print(f"\n📊 Total Records: {record_count}")
                
                return True
                
        except sqlite3.Error as database_error:
            print(f"❌ Database error displaying table structure: {database_error}")
            return False
            
        except Exception as general_error:
            print(f"❌ Unexpected error displaying table structure: {general_error}")
            return False

    def display_table_contents(self, table_name: str, limit: int = 10) -> bool:
        """
        Display the contents of a specific table with formatted output.
        
        This function shows table data in a readable format with proper
        column alignment and optional row limiting for large tables.
        
        Args:
            table_name (str): Name of the table to display
            limit (int): Maximum number of rows to display (default: 10)
            
        Returns:
            bool: True if contents displayed successfully, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                
                # Verify table exists
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name=?
                """, (table_name,))
                
                if not cursor.fetchone():
                    print(f"❌ Table '{table_name}' does not exist")
                    return False
                
                # Get column names for header
                cursor.execute(f"PRAGMA table_info({table_name})")
                column_info = cursor.fetchall()
                column_names = [col[1] for col in column_info]
                
                # Get table data with optional limit
                if limit > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT ?", (limit,))
                    print(f"\n📊 Table Contents: {table_name} (showing first {limit} rows)")
                else:
                    cursor.execute(f"SELECT * FROM {table_name}")
                    print(f"\n📊 Table Contents: {table_name} (all rows)")
                
                records = cursor.fetchall()
                
                print("=" * 80)
                
                if not records:
                    print(f"📝 No records found in table '{table_name}'")
                    return True
                
                # Calculate column widths for proper formatting
                col_widths = []
                for i, col_name in enumerate(column_names):
                    max_width = len(col_name)
                    for record in records:
                        cell_value = str(record[i]) if record[i] is not None else "NULL"
                        max_width = max(max_width, len(cell_value))
                    col_widths.append(min(max_width, 20))  # Cap width at 20 characters
                
                # Display header
                header_parts = []
                for i, col_name in enumerate(column_names):
                    header_parts.append(f"{col_name:<{col_widths[i]}}")
                print(" | ".join(header_parts))
                
                # Display separator line
                separator_parts = ["-" * width for width in col_widths]
                print("-|-".join(separator_parts))
                
                # Display data rows
                for record in records:
                    row_parts = []
                    for i, cell_value in enumerate(record):
                        display_value = str(cell_value) if cell_value is not None else "NULL"
                        # Truncate if too long
                        if len(display_value) > col_widths[i]:
                            display_value = display_value[:col_widths[i]-3] + "..."
                        row_parts.append(f"{display_value:<{col_widths[i]}}")
                    print(" | ".join(row_parts))
                
                # Display row count summary
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                total_count = cursor.fetchone()[0]
                
                print("=" * 80)
                if limit > 0 and total_count > limit:
                    print(f"Showing {len(records)} of {total_count} total records")
                else:
                    print(f"Total records: {total_count}")
                
                return True
                
        except sqlite3.Error as database_error:
            print(f"❌ Database error displaying table contents: {database_error}")
            return False
            
        except Exception as general_error:
            print(f"❌ Unexpected error displaying table contents: {general_error}")
            return False

    def interactive_table_viewer(self) -> None:
        """
        Interactive menu system for viewing database tables.
        
        This function provides a user-friendly interface for exploring
        the database structure and contents, following lab requirements
        for comprehensive database examination.
        """
        try:
            print("\n🔍 Interactive Table Viewer")
            print("=" * 35)
            
            while True:
                # Get list of available tables
                tables = self.list_all_tables()
                
                if not tables:
                    print("No tables available to view")
                    break
                
                print(f"\nOptions:")
                print(f"  0. Exit viewer")
                print(f"  1. View table structure")
                print(f"  2. View table contents")
                print(f"  3. View all table summaries")
                
                try:
                    choice = input("\nEnter your choice (0-3): ").strip()
                    
                    if choice == "0":
                        print("Exiting table viewer...")
                        break
                    
                    elif choice == "1":
                        # View table structure
                        print(f"\nSelect table to examine structure:")
                        for i, table_name in enumerate(tables, 1):
                            print(f"  {i}. {table_name}")
                        
                        table_choice = input(f"Enter table number (1-{len(tables)}): ").strip()
                        
                        try:
                            table_index = int(table_choice) - 1
                            if 0 <= table_index < len(tables):
                                selected_table = tables[table_index]
                                self.display_table_structure(selected_table)
                            else:
                                print("Invalid table selection")
                        except ValueError:
                            print("Please enter a valid number")
                    
                    elif choice == "2":
                        # View table contents
                        print(f"\nSelect table to view contents:")
                        for i, table_name in enumerate(tables, 1):
                            print(f"  {i}. {table_name}")
                        
                        table_choice = input(f"Enter table number (1-{len(tables)}): ").strip()
                        
                        try:
                            table_index = int(table_choice) - 1
                            if 0 <= table_index < len(tables):
                                selected_table = tables[table_index]
                                
                                # Ask for row limit
                                limit_input = input("Enter max rows to display (press Enter for all): ").strip()
                                limit = int(limit_input) if limit_input.isdigit() else 0
                                
                                self.display_table_contents(selected_table, limit)
                            else:
                                print("Invalid table selection")
                        except ValueError:
                            print("Please enter a valid number")
                    
                    elif choice == "3":
                        # View all table summaries
                        print(f"\n📋 All Table Summaries:")
                        for table_name in tables:
                            print(f"\n{'='*20} {table_name} {'='*20}")
                            self.display_table_structure(table_name)
                            self.display_table_contents(table_name, 5)  # Show first 5 rows
                    
                    else:
                        print("Invalid choice. Please enter 0-3.")
                
                except KeyboardInterrupt:
                    print("\nViewer interrupted by user")
                    break
                
                # Ask if user wants to continue
                continue_choice = input("\nPress Enter to continue or 'q' to quit: ").strip().lower()
                if continue_choice == 'q':
                    break
                    
        except Exception as general_error:
            print(f"❌ Error in interactive viewer: {general_error}")

# Add enhanced test function for table viewing
def test_table_viewing():
    """
    Test function for table viewing functionality.
    
    This function demonstrates all table viewing capabilities
    following CPE106L lab requirements for database exploration.
    """
    print("🧪 Testing Table Viewing Functionality")
    print("=" * 40)
    
    # Initialize database manager
    db_manager = ColonialDatabaseManager()
    
    # Ensure database exists with data
    if not os.path.exists(db_manager.db_path):
        print("Database not found. Setting up database first...")
        if not db_manager.execute_sql_script():
            print("❌ Failed to set up database")
            return False
    
    # Test listing tables
    print("\n1️⃣ Testing table listing...")
    tables = db_manager.list_all_tables()
    
    # Test viewing table structures
    print("\n2️⃣ Testing table structure display...")
    if tables:
        for table_name in tables[:3]:  # Show first 3 tables
            db_manager.display_table_structure(table_name)
    
    # Test viewing table contents
    print("\n3️⃣ Testing table contents display...")
    if tables:
        for table_name in tables[:2]:  # Show first 2 tables
            db_manager.display_table_contents(table_name, 3)  # Show 3 rows each
    
    print("\n✅ Table viewing tests completed")
    return True

# Update main execution to include table viewing options
def main():
    """
    Main function with comprehensive database management options.
    
    This function provides a complete interface for database setup,
    verification, and table viewing following lab requirements.
    """
    print("🏞️  CPE106L Lab 5 - Colonial Adventure Database Manager")
    print("=" * 60)
    print("Available operations:")
    print("  1. Set up database (execute SQL script)")
    print("  2. Verify database integrity")
    print("  3. Display database summary")
    print("  4. Interactive table viewer")
    print("  5. Test table viewing functionality")
    print("  6. List all tables")
    
    try:
        choice = input("\nEnter your choice (1-6): ").strip()
        
        db_manager = ColonialDatabaseManager()
        
        if choice == "1":
            setup_colonial_database()
        elif choice == "2":
            db_manager.verify_database_integrity()
        elif choice == "3":
            db_manager.display_database_summary()
        elif choice == "4":
            db_manager.interactive_table_viewer()
        elif choice == "5":
            test_table_viewing()
        elif choice == "6":
            db_manager.list_all_tables()
        else:
            print("Invalid choice. Running database setup by default.")
            setup_colonial_database()
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as error:
        print(f"\nUnexpected error: {error}")

if __name__ == "__main__":
    main()