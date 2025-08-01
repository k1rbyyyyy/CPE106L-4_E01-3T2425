# CPE106L Laboratory 5 - InLab Activities
# Database Operations and Queries

import sqlite3
import os
from datetime import datetime

class ColonialAdventureDB:
    """
    Class to handle all database operations for Colonial Adventure Tours
    """
    
    def __init__(self):
        self.db_path = os.path.join('database', 'colonial_adventure.db')
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        """Ensure the database and tables exist"""
        if not os.path.exists(self.db_path):
            self.setup_database()
    
    def setup_database(self):
        """
        InLab Activity D: Open the script file (SQLServerColonial.sql) to create the six tables 
        and add records to the tables. Revise the script file so that it can be run in the DB Browser.
        """
        print("Setting up Colonial Adventure database...")
        
        # Read and execute schema
        schema_path = os.path.join('database', 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            with sqlite3.connect(self.db_path) as conn:
                # Split and execute each statement
                statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
                for statement in statements:
                    try:
                        conn.execute(statement)
                    except sqlite3.Error as e:
                        print(f"Error executing statement: {e}")
                conn.commit()
        
        # Read and execute sample data
        data_path = os.path.join('database', 'sample_data.sql')
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                data_sql = f.read()
            
            with sqlite3.connect(self.db_path) as conn:
                # Split and execute each statement
                statements = [stmt.strip() for stmt in data_sql.split(';') if stmt.strip()]
                for statement in statements:
                    try:
                        conn.execute(statement)
                    except sqlite3.Error as e:
                        print(f"Error executing statement: {e}")
                conn.commit()
        
        print("Database setup completed!")
    
    def display_table(self, table_name):
        """Display all records from a specified table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name};")
                records = cursor.fetchall()
                
                # Get column names
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = [col[1] for col in cursor.fetchall()]
                
                print(f"\n{table_name} Table Contents:")
                print("-" * (len(table_name) + 16))
                
                # Print headers
                header = " | ".join(f"{col:<12}" for col in columns)
                print(header)
                print("-" * len(header))
                
                # Print records
                for record in records:
                    row = " | ".join(f"{str(val):<12}" if val is not None else f"{'NULL':<12}" for val in record)
                    print(row)
                
                print(f"\nTotal records: {len(records)}")
                
        except sqlite3.Error as e:
            print(f"Error displaying {table_name}: {e}")
    
    def search_customers_by_city(self, city):
        """
        Search for customers in a specific city
        Example query operation for the lab
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT CUSTOMER_NUM, CUSTOMER_NAME, ADDRESS, CITY, STATE, PHONE 
                    FROM Customer 
                    WHERE CITY = ?
                """, (city,))
                
                records = cursor.fetchall()
                
                print(f"\nCustomers in {city}:")
                print("-" * 40)
                if records:
                    for record in records:
                        print(f"ID: {record[0]}, Name: {record[1]}")
                        print(f"Address: {record[2]}, {record[3]}, {record[4]}")
                        print(f"Phone: {record[5]}")
                        print("-" * 40)
                else:
                    print("No customers found in this city.")
                    
        except sqlite3.Error as e:
            print(f"Error searching customers: {e}")
    
    def get_trip_details_with_guides(self):
        """
        InLab Query: Get trip details along with their assigned guides
        This demonstrates JOIN operations between multiple tables
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        t.TRIP_ID,
                        t.TRIP_NAME,
                        t.START_LOCATION,
                        t.STATE,
                        t.DISTANCE,
                        t.TYPE,
                        t.SEASON,
                        g.FIRST_NAME || ' ' || g.LAST_NAME as GUIDE_NAME
                    FROM Trip t
                    LEFT JOIN Trip_Guides tg ON t.TRIP_ID = tg.TRIP_ID
                    LEFT JOIN Guide g ON tg.GUIDE_NUM = g.GUIDE_NUM
                    ORDER BY t.TRIP_ID;
                """)
                
                records = cursor.fetchall()
                
                print("\nTrip Details with Assigned Guides:")
                print("=" * 80)
                
                current_trip = None
                for record in records:
                    if record[0] != current_trip:
                        current_trip = record[0]
                        print(f"\nTrip ID: {record[0]} - {record[1]}")
                        print(f"Location: {record[2]}, {record[3]}")
                        print(f"Distance: {record[4]} miles | Type: {record[5]} | Season: {record[6]}")
                        print(f"Guide: {record[7] if record[7] else 'No guide assigned'}")
                    else:
                        print(f"Additional Guide: {record[7]}")
                        
        except sqlite3.Error as e:
            print(f"Error getting trip details: {e}")
    
    def get_customer_reservations(self):
        """
        InLab Query: Get customer reservations with trip information
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        c.CUSTOMER_NAME,
                        r.RESERVATION_ID,
                        t.TRIP_NAME,
                        r.TRIP_DATE,
                        r.NUM_PERSONS,
                        r.TRIP_PRICE,
                        r.OTHER_FEES,
                        (r.TRIP_PRICE + r.OTHER_FEES) as TOTAL_COST
                    FROM Customer c
                    JOIN Reservation r ON c.CUSTOMER_NUM = r.CUSTOMER_NUM
                    JOIN Trip t ON r.TRIP_ID = t.TRIP_ID
                    ORDER BY c.CUSTOMER_NAME, r.TRIP_DATE;
                """)
                
                records = cursor.fetchall()
                
                print("\nCustomer Reservations:")
                print("=" * 80)
                
                for record in records:
                    print(f"Customer: {record[0]}")
                    print(f"Reservation: {record[1]} | Trip: {record[2]}")
                    print(f"Date: {record[3]} | Persons: {record[4]}")
                    print(f"Trip Price: ${record[5]} | Other Fees: ${record[6]} | Total: ${record[7]}")
                    print("-" * 40)
                    
        except sqlite3.Error as e:
            print(f"Error getting customer reservations: {e}")
    
    def analyze_trip_statistics(self):
        """
        InLab Analysis: Generate statistics about trips
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Most popular trip types
                cursor.execute("""
                    SELECT TYPE, COUNT(*) as trip_count 
                    FROM Trip 
                    GROUP BY TYPE 
                    ORDER BY trip_count DESC;
                """)
                
                print("\nTrip Statistics:")
                print("=" * 40)
                print("Most Popular Trip Types:")
                for record in cursor.fetchall():
                    print(f"{record[0]}: {record[1]} trips")
                
                # Average distance by season
                cursor.execute("""
                    SELECT SEASON, AVG(DISTANCE) as avg_distance, COUNT(*) as trip_count
                    FROM Trip 
                    GROUP BY SEASON 
                    ORDER BY avg_distance DESC;
                """)
                
                print("\nAverage Distance by Season:")
                for record in cursor.fetchall():
                    print(f"{record[0]}: {record[1]:.1f} miles ({record[2]} trips)")
                
                # Guides with most trips
                cursor.execute("""
                    SELECT 
                        g.FIRST_NAME || ' ' || g.LAST_NAME as guide_name,
                        COUNT(tg.TRIP_ID) as trips_guided
                    FROM Guide g
                    LEFT JOIN Trip_Guides tg ON g.GUIDE_NUM = tg.GUIDE_NUM
                    GROUP BY g.GUIDE_NUM, guide_name
                    ORDER BY trips_guided DESC;
                """)
                
                print("\nGuides by Number of Trips:")
                for record in cursor.fetchall():
                    print(f"{record[0]}: {record[1]} trips")
                    
        except sqlite3.Error as e:
            print(f"Error analyzing trip statistics: {e}")

def run_inlab_activities():
    """
    Run all InLab activities
    """
    print("=" * 60)
    print("CPE106L Laboratory 5 - InLab Activities")
    print("=" * 60)
    
    # Initialize database
    db = ColonialAdventureDB()
    
    print("\n1. Displaying all tables...")
    tables = ['Customer', 'Guide', 'Trip', 'Reservation', 'Trip_Guides']
    
    for table in tables:
        db.display_table(table)
        input(f"\nPress Enter to continue to next table...")
    
    print("\n2. Searching customers by city...")
    db.search_customers_by_city('Jaffrey')
    
    print("\n3. Getting trip details with guides...")
    db.get_trip_details_with_guides()
    
    print("\n4. Getting customer reservations...")
    db.get_customer_reservations()
    
    print("\n5. Analyzing trip statistics...")
    db.analyze_trip_statistics()
    
    print("\n" + "=" * 60)
    print("InLab activities completed!")
    print("=" * 60)

if __name__ == "__main__":
    run_inlab_activities()
