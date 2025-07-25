from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List
import sqlite3
import os
import requests

app = FastAPI()
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "matchwise.db")

GOOGLE_MAPS_API_KEY = "your_api_key_here"

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

    cursor.execute("DELETE FROM user_skills WHERE user_id = ?", (user_id,))
    for skill in skills:
        cursor.execute("SELECT skill_id FROM skills WHERE name = ?", (skill,))
        skill_row = cursor.fetchone()
        if skill_row:
            cursor.execute("INSERT INTO user_skills (user_id, skill_id) VALUES (?, ?)", (user_id, skill_row[0]))

    conn.commit()
    conn.close()
    return {"message": "Skills updated successfully"}

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