# CPE106L Laboratory 5 - Database Management System

## Colonial Adventure Tours Database Lab

This laboratory assignment focuses on database design, table creation, data manipulation, and SQL queries using SQLite with Python.

### 🎯 Learning Objectives

- Understand database table creation and structure
- Practice SQL data types and constraints
- Learn data insertion and deletion operations
- Master database queries and joins
- Analyze data using aggregate functions
- Implement database operations using Python and SQLite

### 📁 Project Structure

```
lab5/
├── main.py                     # Main runner script
├── prelab/
│   └── prelab_activities.py    # PreLab exercises
├── inlab/
│   └── inlab_activities.py     # InLab exercises and queries
├── database/
│   ├── schema.sql              # Database schema definition
│   ├── sample_data.sql         # Sample data insertion
│   └── colonial_adventure.db   # SQLite database (created when run)
├── .github/
│   └── copilot-instructions.md # Copilot coding guidelines
└── README.md                   # This file
```

### 🚀 Quick Start

1. **Run the main program:**
   ```bash
   python main.py
   ```

2. **Choose from the menu:**
   - Option 1: PreLab Activities
   - Option 2: InLab Activities  
   - Option 3: Both PreLab and InLab
   - Option 4: Exit

### 📋 PreLab Activities

**Objective:** Learn basic table operations with the ADVENTURE_TRIP table

#### Activity A: Table Creation
- Create the ADVENTURE_TRIP table with proper data types
- VARCHAR for text fields, NUMBER for numeric fields
- Display table structure and characteristics

#### Activity B: Data Insertion
- Insert sample record: Jay Peak trip
- Trip ID: 45, Location: Jay, VT
- Distance: 8 miles, Max group: 8 people
- Type: Hiking, Season: Summer
- Display table contents

#### Activity C: Table Deletion
- Remove the ADVENTURE_TRIP table
- Verify successful deletion

### 🔬 InLab Activities

**Objective:** Work with complete database system and complex queries

#### Activity D: Database Setup
- Create all six tables: Customer, Guide, Trip, Reservation, Trip_Guides
- Insert comprehensive sample data
- Establish foreign key relationships

#### Database Tables:

1. **Customer** - Customer information and contact details
2. **Guide** - Tour guide information and hire dates
3. **Trip** - Trip details, locations, and specifications
4. **Reservation** - Customer trip bookings and pricing
5. **Trip_Guides** - Many-to-many relationship between trips and guides

#### Query Operations:
- Display all table contents
- Search customers by city
- Join trips with assigned guides
- Analyze customer reservations
- Generate trip statistics and reports

### 🗄️ Database Schema

#### Key Relationships:
- Customer ➝ Reservation (1:Many)
- Trip ➝ Reservation (1:Many)  
- Trip ↔ Guide (Many:Many via Trip_Guides)

#### Sample Data Includes:
- 26 Customers across New England states
- 9 Professional tour guides
- 18 Different trips (hiking and biking)
- 20 Customer reservations
- Guide assignments for each trip

### 🛠️ Technical Requirements

- **Python 3.7+**
- **SQLite3** (included with Python)
- **VS Code** with Python extension (recommended)

### 📊 Example Queries and Operations

The lab includes examples of:
- **Basic CRUD operations** (Create, Read, Update, Delete)
- **JOIN queries** across multiple tables
- **Aggregate functions** (COUNT, AVG, SUM)
- **GROUP BY** operations for data analysis
- **Filtering and sorting** with WHERE and ORDER BY
- **Subqueries** for complex data retrieval

### 🎓 Skills Developed

- Database design principles
- SQL query construction
- Python database programming
- Data analysis and reporting
- Error handling and validation
- Database relationship management

### 🔍 Sample Queries Demonstrated

```sql
-- Customer reservations with trip details
SELECT c.CUSTOMER_NAME, t.TRIP_NAME, r.TRIP_DATE, r.TOTAL_COST
FROM Customer c
JOIN Reservation r ON c.CUSTOMER_NUM = r.CUSTOMER_NUM
JOIN Trip t ON r.TRIP_ID = t.TRIP_ID;

-- Trip statistics by season
SELECT SEASON, AVG(DISTANCE), COUNT(*)
FROM Trip
GROUP BY SEASON;

-- Guides with their assigned trips
SELECT g.FIRST_NAME, g.LAST_NAME, COUNT(tg.TRIP_ID)
FROM Guide g
LEFT JOIN Trip_Guides tg ON g.GUIDE_NUM = tg.GUIDE_NUM
GROUP BY g.GUIDE_NUM;
```

### 📝 Assessment Criteria

- Correct table creation with appropriate data types
- Successful data insertion and manipulation
- Proper use of SQL constraints and relationships
- Effective query construction and optimization
- Clear understanding of database normalization
- Professional code documentation and error handling

### 🏆 Extended Learning

After completing the basic lab:
- Try creating additional complex queries
- Implement data validation functions
- Add error handling for edge cases
- Create database backup and restore functions
- Design additional tables for expanded functionality

### 📞 Support

For questions about this lab:
- Review the SQL documentation
- Check Python sqlite3 module documentation
- Consult database design best practices
- Review the sample code and comments

---

**Course:** CPE106L - Computer Engineering Laboratory  
**Lab:** Laboratory 5 - Database Management System  
**Group:** Group 2  
**Database:** Colonial Adventure Tours
