"""
MatchWise Application Recording Script
====================================

This script provides a step-by-step recording guide for demonstrating
the MatchWise application's input/output processes and functionality.

Author: Generated for MatchWise Project
Date: July 29, 2025
"""

import time
from datetime import datetime

class MatchWiseRecordingScript:
    """
    A comprehensive recording script for demonstrating MatchWise application
    """
    
    def __init__(self):
        self.script_sections = []
        self.demo_data = {
            "users": [
                {"username": "alice_smith", "password": "password123", "name": "Alice Smith", "location": "Manila, Philippines", "skills": "Accounting"},
                {"username": "bob_jones", "password": "password123", "name": "Bob Jones", "location": "Quezon City, Philippines", "skills": "Programming"}
            ],
            "listings": [
                {"type": "request", "skill": "Accounting", "description": "Need help with tax preparation", "availability": "Mon 14-16"},
                {"type": "offer", "skill": "Accounting", "description": "Can help with bookkeeping and taxes", "availability": "Mon 15-17"}
            ]
        }
    
    def record_section_1_introduction(self):
        """
        RECORDING SECTION 1: Introduction and Overview
        """
        print("=" * 80)
        print("RECORDING SCRIPT - SECTION 1: INTRODUCTION")
        print("=" * 80)
        
        script = """
NARRATOR SCRIPT:
"Welcome to the MatchWise application demonstration. MatchWise is a skill-sharing 
platform that connects people who want to learn skills with those who can teach them.

Today, we'll demonstrate the complete input-output process, showing how users 
register, create listings, and find matches through our intelligent matching algorithm.

Let's start by examining the application architecture..."

SCREEN ACTIONS:
1. Show project folder structure
2. Highlight main components:
   - main.py (FastAPI backend)
   - login_ui.py (Login interface)
   - register_ui.py (Registration interface)  
   - flet_dashboard.py (Main dashboard)
   - matchwise.db (SQLite database)

TECHNICAL NOTES:
- Python-based application using Flet UI framework
- FastAPI REST API backend
- SQLite database for data persistence
- Google Maps API for location services
- Real-time matching algorithm with percentage scoring
        """
        
        print(script)
        return script
    
    def record_section_2_user_registration(self):
        """
        RECORDING SECTION 2: User Registration Process
        """
        print("\n" + "=" * 80)
        print("RECORDING SCRIPT - SECTION 2: USER REGISTRATION")
        print("=" * 80)
        
        script = """
NARRATOR SCRIPT:
"Let's begin with user registration. I'll show how new users create accounts
and how the system processes their information."

DEMO STEPS:

1. START APPLICATION
   Command: python login_ui.py
   
   SHOW ON SCREEN:
   - Login window appears
   - Clean, modern interface with Material Design
   - Username and password fields
   - "Create a new account" button

2. CLICK "Create a new account"
   
   INPUT DEMONSTRATION:
   - Full Name: "Alice Smith"
   - Username: "alice_smith" 
   - Password: "password123"
   - Confirm Password: "password123"
   - Location: "Manila, Philippines"
   - Skills: Select "Accounting" from dropdown
   
   EXPLAIN WHILE TYPING:
   "Notice the real-time validation - password confirmation must match,
   and we have 30+ skills to choose from including Programming, Cooking,
   Language Tutoring, and more."

3. CLICK "Register"
   
   BACKEND PROCESS (EXPLAIN):
   - System checks username uniqueness
   - Password gets hashed using SHA-256
   - Data inserted into SQLite database
   - Success response returned
   
   RESULT ON SCREEN:
   - "Registration successful!" message
   - Automatic redirect to login page

INPUT → PROCESSING → OUTPUT:
User Form Data → Validation & Hashing → Database Storage → Success Response
        """
        
        print(script)
        return script
    
    def record_section_3_user_login(self):
        """
        RECORDING SECTION 3: User Login Process  
        """
        print("\n" + "=" * 80)
        print("RECORDING SCRIPT - SECTION 3: USER LOGIN")
        print("=" * 80)
        
        script = """
NARRATOR SCRIPT:
"Now let's demonstrate the login process and see how the system authenticates users."

DEMO STEPS:

1. LOGIN WITH ALICE'S CREDENTIALS
   
   INPUT:
   - Username: "alice_smith"
   - Password: "password123"
   
   CLICK "Login"
   
   BACKEND PROCESS (EXPLAIN):
   "The system queries the database, retrieves the stored password hash,
   and compares it with the hashed input password for security."
   
   SQL QUERY SHOWN:
   SELECT * FROM users WHERE username = 'alice_smith'
   
   RESULT:
   - Authentication successful
   - User data retrieved (ID, name, location, skills)
   - Dashboard loads with personalized welcome

2. SHOW DASHBOARD INTERFACE
   
   POINT OUT FEATURES:
   - Welcome message: "Welcome, Alice Smith!"
   - Five main action buttons:
     * 🔍 View Matches
     * 📤 Create Listing  
     * 📋 My Listings
     * 📊 Browse All Listings
     * 🚪 Logout
   
   EXPLAIN NAVIGATION:
   "Single-window application - all features accessible from this dashboard.
   The interface updates dynamically without opening new windows."

INPUT → PROCESSING → OUTPUT:
Credentials → Database Authentication → User Session → Personalized Dashboard
        """
        
        print(script)
        return script
    
    def record_section_4_creating_listings(self):
        """
        RECORDING SECTION 4: Creating Listings
        """
        print("\n" + "=" * 80)
        print("RECORDING SCRIPT - SECTION 4: CREATING LISTINGS")
        print("=" * 80)
        
        script = """
NARRATOR SCRIPT:
"Let's create a skill request. Alice needs help with tax preparation."

DEMO STEPS:

1. CLICK "📤 Create Listing"
   
   FORM APPEARS WITH FIELDS:
   - "I want to..." dropdown (Offer/Request)
   - Skill dropdown (30+ options)
   - Description text area
   - Availability: Day, Start Hour, End Hour

2. FILL OUT REQUEST FORM
   
   INPUT DATA:
   - Type: "request"
   - Skill: "Accounting" 
   - Description: "Need help preparing my annual tax returns. First time doing it myself."
   - Day: "Monday"
   - Start Hour: "14" (2 PM)
   - End Hour: "16" (4 PM)
   
   EXPLAIN WHILE FILLING:
   "The availability system is flexible - users specify day and time ranges.
   Our matching algorithm will find overlapping schedules."

3. CLICK "📤 Submit"
   
   API CALL PROCESS:
   POST /listings/ with JSON payload:
   {
     "user_id": 1,
     "type": "request", 
     "skill": "Accounting",
     "availability": "Mon 14-16",
     "description": "Need help preparing my annual tax returns..."
   }
   
   RESULT:
   - "✅ Listing submitted successfully!" message
   - Listing stored in database with timestamp
   - Ready for matching algorithm

4. CREATE SECOND USER FOR DEMONSTRATION
   
   REGISTER BOB:
   - Name: "Bob Jones"
   - Username: "bob_jones"
   - Location: "Quezon City, Philippines" 
   - Skills: "Accounting"
   
   BOB CREATES OFFER:
   - Type: "offer"
   - Skill: "Accounting"
   - Description: "Experienced accountant offering tax preparation help"
   - Availability: "Mon 15-17"

INPUT → PROCESSING → OUTPUT:
Listing Form → Validation & API Call → Database Storage → Confirmation Message
        """
        
        print(script)
        return script
    
    def record_section_5_matching_algorithm(self):
        """
        RECORDING SECTION 5: Matching Algorithm Demonstration
        """
        print("\n" + "=" * 80)
        print("RECORDING SCRIPT - SECTION 5: MATCHING ALGORITHM")
        print("=" * 80)
        
        script = """
NARRATOR SCRIPT:
"Now comes the exciting part - our intelligent matching algorithm. Let's see 
how Alice finds help for her tax preparation."

DEMO STEPS:

1. ALICE CLICKS "🔍 View Matches"
   
   LOADING PROCESS (SHOW):
   - "🔍 Loading matches..." message appears
   - System searches for compatible offers
   - Multiple API calls happening in background

2. MATCHING ALGORITHM IN ACTION
   
   EXPLAIN THE SCORING SYSTEM:
   "Our algorithm uses a 100-point scoring system with four components:"
   
   - Skill Compatibility: 40 points (exact match required)
   - Location Proximity: 25 points (distance-based using Google Maps)
   - Time Compatibility: 25 points (schedule overlap analysis)  
   - Activity Level: 10 points (user engagement)

3. SHOW DISTANCE CALCULATION
   
   GOOGLE MAPS API CALL:
   - "Manila, Philippines" → Coordinates: 14.5995, 120.9842
   - "Quezon City, Philippines" → Coordinates: 14.6760, 121.0437
   
   HAVERSINE FORMULA CALCULATION:
   Distance = 15.2 km
   Location Score = 20 points (≤25km range)

4. TIME COMPATIBILITY ANALYSIS
   
   ALICE'S AVAILABILITY: Monday 14:00-16:00 (2 PM - 4 PM)
   BOB'S AVAILABILITY: Monday 15:00-17:00 (3 PM - 5 PM)
   
   OVERLAP DETECTION:
   Overlap period: Monday 15:00-16:00 (1 hour)
   Time Score = 15 points (good overlap on same day)

5. FINAL MATCH RESULT
   
   TOTAL SCORE CALCULATION:
   - Skill Match: 40 points ✅ (Accounting = Accounting)
   - Location: 20 points ✅ (15.2 km distance)
   - Time: 15 points ✅ (1-hour overlap)
   - Activity: 10 points ✅ (both users active)
   
   TOTAL: 85/100 = 85% Match Score

6. DISPLAY MATCH CARD
   
   SHOW ON SCREEN:
   🎯 Accounting
   📊 Match Score: 85%
   📍 Distance: 15.2 km  
   👤 Bob Jones
   📝 "Experienced accountant offering tax preparation help"
   ⏰ Perfect overlap on Monday 15:00-16:00
   🤝 "Create Match" button

INPUT → PROCESSING → OUTPUT:
User Request → Algorithm Analysis → Scored Match Results → Match Recommendations
        """
        
        print(script)
        return script
    
    def record_section_6_database_operations(self):
        """
        RECORDING SECTION 6: Database Operations
        """
        print("\n" + "=" * 80)
        print("RECORDING SCRIPT - SECTION 6: DATABASE OPERATIONS")
        print("=" * 80)
        
        script = """
NARRATOR SCRIPT:
"Let's examine the database operations that power our application."

DEMO STEPS:

1. SHOW DATABASE STRUCTURE
   
   OPEN SQLite DATABASE:
   Command: sqlite3 matchwise.db
   
   SHOW TABLES:
   .tables
   
   Result: users, listings, skills, matches

2. EXAMINE USER DATA
   
   SQL QUERY:
   SELECT * FROM users;
   
   SHOW RESULTS:
   | id | username    | password_hash | full_name   | location              | skills     |
   |----|-------------|---------------|-------------|-----------------------|------------|
   | 1  | alice_smith | [hash]        | Alice Smith | Manila, Philippines   | Accounting |
   | 2  | bob_jones   | [hash]        | Bob Jones   | Quezon City, Philippines | Accounting |

3. EXAMINE LISTINGS DATA
   
   SQL QUERY:
   SELECT * FROM listings;
   
   SHOW RESULTS:
   | id | user_id | skill_name | type    | description              | availability |
   |----|---------|------------|---------|--------------------------|--------------|
   | 1  | 1       | Accounting | request | Need help with taxes...  | Mon 14-16    |
   | 2  | 2       | Accounting | offer   | Experienced accountant...| Mon 15-17    |

4. SHOW SKILLS TABLE
   
   SQL QUERY:
   SELECT name FROM skills LIMIT 10;
   
   AVAILABLE SKILLS:
   - Accounting
   - Programming  
   - Cooking
   - Language Tutoring
   - Graphic Design
   - Music Lessons
   - Math Tutoring
   - Writing
   - Photography
   - Web Development

5. REAL-TIME DATA FLOW
   
   DEMONSTRATE:
   - User creates listing → INSERT INTO listings
   - System finds matches → SELECT with JOIN operations
   - Match created → INSERT INTO matches table
   - Status updates → UPDATE matches SET status

DATABASE OPERATIONS:
CREATE → READ → UPDATE → DELETE (Full CRUD operations)
        """
        
        print(script)
        return script
    
    def record_section_7_api_endpoints(self):
        """
        RECORDING SECTION 7: API Endpoints Demonstration
        """
        print("\n" + "=" * 80)
        print("RECORDING SCRIPT - SECTION 7: API ENDPOINTS")
        print("=" * 80)
        
        script = """
NARRATOR SCRIPT:
"Behind the scenes, our application uses a REST API built with FastAPI. 
Let's examine the API endpoints in action."

DEMO STEPS:

1. START API SERVER
   
   Command: python main.py
   
   SHOW TERMINAL OUTPUT:
   INFO: Started server process
   INFO: Uvicorn running on http://127.0.0.1:8000
   INFO: Application startup complete

2. DEMONSTRATE API CALLS
   
   Using browser or Postman, show:
   
   GET http://127.0.0.1:8000/skills/
   Response: {"skills": ["Accounting", "Programming", ...]}
   
   GET http://127.0.0.1:8000/listings/?user_id=1  
   Response: {"listings": [{"id": 1, "skill_name": "Accounting", ...}]}

3. MATCHING API ENDPOINT
   
   GET http://127.0.0.1:8000/matches/find/1
   
   SHOW JSON RESPONSE:
   {
     "matches": [
       {
         "match_score": 85.0,
         "request_listing": {...},
         "offer_listing": {...},
         "distance_km": 15.2,
         "time_compatibility": "Perfect overlap on Monday 15:00-16:00",
         "match_explanation": "Excellent match with high compatibility"
       }
     ]
   }

4. API DOCUMENTATION
   
   VISIT: http://127.0.0.1:8000/docs
   
   SHOW FEATURES:
   - Interactive API documentation
   - Try-it-now functionality
   - Request/response schemas
   - Authentication details

API ARCHITECTURE:
Frontend (Flet) ←→ REST API (FastAPI) ←→ Database (SQLite)
        """
        
        print(script)
        return script
    
    def record_section_8_error_handling(self):
        """
        RECORDING SECTION 8: Error Handling and Validation
        """
        print("\n" + "=" * 80)
        print("RECORDING SCRIPT - SECTION 8: ERROR HANDLING")
        print("=" * 80)
        
        script = """
NARRATOR SCRIPT:
"A robust application must handle errors gracefully. Let's demonstrate 
our validation and error handling systems."

DEMO STEPS:

1. REGISTRATION VALIDATION ERRORS
   
   TRY TO REGISTER WITH:
   - Empty username → "⚠️ All fields are required"
   - Existing username → "❌ Username already exists"
   - Mismatched passwords → "⚠️ Passwords do not match"
   
   SHOW HOW EACH ERROR APPEARS IN THE UI

2. LOGIN VALIDATION ERRORS
   
   TRY TO LOGIN WITH:
   - Wrong password → "❌ Invalid username or password"
   - Non-existent user → "❌ Invalid username or password"
   
   SECURITY NOTE: "Generic error message prevents username enumeration"

3. LISTING CREATION ERRORS
   
   TRY TO CREATE LISTING WITH:
   - Missing fields → "⚠️ Please fill all fields"
   - Invalid time range → "⚠️ End hour must be after start hour"
   
4. NETWORK ERROR HANDLING
   
   STOP API SERVER, THEN:
   - Try to create listing → "❌ Connection Error: Connection refused"
   - Try to load matches → "❌ Error loading matches: Network unreachable"

5. DATABASE ERROR HANDLING
   
   DEMONSTRATE:
   - Graceful fallback for missing data
   - User-friendly error messages
   - System continues functioning despite errors

ERROR HANDLING STRATEGY:
Validate Input → Process Safely → Return User-Friendly Messages → Log Technical Details
        """
        
        print(script)
        return script
    
    def record_section_9_complete_workflow(self):
        """
        RECORDING SECTION 9: Complete Workflow Demonstration
        """
        print("\n" + "=" * 80)
        print("RECORDING SCRIPT - SECTION 9: COMPLETE WORKFLOW")
        print("=" * 80)
        
        script = """
NARRATOR SCRIPT:
"Let's now demonstrate the complete workflow from registration to successful matching."

COMPLETE DEMO WORKFLOW:

1. USER REGISTRATION (Alice)
   Input: Registration form
   Process: Validation, hashing, database storage
   Output: Successful account creation

2. USER LOGIN (Alice)  
   Input: Username and password
   Process: Authentication and session creation
   Output: Personalized dashboard

3. CREATE REQUEST LISTING (Alice)
   Input: Skill request details
   Process: API call and database storage
   Output: Active listing

4. SECOND USER REGISTRATION (Bob)
   Input: Registration form with complementary skills
   Process: Account creation
   Output: Second user account

5. CREATE OFFER LISTING (Bob)
   Input: Skill offer details  
   Process: Database storage
   Output: Matching offer available

6. FIND MATCHES (Alice)
   Input: Match search request
   Process: Algorithm analysis, scoring, ranking
   Output: Ranked list of compatible users

7. CREATE MATCH
   Input: Select preferred match
   Process: Match record creation
   Output: Connection established

8. MATCH MANAGEMENT
   Input: Accept/decline/complete actions
   Process: Status updates
   Output: Successful skill exchange

COMPLETE DATA FLOW:
Registration → Authentication → Listing Creation → Matching Algorithm → Match Management → Skill Exchange

SUCCESS METRICS:
- 85% match score achieved
- 15.2 km distance (excellent proximity)
- 1-hour time overlap (perfect scheduling)
- Successful connection between users
        """
        
        print(script)
        return script
    
    def record_section_10_conclusion(self):
        """
        RECORDING SECTION 10: Conclusion and Summary
        """
        print("\n" + "=" * 80)
        print("RECORDING SCRIPT - SECTION 10: CONCLUSION")
        print("=" * 80)
        
        script = """
NARRATOR SCRIPT:
"We've successfully demonstrated the complete MatchWise application workflow."

SUMMARY OF DEMONSTRATED FEATURES:

1. TECHNICAL ARCHITECTURE
   ✅ Python-based application with modern frameworks
   ✅ FastAPI REST API backend
   ✅ Flet UI framework for desktop interface
   ✅ SQLite database for data persistence
   ✅ Google Maps API integration

2. USER EXPERIENCE FEATURES
   ✅ Intuitive registration and login process
   ✅ Simple listing creation with validation
   ✅ Intelligent matching algorithm
   ✅ Real-time match scoring and explanations
   ✅ Single-window navigation system

3. MATCHING ALGORITHM CAPABILITIES
   ✅ 100-point scoring system
   ✅ Geographic distance calculation using Haversine formula
   ✅ Flexible time compatibility analysis
   ✅ Skill-based matching with 30+ categories
   ✅ Percentage-based match explanations

4. TECHNICAL ROBUSTNESS
   ✅ Comprehensive error handling
   ✅ Input validation and security measures
   ✅ RESTful API design
   ✅ Scalable database schema
   ✅ Real-time data updates

BUSINESS VALUE:
- Connects people for skill sharing
- Reduces learning barriers
- Builds community connections
- Efficient matching reduces search time
- Flexible scheduling accommodates busy lifestyles

FUTURE ENHANCEMENTS:
- Mobile app version
- Advanced filtering options
- Rating and review system
- Payment integration
- Video call integration
- Expanded skill categories

FINAL DEMONSTRATION RESULT:
✅ Alice (needs tax help) successfully matched with Bob (tax expert)
✅ 85% compatibility score
✅ Geographic proximity confirmed  
✅ Scheduling compatibility verified
✅ Ready for skill exchange to begin

The MatchWise application successfully demonstrates how technology can facilitate 
meaningful connections and enable efficient skill sharing in local communities.

Thank you for watching this demonstration!
        """
        
        print(script)
        return script
    
    def generate_complete_recording_script(self):
        """
        Generate the complete recording script
        """
        print("MATCHWISE APPLICATION - COMPLETE RECORDING SCRIPT")
        print("=" * 80)
        print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Estimated Duration: 15-20 minutes")
        print("Target Audience: Technical and non-technical stakeholders")
        
        sections = [
            self.record_section_1_introduction(),
            self.record_section_2_user_registration(),
            self.record_section_3_user_login(),
            self.record_section_4_creating_listings(),
            self.record_section_5_matching_algorithm(),
            self.record_section_6_database_operations(),
            self.record_section_7_api_endpoints(),
            self.record_section_8_error_handling(),
            self.record_section_9_complete_workflow(),
            self.record_section_10_conclusion()
        ]
        
        print("\n" + "=" * 80)
        print("RECORDING CHECKLIST")
        print("=" * 80)
        
        checklist = """
PRE-RECORDING PREPARATION:
□ Start API server (python main.py)
□ Ensure database is initialized with sample data
□ Clear any existing user data for clean demo
□ Test all functionality once before recording
□ Prepare screen recording software
□ Set up proper lighting and audio

DURING RECORDING:
□ Speak clearly and at moderate pace
□ Explain each step before performing it
□ Show both input and output for each operation
□ Highlight key technical concepts
□ Point out error handling scenarios
□ Demonstrate the matching algorithm clearly

POST-RECORDING:
□ Review footage for clarity
□ Add captions/subtitles if needed
□ Include timestamps for key sections
□ Prepare accompanying documentation
□ Test recording playback quality

TECHNICAL REQUIREMENTS:
□ Python 3.12+ installed
□ All dependencies installed (pip install -r requirements.txt)
□ Google Maps API key configured (optional for demo)
□ Screen recording software configured
□ Adequate system resources for smooth demo
        """
        
        print(checklist)


def main():
    """
    Main function to generate the recording script
    """
    script_generator = MatchWiseRecordingScript()
    script_generator.generate_complete_recording_script()


if __name__ == "__main__":
    main()
