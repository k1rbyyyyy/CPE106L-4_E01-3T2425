-- CPE106L Laboratory 5 - Colonial Adventure Tours Database
-- SQLite-compatible script for DB Browser execution
-- Original SQL Server script revised for SQLite compatibility

-- =============================================================================
-- COLONIAL ADVENTURE TOURS DATABASE SCHEMA
-- =============================================================================
-- This script creates six tables and populates them with sample data
-- Tables: Customer, Guide, Trip, Reservation, TripGuides, Paddling

-- Clean up existing tables (if any) for fresh start
-- Note: DROP TABLE IF EXISTS prevents errors if tables don't exist
DROP TABLE IF EXISTS TripGuides;
DROP TABLE IF EXISTS Reservation; 
DROP TABLE IF EXISTS Paddling;
DROP TABLE IF EXISTS Trip;
DROP TABLE IF EXISTS Guide;
DROP TABLE IF EXISTS Customer;

-- =============================================================================
-- TABLE 1: Customer
-- =============================================================================
-- Stores customer information for adventure trip bookings
CREATE TABLE Customer (
    CustomerNum INTEGER PRIMARY KEY,
    CustomerName VARCHAR(35) NOT NULL,
    Address VARCHAR(35),
    City VARCHAR(20),
    State CHAR(2),
    PostalCode CHAR(5),
    Phone CHAR(12)
);

-- Insert sample customer data
INSERT INTO Customer (CustomerNum, CustomerName, Address, City, State, PostalCode, Phone) VALUES
(101, 'Northwind Traders', '125 Main St', 'Harrisburg', 'PA', '17201', '717-555-0134'),
(102, 'Paris Specialty', '987 Pine Rd', 'Bath', 'ME', '04530', '207-555-0167'),
(103, 'Hanari Carnes', '456 Oak Ave', 'Jackson', 'WY', '83001', '307-555-0145'),
(104, 'Toms Spezialitäten', '789 Elm St', 'Bozeman', 'MT', '59715', '406-555-0112'),
(105, 'Rattlesnake Canyon', '321 Cedar Ln', 'Bozeman', 'MT', '59718', '406-555-0174'),
(106, 'Old World Delicatessen', '654 Maple Dr', 'Seattle', 'WA', '98104', '206-555-0138'),
(107, 'The Cracker Box', '147 Birch Way', 'Centralia', 'WA', '98531', '360-555-0156'),
(108, 'White Clover Markets', '258 Spruce St', 'White Salmon', 'WA', '98672', '509-555-0129'),
(109, 'Trails Head Outfitters', '369 Aspen Ct', 'Powell', 'WY', '82435', '307-555-0183');

-- =============================================================================
-- TABLE 2: Guide
-- =============================================================================
-- Stores information about tour guides
CREATE TABLE Guide (
    GuideNum INTEGER PRIMARY KEY,
    LastName VARCHAR(15) NOT NULL,
    FirstName VARCHAR(15) NOT NULL,
    Address VARCHAR(35),
    City VARCHAR(20),
    State CHAR(2),
    PostalCode CHAR(5),
    Phone CHAR(12),
    HireDate DATE
);

-- Insert sample guide data
INSERT INTO Guide (GuideNum, LastName, FirstName, Address, City, State, PostalCode, Phone, HireDate) VALUES
(10, 'Devon', 'Bill', '1925 Rocky Road', 'Cody', 'WY', '82414', '307-555-7989', '2019-06-05'),
(11, 'Unser', 'Susan', '2442 Aspen Street', 'Dubois', 'WY', '82513', '307-555-8744', '2020-05-30'),
(12, 'Kiley', 'Darnell', '8787 Moose Head Drive', 'Lander', 'WY', '82520', '307-555-2285', '2018-04-15'),
(13, 'Marmon', 'Kyle', '7787 Eagle Drive', 'Lander', 'WY', '82520', '307-555-0187', '2020-08-11'),
(14, 'Kelly', 'Samuel', '334 Badger Lane', 'Worland', 'WY', '82401', '307-555-5748', '2021-03-22'),
(15, 'Boyers', 'Rita', '1414 Bighorn Blvd', 'Thermopolis', 'WY', '82443', '307-555-4871', '2019-11-18');

-- =============================================================================
-- TABLE 3: Trip
-- =============================================================================
-- Stores adventure trip information
CREATE TABLE Trip (
    TripID INTEGER PRIMARY KEY,
    TripName VARCHAR(75) NOT NULL,
    StartLocation VARCHAR(50),
    State CHAR(2),
    Distance INTEGER,
    MaxGrpSize INTEGER,
    Type VARCHAR(25),
    Season VARCHAR(15)
);

-- Insert sample trip data
INSERT INTO Trip (TripID, TripName, StartLocation, State, Distance, MaxGrpSize, Type, Season) VALUES
(1, 'Aramus', 'Buffalo', 'WY', 5, 6, 'Hiking', 'Summer'),
(2, 'Beartooth', 'Yellowstone', 'WY', 17, 10, 'Hiking', 'Late Spring'),
(3, 'Woodrat', 'Lander', 'WY', 5, 8, 'Hiking', 'Summer'),
(4, 'Gila Monster', 'Worland', 'WY', 10, 8, 'Hiking', 'Late Spring'),
(5, 'Sulphur', 'Thermopolis', 'WY', 12, 15, 'Hiking', 'Early Fall'),
(21, 'Blackfoot River', 'Glacier Park', 'MT', 3, 4, 'Paddling', 'Summer'),
(22, 'Flathead River', 'Glacier Park', 'MT', 10, 8, 'Paddling', 'Summer'),
(23, 'Missouri River', 'Three Forks', 'MT', 4, 12, 'Paddling', 'Summer'),
(24, 'Salmon River', 'Riggins', 'ID', 7, 6, 'Paddling', 'Late Spring'),
(25, 'Snake River', 'Jackson', 'WY', 3, 8, 'Paddling', 'Summer'),
(26, 'Green River', 'Vernal', 'UT', 6, 10, 'Paddling', 'Late Spring'),
(27, 'Dolores River', 'Moab', 'UT', 15, 8, 'Paddling', 'Early Fall'),
(28, 'Buffalo River', 'Rush', 'AR', 4, 6, 'Paddling', 'Late Spring'),
(29, 'Big Piney', 'Fort Smith', 'AR', 2, 4, 'Paddling', 'Summer');

-- =============================================================================
-- TABLE 4: Reservation
-- =============================================================================
-- Stores customer trip reservations with pricing information
CREATE TABLE Reservation (
    ReservationID INTEGER PRIMARY KEY,
    TripID INTEGER NOT NULL,
    TripDate DATE,
    NumPersons INTEGER,
    TripPrice DECIMAL(6,2),
    OtherFees DECIMAL(6,2),
    CustomerNum INTEGER NOT NULL,
    FOREIGN KEY (TripID) REFERENCES Trip(TripID),
    FOREIGN KEY (CustomerNum) REFERENCES Customer(CustomerNum)
);

-- Insert sample reservation data
INSERT INTO Reservation (ReservationID, TripID, TripDate, NumPersons, TripPrice, OtherFees, CustomerNum) VALUES
(1001, 1, '2024-05-16', 2, 55.00, 4.50, 101),
(1002, 2, '2024-06-02', 3, 90.00, 8.50, 102),
(1003, 1, '2024-06-09', 1, 55.00, 4.50, 103),
(1004, 3, '2024-06-16', 2, 45.00, 6.75, 104),
(1005, 2, '2024-06-23', 4, 90.00, 8.50, 105),
(1006, 4, '2024-06-30', 6, 80.00, 12.20, 106),
(1007, 5, '2024-07-07', 8, 110.00, 13.25, 107),
(1008, 21, '2024-07-14', 3, 100.00, 18.00, 108),
(1009, 22, '2024-07-21', 5, 280.00, 32.50, 109),
(1010, 23, '2024-07-28', 2, 140.00, 17.25, 101),
(1011, 24, '2024-08-04', 4, 195.00, 26.40, 102),
(1012, 25, '2024-08-11', 6, 105.00, 15.75, 103),
(1013, 26, '2024-08-18', 8, 210.00, 28.80, 104),
(1014, 27, '2024-08-25', 3, 420.00, 56.25, 105),
(1015, 28, '2024-09-01', 4, 140.00, 17.25, 106);

-- =============================================================================
-- TABLE 5: TripGuides
-- =============================================================================
-- Junction table linking trips with their assigned guides (many-to-many relationship)
CREATE TABLE TripGuides (
    TripID INTEGER NOT NULL,
    GuideNum INTEGER NOT NULL,
    PRIMARY KEY (TripID, GuideNum),
    FOREIGN KEY (TripID) REFERENCES Trip(TripID),
    FOREIGN KEY (GuideNum) REFERENCES Guide(GuideNum)
);

-- Insert trip-guide assignments
INSERT INTO TripGuides (TripID, GuideNum) VALUES
(1, 10),
(1, 11),
(2, 10),
(2, 12),
(3, 11),
(3, 13),
(4, 12),
(4, 14),
(5, 13),
(5, 15),
(21, 10),
(21, 14),
(22, 11),
(22, 15),
(23, 12),
(23, 10),
(24, 13),
(24, 11),
(25, 14),
(25, 12),
(26, 15),
(26, 13),
(27, 10),
(27, 14),
(28, 11),
(28, 15),
(29, 12),
(29, 13);

-- =============================================================================
-- TABLE 6: Paddling
-- =============================================================================
-- Specialized table for paddling trips with specific equipment requirements
CREATE TABLE Paddling (
    TripID INTEGER PRIMARY KEY,
    RiverRating VARCHAR(5),
    LifeJacketReq CHAR(1) CHECK (LifeJacketReq IN ('Y', 'N')),
    FOREIGN KEY (TripID) REFERENCES Trip(TripID)
);

-- Insert paddling-specific data for water-based trips
INSERT INTO Paddling (TripID, RiverRating, LifeJacketReq) VALUES
(21, 'I', 'Y'),
(22, 'II', 'Y'),
(23, 'I', 'Y'),
(24, 'III', 'Y'),
(25, 'I', 'Y'),
(26, 'II', 'Y'),
(27, 'IV', 'Y'),
(28, 'II', 'Y'),
(29, 'I', 'Y');

-- =============================================================================
-- VERIFICATION QUERIES
-- =============================================================================
-- Use these queries to verify the data was inserted correctly

-- Display record counts for each table
SELECT 'Customer' as TableName, COUNT(*) as RecordCount FROM Customer
UNION ALL
SELECT 'Guide' as TableName, COUNT(*) as RecordCount FROM Guide
UNION ALL
SELECT 'Trip' as TableName, COUNT(*) as RecordCount FROM Trip
UNION ALL
SELECT 'Reservation' as TableName, COUNT(*) as RecordCount FROM Reservation
UNION ALL
SELECT 'TripGuides' as TableName, COUNT(*) as RecordCount FROM TripGuides
UNION ALL
SELECT 'Paddling' as TableName, COUNT(*) as RecordCount FROM Paddling;

-- =============================================================================
-- ADDITIONAL VERIFICATION VIEWS
-- =============================================================================
-- These views demonstrate relationships between tables


    c.CustomerName,
    t.TripName,
    r.TripDate,
    r.NumPersons,
    r.TripPrice + r.OtherFees as TotalCost
FROM Customer c
JOIN Reservation r ON c.CustomerNum = r.CustomerNum
JOIN Trip t ON r.TripID = t.TripID
ORDER BY c.CustomerName, r.TripDate;

-- Trip assignments with guide information
CREATE VIEW TripAssignments AS
SELECT 
    t.TripName,
    t.Type,
    t.Season,
    g.FirstName || ' ' || g.LastName as GuideName,
    g.Phone as GuidePhone
FROM Trip t
JOIN TripGuides tg ON t.TripID = tg.TripID
JOIN Guide g ON tg.GuideNum = g.GuideNum
ORDER BY t.TripName, g.LastName;

-- Paddling trips with safety requirements
CREATE VIEW PaddlingTrips AS
SELECT 
    t.TripName,
    t.StartLocation,
    t.State,
    t.Distance,
    p.RiverRating,
    CASE 
        WHEN p.LifeJacketReq = 'Y' THEN 'Required' 
        ELSE 'Not Required' 
    END as LifeJacketStatus
FROM Trip t
JOIN Paddling p ON t.TripID = p.TripID
ORDER BY p.RiverRating, t.TripName;

-- =============================================================================
-- SUCCESS MESSAGE
-- =============================================================================
-- This will be the last output when script completes successfully
SELECT 'Colonial Adventure Tours database created successfully!' as Status,
       'All 6 tables created and populated with sample data' as Details;
	   
	   -- List all tables
.tables

-- View specific table
SELECT * FROM Customer LIMIT 5;
SELECT * FROM Trip WHERE Type = 'Hiking';
SELECT * FROM Reservation ORDER BY TripDate;