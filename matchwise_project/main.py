from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# User model
class User(BaseModel):
    full_name: str
    email: str
    location: str = ""
    availability: str = ""

@app.get("/")
def read_root():
    return {"message": "Welcome to MatchWise API!"}

@app.get("/users/")
def get_users():
    conn = sqlite3.connect("matchwise.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, full_name, email FROM users")
    users = cursor.fetchall()
    conn.close()
    return {"users": users}

@app.post("/register/")
def register_user(user: User):
    conn = sqlite3.connect("matchwise.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (full_name, email, location, availability)
            VALUES (?, ?, ?, ?)
        """, (user.full_name, user.email, user.location, user.availability))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered.")
    conn.close()
    return {"message": f"User '{user.full_name}' registered successfully!"}


# Listing model
class Listing(BaseModel):
    user_id: int
    skill_id: int
    type: str  # 'offer' or 'request'
    description: str
    availability: str
    location: str
    radius_km: int

# Create a listing
@app.post("/listings/")
def create_listing(listing: Listing):
    if listing.type not in ["offer", "request"]:
        raise HTTPException(status_code=400, detail="Type must be 'offer' or 'request'")
    
    conn = sqlite3.connect("matchwise.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO listings (user_id, skill_id, type, description, availability, location, radius_km)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (listing.user_id, listing.skill_id, listing.type, listing.description, listing.availability, listing.location, listing.radius_km))
    conn.commit()
    conn.close()
    return {"message": f"{listing.type.capitalize()} listing created."}

# Get all listings
@app.get("/listings/")
def get_all_listings():
    conn = sqlite3.connect("matchwise.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT listing_id, user_id, skill_id, type, description, availability, location, radius_km
        FROM listings
    """)
    listings = cursor.fetchall()
    conn.close()
    return {"listings": listings}

# Get listings by type
@app.get("/listings/{listing_type}/")
def get_listings_by_type(listing_type: str):
    if listing_type not in ["offer", "request"]:
        raise HTTPException(status_code=400, detail="Invalid listing type")
    
    conn = sqlite3.connect("matchwise.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT listing_id, user_id, skill_id, type, description, availability, location, radius_km
        FROM listings
        WHERE type = ?
    """, (listing_type,))
    listings = cursor.fetchall()
    conn.close()
    return {f"{listing_type}_listings": listings}
@app.get("/match/{request_listing_id}/")
def find_matches_for_request(request_listing_id: int):
    conn = sqlite3.connect("matchwise.db")
    cursor = conn.cursor()

    # Get the request listing details
    cursor.execute("""
        SELECT skill_id, availability, location
        FROM listings
        WHERE listing_id = ? AND type = 'request'
    """, (request_listing_id,))
    request_listing = cursor.fetchone()

    if not request_listing:
        conn.close()
        raise HTTPException(status_code=404, detail="Request listing not found.")

    skill_id, req_avail, req_location = request_listing

    # Find matching offers with same skill
    cursor.execute("""
        SELECT listing_id, user_id, description, availability, location
        FROM listings
        WHERE skill_id = ? AND type = 'offer'
    """, (skill_id,))
    offers = cursor.fetchall()
    conn.close()

    return {
        "matches": [
            {
                "listing_id": o[0],
                "user_id": o[1],
                "description": o[2],
                "availability": o[3],
                "location": o[4]
            }
            for o in offers
            if req_avail in o[3] or o[3] in req_avail  # simple overlap check
        ]
    }
