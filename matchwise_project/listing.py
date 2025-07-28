from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List
import sqlite3
import os
import requests

app = FastAPI()

# Set up path to database
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "matchwise.db")

# Google Maps API key (used elsewhere)
Maps_API_KEY = "AIzaSyD6VUdTTciWHoYMrDIwIIHYjSpgFQwdCAA"

# -------------------- MODELS --------------------
class AvailabilityUpdate(BaseModel):
    availability: List[str]

class LoginData(BaseModel):
    username: str
    password: str

class User(BaseModel):
    full_name: str
    username: str
    password: str
    email: str
    location: str = ""
    availability: str = ""

class CreateListing(BaseModel):
    user_id: int
    type: str  # e.g., "offer" or "request"
    skill: str
    availability: str

# -------------------- ENDPOINTS --------------------

@app.post("/register/")
def register_user(user: User):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Insert user
        cursor.execute("""
            INSERT INTO users (full_name, username, password, email, location, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user.full_name, user.username, user.password, user.email, user.location, 0))
        user_id = cursor.lastrowid

        # Insert availability if provided
        if user.availability:
            for slot in user.availability.split(","):
                cursor.execute("INSERT INTO availability (user_id, timeslot) VALUES (?, ?)", (user_id, slot.strip()))

        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists or invalid data.")
    conn.close()
    return {"message": f"User '{user.username}' registered successfully!"}

@app.post("/login/")
def login(data: LoginData):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, full_name FROM users WHERE username = ? AND password = ?", (data.username, data.password))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_id, full_name = user
        return {"message": "Login successful!", "user_id": user_id, "full_name": full_name}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/update_skills/")
def update_user_skills(user_id: int, skills: List[str] = Body(...)):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    skills_str = ",".join(skills)
    cursor.execute("UPDATE users SET skills = ? WHERE user_id = ?", (skills_str, user_id))
    conn.commit()
    conn.close()
    return {"message": "Skills updated successfully"}

@app.get("/users/{user_id}/availability")
def get_user_availability(user_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT timeslot FROM availability WHERE user_id = ?", (user_id,))
    slots = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"availability": slots}

@app.post("/update_availability/")
def update_availability(user_id: int, availability: List[str] = Body(...)):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Delete old availability
        c.execute("DELETE FROM availability WHERE user_id = ?", (user_id,))

        # Insert new availability
        for slot in availability:
            if " " in slot and "-" in slot:
                c.execute("INSERT INTO availability (user_id, timeslot) VALUES (?, ?)", (user_id, slot.strip()))

        conn.commit()
        return {"message": "Availability updated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/users/")
def get_users():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, full_name, email, skills FROM users")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"user_id": uid, "full_name": fn, "email": em, "skills": skills.split(",") if skills else []}
        for uid, fn, em, skills in rows
    ]

@app.get("/users/{user_id}/skills")
def get_user_skills(user_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT skills FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row and row[0]:
        return {"skills": row[0].split(",")}
    else:
        return {"skills": []}

@app.post("/listings/")
def create_listing(listing: CreateListing):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if skill exists or insert
    cursor.execute("SELECT skill_id FROM skills WHERE name = ?", (listing.skill,))
    result = cursor.fetchone()
    if result:
        skill_id = result[0]
    else:
        cursor.execute("INSERT INTO skills (name) VALUES (?)", (listing.skill,))
        skill_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO listings (user_id, skill_id, type, description, availability, location, radius_km)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        listing.user_id,
        skill_id,
        listing.type,
        "Sample description",
        listing.availability,
        "Sample location",
        10
    ))

    conn.commit()
    conn.close()
    return {"message": "Listing created successfully"}

# 👇 NEW ENDPOINT
@app.get("/skills/")
def get_all_skills():
    """Returns a list of all unique skills from the skills table."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Fetch all skill names from the dedicated 'skills' table
        cursor.execute("SELECT name FROM skills ORDER BY name ASC")
        skills = [row[0] for row in cursor.fetchall()]
        # Add any skills from the users table that might not be in the skills table yet
        cursor.execute("SELECT skills FROM users")
        user_skills_rows = cursor.fetchall()
        for row in user_skills_rows:
            if row[0]:
                for skill in row[0].split(','):
                    if skill.strip() not in skills:
                        skills.append(skill.strip())
        skills = sorted(list(set(skills))) # Get unique sorted list
        return {"skills": skills}
    finally:
        conn.close()