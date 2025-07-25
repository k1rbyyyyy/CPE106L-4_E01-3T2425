from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List
import sqlite3
import os
import requests

app = FastAPI()
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "matchwise.db")

GOOGLE_MAPS_API_KEY = "AIzaSyD6VUdTTciWHoYMrDIwIIHYjSpgFQwdCAA"

# Models
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

@app.post("/register/")
def register_user(user: User):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Convert availability to comma-separated string
        availability_str = user.availability[0] if user.availability else ""
        
        cursor.execute("""
            INSERT INTO users
              (full_name, username, password, email, location, availability, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user.full_name,
            user.username,
            user.password,
            user.email,
            user.location,
            availability_str,  # Use the first slot only
            0  # is_admin is 0 for regular users
        ))
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
    
    # First try to get from availability table
    cursor.execute("SELECT timeslot FROM availability WHERE user_id = ?", (user_id,))
    slots = [row[0] for row in cursor.fetchall()]
    
    # If not found, try users table
    if not slots:
        cursor.execute("SELECT availability FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row and row[0]:
            # Split comma-separated slots
            slots = row[0].split(",")
    
    conn.close()
    return {"availability": slots}

@app.post("/update_availability/")
def update_availability(user_id: int, slots: List[str] = Body(...)):
    if len(slots) > 3:
        raise HTTPException(400, "Max 3 slots allowed")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET availability = ? WHERE user_id = ?",
        (",".join(slots), user_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Availability updated"}

@app.get("/users/")
def get_users():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, full_name, email, skills
        FROM users
    """)
    rows = cursor.fetchall()
    conn.close()
    return [
      {"user_id": uid, "full_name": fn, "email": em, "skills": skills.split(",") if skills else []}
      for uid,fn,em,skills in rows
    ]

@app.get("/users/{user_id}/skills")
def get_user_skills(user_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.name
        FROM user_skills us
        JOIN skills s ON us.skill_id = s.skill_id
        WHERE us.user_id = ?
    """, (user_id,))
    skills = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"skills": skills}