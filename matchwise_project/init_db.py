import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "matchwise.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🔧 Initializing MatchWise Database...")

cursor.executescript("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    location TEXT,
    availability TEXT,
    is_admin BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS user_skills (
    user_id INTEGER,
    skill_id INTEGER,
    proficiency TEXT CHECK(proficiency IN ('novice', 'intermediate', 'expert')),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(skill_id) REFERENCES skills(skill_id),
    PRIMARY KEY (user_id, skill_id)
);

CREATE TABLE IF NOT EXISTS listings (
    listing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    skill_id INTEGER,
    type TEXT CHECK(type IN ('offer', 'request')),
    description TEXT,
    availability TEXT,
    location TEXT,
    radius_km INTEGER DEFAULT 50,
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
);

CREATE TABLE IF NOT EXISTS availability (
    availability_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    timeslot TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_request_id INTEGER,
    listing_offer_id INTEGER,
    match_score REAL,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'accepted', 'declined', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(listing_request_id) REFERENCES listings(listing_id),
    FOREIGN KEY(listing_offer_id) REFERENCES listings(listing_id)
);

CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    match_id INTEGER,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(sender_id) REFERENCES users(user_id),
    FOREIGN KEY(receiver_id) REFERENCES users(user_id),
    FOREIGN KEY(match_id) REFERENCES matches(match_id)
);
""")

# Insert some default skills
default_skills = [
    "Programming", "Web Development", "Cooking", "Tutoring", "Math", 
    "English", "Spanish", "French", "Graphic Design", "Photography",
    "Plumbing", "Carpentry", "Electrical Work", "Gardening", "Cleaning",
    "Music Lessons", "Piano", "Guitar", "Singing", "Dancing",
    "Fitness Training", "Yoga", "Massage Therapy", "Pet Care", "Driving",
    "Writing", "Editing", "Translation", "Data Analysis", "Accounting"
]

for skill in default_skills:
    cursor.execute("INSERT OR IGNORE INTO skills (name) VALUES (?)", (skill,))

print("✅ Database initialized successfully!")
print("📍 Database location:", os.path.abspath("matchwise.db"))

conn.commit()
conn.close()
