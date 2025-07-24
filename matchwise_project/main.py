from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
#from simulated_distance import get_distance_km (this was used to simulate distance before using Google Maps API)
import sqlite3
import os
import requests


base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "matchwise.db")
app = FastAPI()

GOOGLE_MAPS_API_KEY = "AIzaSyD6VUdTTciWHoYMrDIwIIHYjSpgFQwdCAA"

def get_distance_km(origin: str, destination: str) -> float:
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "key": GOOGLE_MAPS_API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    data = response.json()
    try:
        distance_meters = data["rows"][0]["elements"][0]["distance"]["value"]
        return distance_meters / 1000.0
    except Exception:
        print(f"⚠️ Google API failed for: {origin} → {destination}")
        return float('inf')
    

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
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, full_name, email FROM users")
    users = cursor.fetchall()
    conn.close()
    return {"users": users}

@app.post("/register/")
def register_user(user: User):
    conn = sqlite3.connect(db_path)
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
    
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT listing_id, user_id, skill_id, type, description, availability, location, radius_km
        FROM listings
    """)
    listings = cursor.fetchall()
    conn.close()
    return {"listings": listings}

# Get listings by type
@app.get("/listings/{listing_type}")
def get_listings_by_type(listing_type: str):
    if listing_type not in ["offer", "request"]:
        raise HTTPException(status_code=400, detail="Invalid listing type")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT listing_id, user_id, skill_id, type, description, availability, location, radius_km
        FROM listings
        WHERE type = ?
    """, (listing_type,))
    listings = cursor.fetchall()
    conn.close()
    return {f"{listing_type}_listings": listings}
def parse_availability(avail_str: str) -> List[Tuple[str, int, int]]:
    # Example input: "Mon 9-12,Tue 14-16"
    timeslots = []
    for slot in avail_str.split(","):
        try:
            day, hours = slot.strip().split()
            start, end = map(int, hours.split("-"))
            timeslots.append((day, start, end))
        except ValueError:
            continue
    return timeslots

def availability_overlap(req_avail: str, offer_avail: str) -> bool:
    req_slots = parse_availability(req_avail)
    offer_slots = parse_availability(offer_avail)
    for r_day, r_start, r_end in req_slots:
        for o_day, o_start, o_end in offer_slots:
            if r_day == o_day and not (r_end <= o_start or r_start >= o_end):
                return True
    return False

def score_match(request, offer) -> int:
    score = 1  # skill already matches
    if availability_overlap(request[1], offer[3]):
        score += 1
    if request[2] and offer[4] and request[2] == offer[4]:  # location string match
        score += 1
    return score

@app.get("/match/{request_listing_id}")
def find_matches_for_request(request_listing_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    
    # Get the request listing
    cursor.execute("""
        SELECT skill_id, availability, location, radius_km
        FROM listings
        WHERE listing_id = ? AND type = 'request'
    """, (request_listing_id,))
    request_listing = cursor.fetchone()
    if not request_listing:
        conn.close()
        raise HTTPException(status_code=404, detail="Request listing not found.")

    skill_id, req_avail, req_location, req_radius = request_listing

    

    # Get all offer listings for the same skill
    cursor.execute("""
        SELECT listing_id, user_id, description, availability, location, radius_km
        FROM listings
        WHERE skill_id = ? AND type = 'offer'
    """, (skill_id,))
    offers = cursor.fetchall()
    conn.close()

    matches = []
    for offer in offers:
        offer_id, user_id, desc, offer_avail, offer_location, offer_radius = offer

        # Compute availability overlap and distance
        overlap = availability_overlap(req_avail, offer_avail)
        distance = get_distance_km(req_location, offer[4])
        print(f"🧭 Distance from request to offer: {distance} km (offer in {offer[4]})")

        if distance > offer[5]:
            print("❌ Skipping - outside radius:", offer[5])
            continue

        score = score_match((skill_id, req_avail, req_location), offer)

        matches.append({
    "listing_id": offer_id,
    "score": score,
    "distance_km": distance,
    "location": offer_location,
    "debug": f"{req_location} → {offer_location} = {distance} km"
})
    # Sort matches by score descending
    matches.sort(key=lambda x: x["score"], reverse=True)

    return {"matches": matches}

