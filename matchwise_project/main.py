from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os
import math
import requests
from datetime import datetime

app = FastAPI(title="MatchWise API", description="Smart Matching of Skills and Needs", version="1.0.0")

# Set up path to database
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "matchwise.db")

Maps_API_KEY = "AIzaSyD6VUdTTciWHoYMrDIwIIHYjSpgFQwdCAA"

# -------------------- MODELS --------------------
class LoginData(BaseModel):
    username: str
    password: str

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

class MatchRequest(BaseModel):
    user_id: int
    listing_type: str = "request"  # Find matches for requests by default

class MatchResponse(BaseModel):
    match_id: Optional[int] = None
    request_listing: dict
    offer_listing: dict
    match_score: float
    distance_km: Optional[float] = None
    availability_overlap: List[str] = []

# -------------------- UTILITY FUNCTIONS --------------------

def parse_availability(availability_str: str) -> List[tuple]:
    """Parse availability string into list of (day, start_hour, end_hour) tuples"""
    slots = []
    if not availability_str:
        return slots
    
    for slot in availability_str.split(','):
        slot = slot.strip()
        if ' ' in slot and '-' in slot:
            day_part, time_part = slot.split(' ', 1)
            if '-' in time_part:
                start, end = time_part.split('-')
                try:
                    slots.append((day_part.strip(), int(start), int(end)))
                except ValueError:
                    continue
    return slots

def calculate_availability_overlap(avail1: str, avail2: str) -> List[str]:
    """Calculate overlapping availability between two users"""
    slots1 = parse_availability(avail1)
    slots2 = parse_availability(avail2)
    
    overlaps = []
    for day1, start1, end1 in slots1:
        for day2, start2, end2 in slots2:
            if day1 == day2:
                overlap_start = max(start1, start2)
                overlap_end = min(end1, end2)
                if overlap_start < overlap_end:
                    overlaps.append(f"{day1} {overlap_start}-{overlap_end}")
    
    return overlaps

def get_time_compatibility_explanation(avail1: str, avail2: str) -> str:
    """Get human-readable explanation of time compatibility"""
    slots1 = parse_availability(avail1)
    slots2 = parse_availability(avail2)
    
    # Check for perfect overlaps first
    overlaps = calculate_availability_overlap(avail1, avail2)
    if overlaps:
        return f"Perfect match! Overlapping times: {', '.join(overlaps)}"
    
    # Check for same day matches
    for day1, start1, end1 in slots1:
        for day2, start2, end2 in slots2:
            if day1 == day2:
                gap = min(abs(start1 - end2), abs(start2 - end1))
                if gap <= 1:
                    return f"Great match! Both available on {day1} within 1 hour of each other"
                elif gap <= 2:
                    return f"Good match! Both available on {day1} within 2 hours of each other"
                elif gap <= 4:
                    return f"Fair match! Both available on {day1} within 4 hours of each other"
                else:
                    return f"Same day availability on {day1} - coordination possible"
    
    # Check for adjacent days
    days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for day1, _, _ in slots1:
        for day2, _, _ in slots2:
            try:
                day1_idx = days_order.index(day1)
                day2_idx = days_order.index(day2)
                day_diff = abs(day1_idx - day2_idx)
                if day_diff == 1 or day_diff == 6:
                    return f"Adjacent day availability ({day1}/{day2}) - flexible scheduling possible"
            except ValueError:
                pass
    
    return "Different schedules - coordination may be needed"

def calculate_time_compatibility_score(avail1: str, avail2: str) -> float:
    """Calculate time compatibility score even without perfect overlap"""
    slots1 = parse_availability(avail1)
    slots2 = parse_availability(avail2)
    
    max_score = 0.0
    
    for day1, start1, end1 in slots1:
        for day2, start2, end2 in slots2:
            if day1 == day2:  # Same day
                # Perfect overlap
                overlap_start = max(start1, start2)
                overlap_end = min(end1, end2)
                if overlap_start < overlap_end:
                    overlap_hours = overlap_end - overlap_start
                    max_score = max(max_score, min(overlap_hours * 10, 25))  # Up to 25 points for perfect overlap
                else:
                    # No overlap but same day - calculate proximity score
                    if start1 <= end2 and start2 <= end1:  # Times are close
                        # Calculate how close the times are
                        gap = min(abs(start1 - end2), abs(start2 - end1))
                        if gap <= 1:  # Within 1 hour
                            proximity_score = 15  # Good proximity
                        elif gap <= 2:  # Within 2 hours
                            proximity_score = 10  # Moderate proximity
                        elif gap <= 4:  # Within 4 hours
                            proximity_score = 7   # Fair proximity
                        else:
                            proximity_score = 3   # Poor proximity but same day
                        max_score = max(max_score, proximity_score)
            else:
                # Different days - check if they're adjacent days
                days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                try:
                    day1_idx = days_order.index(day1)
                    day2_idx = days_order.index(day2)
                    day_diff = abs(day1_idx - day2_idx)
                    if day_diff == 1 or day_diff == 6:  # Adjacent days (including Sun-Mon wrap)
                        max_score = max(max_score, 5)  # Small bonus for adjacent days
                except ValueError:
                    pass
    
    return max_score

def get_coordinates(location: str) -> tuple:
    """Get coordinates for a location using Google Maps API"""
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': location,
            'key': Maps_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            location_data = data['results'][0]['geometry']['location']
            return location_data['lat'], location_data['lng']
    except:
        pass
    return None, None

def calculate_distance(loc1: str, loc2: str) -> float:
    """Calculate distance between two locations in kilometers"""
    lat1, lon1 = get_coordinates(loc1)
    lat2, lon2 = get_coordinates(loc2)
    
    if None in (lat1, lon1, lat2, lon2):
        # Fallback: simple text comparison
        if loc1.lower() == loc2.lower():
            return 0.0
        return 50.0  # Default distance if can't calculate
    
    # Haversine formula
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2) * math.sin(dlat/2) + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon/2) * math.sin(dlon/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance

def calculate_match_score(request_listing: dict, offer_listing: dict) -> float:
    """Calculate match score between a request and offer listing"""
    score = 0.0
    
    # Skill match (most important) - 40 points
    if request_listing['skill_name'] == offer_listing['skill_name']:
        score += 40.0
    
    # Location proximity - 25 points
    distance = calculate_distance(request_listing['location'], offer_listing['location'])
    if distance <= 10:
        score += 25.0
    elif distance <= 25:
        score += 20.0
    elif distance <= 50:
        score += 15.0
    elif distance <= 100:
        score += 10.0
    else:
        score += 5.0
    
    # Time compatibility - 25 points (improved to include partial matches)
    time_score = calculate_time_compatibility_score(
        request_listing['availability'], 
        offer_listing['availability']
    )
    score += time_score
    
    # Activity level (recent listings) - 10 points
    # This could be enhanced with user activity data
    score += 10.0
    
    return min(score, 100.0)  # Cap at 100

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

@app.get("/listings/")
def get_listings(user_id: Optional[int] = None, listing_type: Optional[str] = None, skill: Optional[str] = None):
    """Get listings with optional filters"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        query = """
            SELECT l.listing_id, l.user_id, u.full_name, s.name as skill_name, 
                   l.type, l.description, l.availability, l.location, l.status, l.created_at
            FROM listings l
            JOIN users u ON l.user_id = u.user_id
            JOIN skills s ON l.skill_id = s.skill_id
            WHERE l.status = 'active'
        """
        params = []
        
        if user_id:
            query += " AND l.user_id = ?"
            params.append(user_id)
        
        if listing_type:
            query += " AND l.type = ?"
            params.append(listing_type)
            
        if skill:
            query += " AND s.name = ?"
            params.append(skill)
            
        query += " ORDER BY l.created_at DESC"
        
        cursor.execute(query, params)
        listings = []
        for row in cursor.fetchall():
            listings.append({
                "listing_id": row[0],
                "user_id": row[1],
                "user_name": row[2],
                "skill_name": row[3],
                "type": row[4],
                "description": row[5],
                "availability": row[6],
                "location": row[7],
                "status": row[8],
                "created_at": row[9]
            })
        
        return {"listings": listings}
    finally:
        conn.close()

@app.post("/matches/find/")
def find_matches(match_request: MatchRequest):
    """Find matches for a user's listings"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get user's request listings if looking for offers, or vice versa
        target_type = "offer" if match_request.listing_type == "request" else "request"
        
        # Get user's listings of the specified type
        cursor.execute("""
            SELECT l.listing_id, l.user_id, u.full_name, s.name as skill_name, 
                   l.type, l.description, l.availability, l.location, l.status
            FROM listings l
            JOIN users u ON l.user_id = u.user_id
            JOIN skills s ON l.skill_id = s.skill_id
            WHERE l.user_id = ? AND l.type = ? AND l.status = 'active'
        """, (match_request.user_id, match_request.listing_type))
        
        user_listings = []
        for row in cursor.fetchall():
            user_listings.append({
                "listing_id": row[0],
                "user_id": row[1],
                "user_name": row[2],
                "skill_name": row[3],
                "type": row[4],
                "description": row[5],
                "availability": row[6],
                "location": row[7],
                "status": row[8]
            })
        
        if not user_listings:
            return {"matches": [], "message": f"No active {match_request.listing_type} listings found for user"}
        
        all_matches = []
        
        for user_listing in user_listings:
            # Find potential matches for this listing
            cursor.execute("""
                SELECT l.listing_id, l.user_id, u.full_name, s.name as skill_name, 
                       l.type, l.description, l.availability, l.location, l.status
                FROM listings l
                JOIN users u ON l.user_id = u.user_id
                JOIN skills s ON l.skill_id = s.skill_id
                WHERE l.type = ? AND l.status = 'active' AND l.user_id != ? AND s.name = ?
            """, (target_type, match_request.user_id, user_listing['skill_name']))
            
            potential_matches = []
            for row in cursor.fetchall():
                potential_matches.append({
                    "listing_id": row[0],
                    "user_id": row[1],
                    "user_name": row[2],
                    "skill_name": row[3],
                    "type": row[4],
                    "description": row[5],
                    "availability": row[6],
                    "location": row[7],
                    "status": row[8]
                })
            
            # Calculate match scores
            for potential_match in potential_matches:
                try:
                    if match_request.listing_type == "request":
                        score = calculate_match_score(user_listing, potential_match)
                        request_listing = user_listing
                        offer_listing = potential_match
                    else:
                        score = calculate_match_score(potential_match, user_listing)
                        request_listing = potential_match
                        offer_listing = user_listing
                    
                except Exception as e:
                    continue
                
                if score >= 30:  # Lower threshold to include partial time matches
                    overlap = calculate_availability_overlap(
                        request_listing['availability'],
                        offer_listing['availability']
                    )
                    
                    distance = calculate_distance(
                        request_listing['location'],
                        offer_listing['location']
                    )
                    
                    time_explanation = get_time_compatibility_explanation(
                        request_listing['availability'],
                        offer_listing['availability']
                    )
                    
                    all_matches.append({
                        "request_listing": request_listing,
                        "offer_listing": offer_listing,
                        "match_score": round(score, 2),
                        "distance_km": round(distance, 2) if distance else None,
                        "availability_overlap": overlap,
                        "time_compatibility": time_explanation
                    })
        
        # Sort by match score
        all_matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return {"matches": all_matches[:20]}  # Return top 20 matches
        
    finally:
        conn.close()

@app.post("/matches/create/")
def create_match(request_listing_id: int, offer_listing_id: int):
    """Create a match between a request and offer listing"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verify both listings exist and are of correct types
        cursor.execute("""
            SELECT l1.listing_id, l1.user_id, l1.type, s1.name,
                   l1.availability, l1.location,
                   l2.listing_id, l2.user_id, l2.type, s2.name,
                   l2.availability, l2.location
            FROM listings l1
            JOIN skills s1 ON l1.skill_id = s1.skill_id
            JOIN listings l2 ON l2.listing_id = ?
            JOIN skills s2 ON l2.skill_id = s2.skill_id
            WHERE l1.listing_id = ? AND l1.status = 'active' AND l2.status = 'active'
        """, (offer_listing_id, request_listing_id))
        
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="One or both listings not found or inactive")
        
        req_id, req_user, req_type, req_skill, req_avail, req_loc, \
        off_id, off_user, off_type, off_skill, off_avail, off_loc = result
        
        if req_type != "request" or off_type != "offer":
            raise HTTPException(status_code=400, detail="Invalid listing types for matching")
        
        if req_skill != off_skill:
            raise HTTPException(status_code=400, detail="Skills don't match")
        
        # Check if match already exists
        cursor.execute("""
            SELECT match_id FROM matches 
            WHERE listing_request_id = ? AND listing_offer_id = ? 
            AND status != 'declined'
        """, (request_listing_id, offer_listing_id))
        
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Match already exists")
        
        # Calculate match score
        request_listing = {
            "skill_name": req_skill, "availability": req_avail, "location": req_loc
        }
        offer_listing = {
            "skill_name": off_skill, "availability": off_avail, "location": off_loc
        }
        
        match_score = calculate_match_score(request_listing, offer_listing)
        
        # Create the match
        cursor.execute("""
            INSERT INTO matches (listing_request_id, listing_offer_id, match_score, status)
            VALUES (?, ?, ?, 'pending')
        """, (request_listing_id, offer_listing_id, match_score))
        
        match_id = cursor.lastrowid
        conn.commit()
        
        return {
            "message": "Match created successfully",
            "match_id": match_id,
            "match_score": round(match_score, 2)
        }
        
    finally:
        conn.close()

@app.get("/matches/")
def get_user_matches(user_id: int):
    """Get all matches for a user"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT m.match_id, m.match_score, m.status, m.created_at,
                   lr.listing_id as req_id, lr.description as req_desc, ur.full_name as req_user,
                   lo.listing_id as off_id, lo.description as off_desc, uo.full_name as off_user,
                   s.name as skill_name
            FROM matches m
            JOIN listings lr ON m.listing_request_id = lr.listing_id
            JOIN listings lo ON m.listing_offer_id = lo.listing_id
            JOIN users ur ON lr.user_id = ur.user_id
            JOIN users uo ON lo.user_id = uo.user_id
            JOIN skills s ON lr.skill_id = s.skill_id
            WHERE lr.user_id = ? OR lo.user_id = ?
            ORDER BY m.created_at DESC
        """, (user_id, user_id))
        
        matches = []
        for row in cursor.fetchall():
            matches.append({
                "match_id": row[0],
                "match_score": row[1],
                "status": row[2],
                "created_at": row[3],
                "request": {
                    "listing_id": row[4],
                    "description": row[5],
                    "user_name": row[6]
                },
                "offer": {
                    "listing_id": row[7],
                    "description": row[8],
                    "user_name": row[9]
                },
                "skill_name": row[10]
            })
        
        return {"matches": matches}
        
    finally:
        conn.close()

@app.put("/matches/{match_id}/status/")
def update_match_status(match_id: int, status: str, user_id: int):
    """Update match status (accept, decline, complete)"""
    if status not in ["accepted", "declined", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verify user is part of this match
        cursor.execute("""
            SELECT lr.user_id, lo.user_id 
            FROM matches m
            JOIN listings lr ON m.listing_request_id = lr.listing_id
            JOIN listings lo ON m.listing_offer_id = lo.listing_id
            WHERE m.match_id = ?
        """, (match_id,))
        
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Match not found")
        
        req_user_id, off_user_id = result
        if user_id not in (req_user_id, off_user_id):
            raise HTTPException(status_code=403, detail="Not authorized to update this match")
        
        # Update status
        cursor.execute("""
            UPDATE matches SET status = ? WHERE match_id = ?
        """, (status, match_id))
        
        conn.commit()
        
        return {"message": f"Match status updated to {status}"}
        
    finally:
        conn.close()