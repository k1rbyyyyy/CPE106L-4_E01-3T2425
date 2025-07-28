# MatchWise – Smart Matching of Skills and Needs

MatchWise is a community-based skill-sharing platform that intelligently matches volunteers with requesters based on skills, availability, and location. It supports local engagement through a fair and optimized system for offering and requesting help such as tutoring, repairs, tech support, and more.

---

## 🚀 Features

- User registration and profile management
- Skill management and tagging
- Listing system (offer/request)
- Greedy-based matching algorithm
- SQLite database
- FastAPI backend with auto-generated docs
- JSON-based REST API

---

## 🛠️ Setup Instructions

### ✅ Ubuntu Virtual Machine

1. Open Terminal in your project directory:
   ```bash
   cd ~/matchwise_project
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

4. Initialize the database:
   ```bash
   python3 init_db.py
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

6. Visit the interactive API docs:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### ✅ Windows Terminal

1. Open Windows Terminal and go to your project folder:
   ```bash
   cd path\to\matchwise_project
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

4. Run the database setup:
   ```bash
   python init_db.py
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

6. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the API.

---

## 📦 Dependencies

- Python 3.12+
- FastAPI
- Uvicorn
- SQLite (via Python standard library)
- Pydantic
- Google Maps Distance Matrix API
- Flet

---

## 📂 Project Structure

```
matchwise_project/
├── main.py          # FastAPI backend
├── flet_dashboard	 # Dashboard for app
├── flet-login		 # Initiates the login UI
├── flet-register    # Initiates the register UI
├── init_db.py       # SQLite database setup
├── matchwise.db     # SQLite database file (auto-created)
└── README.md        # Project documentation
```

---

## 👥 Team Members & Roles

| Name                | Role                         |
|---------------------|------------------------------|
| Ivan                | Developer, System Integrator |
| Ivan                | Database Designer            |
| Kirby               | API Tester, Documentation    |
| [Add Name Here]     | Algorithm & Matching Logic   |

> *Please update team names and roles as appropriate.*

---

## ✅ Next Features (Optional Ideas)

- Google Maps API integration for real location matching
- Flet Desktop GUI
- Skill demand and match visualization using Matplotlib
- Admin dashboard and user feedback system