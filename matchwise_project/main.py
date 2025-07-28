from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List
import sqlite3
import os

app = FastAPI()

# Set up path to database
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "matchwise.db")

Maps_API_KEY = "AIzaSyD6VUdTTciWHoYMrDIwIIHYjSpgFQwdCAA"

# -------------------- MODELS --------------------
class LoginData(BaseModel):
    username: str
    password: str

# User model no longer includes 'skills' or 'availability'
class User(BaseModel):
    full_name: str
    username: str
    password: str
    email: str
    location: str = ""

class CreateListing(BaseModel):
    user_id: int
    type: str
    skill: str
    availability: str
    description: str

# -------------------- ENDPOINTS --------------------

@app.post("/register/")
def register_user(user: User):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Removed availability and skills insertion logic
        cursor.execute("""
            INSERT INTO users (full_name, username, password, email, location, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user.full_name, user.username, user.password, user.email, user.location, 0))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists or invalid data.")
    finally:
        if conn:
            conn.close()
    return {"message": f"User '{user.username}' registered successfully!"}

@app.post("/login/")
def login(data: LoginData):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, full_name, location FROM users WHERE username = ? AND password = ?", (data.username, data.password))
    user = cursor.fetchone()
    conn.close()
    if user:
        user_id, full_name, location = user
        return {"message": "Login successful!", "user_id": user_id, "full_name": full_name, "location": location}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/listings/")
def create_listing(listing: CreateListing):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT skill_id FROM skills WHERE name = ?", (listing.skill,))
        result = cursor.fetchone()
        skill_id = result[0] if result else cursor.execute("INSERT INTO skills (name) VALUES (?)", (listing.skill,)).lastrowid

        cursor.execute("SELECT location FROM users WHERE user_id = ?", (listing.user_id,))
        user_location_row = cursor.fetchone()
        user_location = user_location_row[0] if user_location_row else "Unknown"

        cursor.execute("""
            INSERT INTO listings (user_id, skill_id, type, availability, description, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (listing.user_id, skill_id, listing.type, listing.availability, listing.description, user_location))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
    return {"message": "Listing created successfully"}

@app.get("/skills/")
def get_all_skills():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Simplified to only get skills from the official 'skills' table
        cursor.execute("SELECT name FROM skills ORDER BY name ASC")
        skills = {row[0] for row in cursor.fetchall()}
        return {"skills": sorted(list(skills))}
    finally:
        if conn:
            conn.close()