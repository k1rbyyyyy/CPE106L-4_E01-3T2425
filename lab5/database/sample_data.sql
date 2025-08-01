-- CPE106L Laboratory 5 - Sample Data
-- Insert statements for all tables based on the provided data

-- Insert Customer data
INSERT INTO Customer (CUSTOMER_NUM, CUSTOMER_NAME, ADDRESS, CITY, STATE, POSTAL_CODE, PHONE) VALUES
(101, 'Northwind', '1236 N. 14th St. Apt 14', 'Undervaney', 'NH', '03451', '603-555-7620'),
(102, 'Brookstone', '2392 South St. Apt 3', 'Springfield', 'MA', '01101', '413-555-3097'),
(103, 'Outdoor Resort', '1395 Main St. #8', 'East Hartford', 'CT', '06108', '860-555-0703'),
(104, 'Wilson', '1048 Green Street', 'Cowell', 'VT', '05636', '802-555-3475'),
(105, 'Walker', '345 Lower Ave.', 'Wolcott', 'VT', '05680', '802-555-9921'),
(106, 'Sesward', '156 Scholar Dr.', 'Johnston', 'RI', '02919', '401-555-4848'),
(107, 'Marchand', 'Club', '78 Cross Rd.', 'Bath', 'NH', '03740', '603-555-0546'),
(108, 'Kiley', 'Leach', '22 River Stop Dr.', 'Belmont', 'MA', '02478', '617-555-8871'),
(109, 'Caron', 'Jean Luc', '10 Greanfield St.', 'Rome', 'ME', '04963', '207-555-0044'),
(110, 'Welch', 'Bertide', '45 Granite St.', 'Rome', 'ME', '04963', '207-555-7511'),
(112, 'Jones', 'Laura', '178 Highland Ave.', 'Somersville', 'MA', '02143', '617-555-6216'),
(115, 'Kurrat', 'Adam', '1295 Ocean Walk', 'Ocean City', 'NJ', '08226', '609-555-5530'),
(116, 'Markamal', 'Siri', '7 Cherry Blossom St. Waym', 'NH', '03168', '617-555-6665'),
(117, 'Cheximent', 'Gregory', '10 Ann Ledge Ln.', 'Londonderry', 'VT', '05148', '802-555-5050'),
(119, 'Gernandez', 'Sadie', '24 Stump Rd.', 'Athens', 'NH', '03819', '207-555-4507'),
(121, 'Kahlmann', 'Kelly', '10 Old Bath Ln.', 'Cambridge', 'VT', '05444', '802-555-3412'),
(122, 'Jefferson', 'Orlagh', '150 South St. Apt 17', 'Manchester', 'NH', '03101', '603-555-3474'),
(123, 'Smilarsky', 'Greg', '45 Pine St.', 'Acton', 'MA', '01720', '508-555-8979'),
(124, 'Rums', 'Karen', '12 Foster St.', 'South Windsor', 'CT', '06074', '860-555-5512'),
(125, 'Strysko', 'Darya', '13 Piedatyle St.', 'Akins', 'CT', '06279', '203-555-2987'),
(126, 'Brown', 'Brigitte', '154 Central St.', 'Vernon', 'CT', '06066', '860-555-3214');

-- Insert Guide data
INSERT INTO Guide (GUIDE_NUM, LAST_NAME, FIRST_NAME, ADDRESS, CITY, STATE, POSTAL_CODE, PHONE_NUM, HIRE_DATE) VALUES
(001, 'Abrams', 'Miles', '54 Quest Ave.', 'Williamsburg', 'MA', '01096', '617-555-6032', '2022-05-15'),
(002, 'Boyers', 'Rita', '140 Oakton St.', 'Jaffrey', 'NH', '03452', '603-555-2134', '2021-03-10'),
(003, 'Devon', 'Harley', '25 Old Maple Rd.', 'Sunderland', 'MA', '01375', '413-555-7767', '2020-08-22'),
(004, 'Kiley', 'Susan', '387 Oakton St.', 'Jaffrey', 'NH', '03452', '603-555-2200', '2019-04-15'),
(005, 'Merville', 'Jeremy', '8 Johnson Ave.', 'Franconia', 'NH', '03580', '603-555-9000', '2023-01-12'),
(006, 'Routen', 'Hal', '35 Woodstream Rd.', 'Springfield', 'MA', '01101', '413-555-8543', '2021-07-08'),
(007, 'Stevens', 'Carl', '12 Beevers St.', 'Mount Desert', 'ME', '04660', '207-555-8030', '2020-12-03'),
(008, 'Tyler', 'Sam', '15 Riverwalk Way', 'Townshend', 'VT', '05353', '802-555-3339', '2022-09-18'),
(009, 'Unser', 'Lissa', '132 Riverside St.', 'Danbury', 'CT', '06810', '203-555-8734', '2019-11-25');

-- Insert Trip data
INSERT INTO Trip (TRIP_ID, TRIP_NAME, START_LOCATION, STATE, DISTANCE, MAX_GRP_SIZE, TYPE, SEASON) VALUES
(1, 'Arethusa Falls', 'Harts Location', 'NH', 5, 10, 'Hiking', 'Summer'),
(2, 'Mt Washington North Peak', 'Washington-field', 'VT', 5, 8, 'Hiking', 'Late Spring'),
(3, 'Mt Mansfield', 'Stowe Beat', 'VT', 4, 3, 'Hiking', 'Early Fall'),
(4, 'Marsh-Billings', 'Woodstock', 'VT', 6, 8, 'Hiking', 'Late Spring'),
(5, 'Bradlord Mountain', 'North Brady', 'NH', 5, 10, 'Hiking', 'Early Spring'),
(6, 'Sante Hill', 'Townshend Over', 'VT', 5, 12, 'Hiking', 'Early Fall'),
(7, 'Sterling Pond', 'Stowe', 'VT', 3, 15, 'Hiking', 'Summer'),
(8, 'Lye Brook Falls', 'Manchester', 'VT', 6, 15, 'Hiking', 'Early Spring'),
(9, 'Sunset Rock', 'Somerset', 'NH', 6, 12, 'Hiking', 'Summer'),
(10, 'Mt Chocorua', 'Bartbridge', 'NH', 7, 14, 'Hiking', 'Early Fall'),
(11, 'Cadillac Mountain', 'Bar Harbor', 'ME', 1, 5, 'Hiking', 'Spring'),
(12, 'Mt Jackson', 'Bartbridge', 'NH', 7, 12, 'Hiking', 'Early Fall'),
(13, 'Winnepesaukee Trail', 'Gonic', 'NH', 1, 8, 'Biking', 'Summer'),
(14, 'Cherry Pond', 'Whitefield', 'NH', 4, 14, 'Biking', 'Spring'),
(15, 'North Conway Trail', 'New London', 'NH', 7, 10, 'Biking', 'Early Fall'),
(16, 'East Pond Loop', 'Thornton', 'NH', 8, 12, 'Biking', 'Summer'),
(17, 'Welch-Dickey Loop', 'Thornton', 'NH', 5, 5, 'Hiking', 'Summer'),
(18, 'Mount Hale', 'Zealand', 'NH', 9, 12, 'Hiking', 'Summer');

-- Insert Reservation data
INSERT INTO Reservation (RESERVATION_ID, TRIP_ID, TRIP_DATE, NUM_PERSONS, TRIP_PRICE, OTHER_FEES, CUSTOMER_NUM) VALUES
(1000001, 40, '2025-03-16', 2, 55, 0, 101),
(1000002, 23, '2025-03-16', 5, 55, 0, 102),
(1000003, 35, '2025-03-16', 1, 45, 0, 103),
(1000004, 40, '2025-03-16', 2, 55, 10, 104),
(1000005, 35, '2025-03-16', 5, 45, 0, 105),
(1000006, 52, '2025-03-16', 1, 80, 20, 106),
(1000007, 22, '2025-03-16', 8, 75, 10, 107),
(1000008, 24, '2025-03-16', 2, 35, 0, 108),
(1000009, 35, '2025-03-16', 4, 80, 40, 109),
(1000010, 2, '2025-03-16', 1, 35, 0, 102),
(1000011, 5, '2025-03-16', 3, 25, 0, 110),
(1000012, 1, '2025-03-16', 6, 55, 0, 119),
(1000013, 8, '2025-03-16', 1, 20, 0, 116),
(1000014, 10, '2025-03-16', 6, 40, 0, 119),
(1000015, 15, '2025-03-16', 1, 20, 0, 120),
(1000016, 11, '2025-03-16', 6, 75, 15, 121),
(1000017, 39, '2025-03-16', 3, 25, 5, 122),
(1000018, 28, '2025-03-16', 8, 85, 15, 126),
(1000019, 25, '2025-03-16', 2, 110, 25, 124),
(1000020, 28, '2025-03-16', 2, 35, 10, 124);

-- Insert Trip_Guides data (relationships between trips and guides)
INSERT INTO Trip_Guides (TRIP_ID, GUIDE_NUM) VALUES
(1, 001),
(2, 005),
(3, 001),
(4, 005),
(5, 006),
(6, 001),
(7, 002),
(8, 001),
(9, 006),
(10, 005),
(11, 006),
(12, 002),
(13, 001),
(14, 005),
(15, 002),
(16, 001),
(17, 001),
(18, 002);
