# MatchWise – Smart Matching of Skills and Needs

MatchWise is a community-based skill-sharing platform that intelligently matches volunteers with requesters based on skills, availability, and location. It supports local engagement through a fair and optimized system for offering and requesting help such as tutoring, repairs, tech support, and more.

---

## 🚀 Features

- **User registration and profile management** - Create accounts with location and availability
- **Skill management and tagging** - 30+ predefined skills with easy selection  
- **Smart listing system** - Create offers and requests for skills
- **Advanced matching algorithm** - Matches based on:
  - Skill compatibility (40 points)
  - Location proximity (25 points) 
  - Availability overlap (25 points)
  - User activity level (10 points)
- **Real-time match scoring** - Scores from 0-100% for match quality
- **Interactive dashboard** - View matches, create listings, browse all listings
- **SQLite database** - Persistent data storage
- **FastAPI backend** - High-performance API with auto-generated docs
- **Flet UI** - Modern desktop interface

---

## 🎯 What's New & Completed

### ✅ Completed Functions:

1. **Advanced Matching Algorithm**
   - `calculate_match_score()` - Comprehensive scoring system
   - `calculate_availability_overlap()` - Time slot matching
   - `calculate_distance()` - Location-based scoring (with Google Maps API fallback)

2. **Complete API Endpoints**
   - `POST /matches/find/` - Find potential matches for users
   - `POST /matches/create/` - Create matches between users  
   - `GET /matches/` - View user's existing matches
   - `PUT /matches/{match_id}/status/` - Accept/decline/complete matches
   - `GET /listings/` - Browse all listings with filters

3. **Enhanced Dashboard**
   - **View Matches** - See potential and existing matches with scores
   - **My Listings** - Manage your offers and requests
   - **Browse Listings** - Explore all community listings
   - **Create Listings** - Easy form with validation

4. **Database Improvements**
   - Added status tracking for listings and matches
   - Timestamps for all records
   - Proper foreign key relationships
   - Sample data for testing

### 🎯 Easier Matching System:

- **Automatic Match Discovery** - System finds matches for you
- **Smart Scoring** - Clear percentage scores show match quality
- **Time Overlap Detection** - Shows exactly when you're both available
- **One-Click Actions** - Accept, decline, or complete matches easily
- **Visual Feedback** - Color-coded status and clear icons

---

## 🛠️ Setup Instructions

### ✅ Windows Terminal

1. **Navigate to project folder:**
   ```bash
   cd "c:\Users\Asus TUF\Downloads\Reop\CPE106L-4_E01-3T2425-3\matchwise_project"
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn requests flet
   ```

3. **Initialize database with sample data:**
   ```bash
   python init_db.py
   python add_sample_data.py
   ```

4. **Start the application:**
   ```bash
   python start_app.py
   ```
   This will:
   - Start the FastAPI server
   - Open API docs in browser
   - Show instructions for UI

5. **Start the UI (in a new terminal):**
   ```bash
   python login_ui.py
   ```

6. **Test with sample accounts:**
   - Username: `alice` / Password: `password123`
   - Username: `bob` / Password: `password123`
   - Username: `carol` / Password: `password123`

---

## 🔧 Quick Start Guide

### 1. Testing the Matching System

1. **Login** as `alice` (password: `password123`)
2. **View Matches** - See potential matches for Alice's programming offer and cooking request
3. **Create a Match** - Click "Create Match" on a high-scoring potential match
4. **Switch Users** - Logout and login as `bob` to see the match from the other side
5. **Accept/Decline** - Bob can accept or decline Alice's programming help

### 2. Creating New Listings

1. **Click "Create Listing"**
2. **Choose Type** - Offer a skill or Request help
3. **Select Skill** - From 30+ available skills
4. **Add Description** - What specifically you need/offer
5. **Set Availability** - When you're available
6. **Submit** - System automatically finds matches

### 3. Browse Community

1. **Click "Browse All Listings"**
2. **Filter** - By type (offers/requests) or skill
3. **View Details** - See what others are offering/requesting
4. **Manual Matching** - Contact users directly

---

## 📊 API Documentation

**Interactive API docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Key Endpoints:

- `POST /register/` - Create new user account
- `POST /login/` - User authentication  
- `POST /listings/` - Create skill listing
- `GET /listings/` - Browse listings with filters
- `POST /matches/find/` - Find potential matches
- `POST /matches/create/` - Create match between users
- `GET /matches/` - View user's matches
- `PUT /matches/{match_id}/status/` - Update match status

---

## 🏗️ Project Structure

```
matchwise_project/
├── main.py              # FastAPI backend with matching algorithms
├── init_db.py           # Database initialization with schema
├── add_sample_data.py   # Sample users and listings for testing
├── migrate_db.py        # Database schema updates
├── start_app.py         # Easy startup script
├── flet_dashboard.py    # Complete UI dashboard with all features
├── login_ui.py          # Login interface
├── login_data.py        # Login API integration
├── register_ui.py       # Registration interface  
├── register_data.py     # Registration API integration
├── matchwise.db         # SQLite database (auto-created)
└── README.md           # This documentation
```

---

## 🧮 Matching Algorithm Details

### Scoring System (0-100 points):

1. **Skill Match (40 points)** - Must match exactly
2. **Location Proximity (25 points)**
   - Same location: 25 points
   - Within 10km: 25 points
   - Within 25km: 20 points
   - Within 50km: 15 points
   - Within 100km: 10 points
   - Further: 5 points

3. **Availability Overlap (25 points)**
   - More overlapping time slots = higher score
   - Calculated by parsing "Day HH-HH" format

4. **Activity Level (10 points)**
   - Recent activity and responsiveness

### Example Calculation:
- Alice offers Programming on "Mon 18-20"
- Bob requests Programming on "Mon 19-21"  
- Both in New York
- **Score: 40 + 25 + 20 + 10 = 95%** (Excellent match!)

---

## 📦 Dependencies

- **Python 3.12+**
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **SQLite** - Database (via Python standard library)
- **Pydantic** - Data validation
- **Requests** - HTTP client
- **Flet** - Desktop UI framework
- **Google Maps API** (optional) - For accurate distance calculation

---

## 🎮 Demo Scenarios

### Scenario 1: Programming Help
1. Alice offers Python programming tutoring
2. Bob requests JavaScript help  
3. **No match** - Different skills

### Scenario 2: Cooking Lessons
1. Carol offers cooking lessons in Brooklyn
2. Alice requests cooking help in New York
3. **85% match** - Same skill, nearby locations, some time overlap

### Scenario 3: Perfect Match
1. Eva offers guitar lessons "Wed 17-21"
2. David requests guitar lessons "Wed 18-20"
3. **95% match** - Same skill, overlapping times, nearby

---

## 🚀 Advanced Features

### For Developers:
- **Real-time matching** via WebSocket (can be added)
- **Machine learning** recommendations (can be integrated)
- **Rating system** for match quality improvement
- **Calendar integration** for availability management

### For Users:
- **Smart notifications** for new matches
- **Feedback system** to improve matching
- **Community features** like skill groups
- **Mobile app** version using Flet mobile

---

## 🔍 Troubleshooting

### Common Issues:

1. **Server won't start**
   ```bash
   pip install --upgrade fastapi uvicorn
   python -m uvicorn main:app --reload
   ```

2. **Database errors**
   ```bash
   python migrate_db.py
   python init_db.py
   ```

3. **No matches found**
   - Check that users have created both offers and requests
   - Verify skills match exactly
   - Run `python add_sample_data.py` for test data

4. **UI connection errors**
   - Ensure FastAPI server is running on port 8000
   - Check firewall settings
   - Verify API base URL in flet_dashboard.py

---

## 👥 Team Members & Roles

| Name                | Role                         |
|---------------------|------------------------------|
| Ivan                | Developer, System Integrator |
| Justin           | Database Designer            |
| Kirby               | API Tester, Documentation    |



---

## ✅ Future Enhancements

- 🗺️ **Google Maps integration** for real location matching
- 📱 **Mobile app** with Flet mobile framework  
- 📊 **Analytics dashboard** with match success rates
- 💬 **In-app messaging** between matched users
- ⭐ **Rating and review system** for skill providers
- 🔔 **Push notifications** for new matches
- 🎯 **AI-powered** skill recommendations
- 📅 **Calendar integration** for scheduling

---

## 📄 License

This project is created for educational purposes as part of CPE106L coursework.

---

**🎉 Happy Skill Sharing with MatchWise! 🎉**
