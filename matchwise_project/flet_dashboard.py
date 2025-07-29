import flet as ft
import requests

API_BASE = "http://127.0.0.1:8000"

def show_create_listing_form(page: ft.Page, user_id: int, location: str, full_name: str):
    page.clean()
    page.title = "Create Listing"
    
    try:
        all_skills_resp = requests.get(f"{API_BASE}/skills/")
        all_skills_resp.raise_for_status()
        all_skills = all_skills_resp.json().get("skills", [])
    except requests.RequestException as e:
        print(f"DEBUG: Could not fetch skills from API. Error: {e}")
        all_skills = ["Cooking", "Programming", "Cleaning"]

    listing_type_dropdown = ft.Dropdown(
        label="I want to...", 
        hint_text="Offer or Request a skill?", 
        options=[ft.dropdown.Option("offer"), ft.dropdown.Option("request")]
    )
    skill_dropdown = ft.Dropdown(
        label="Skill", 
        hint_text="What skill is this for?", 
        options=[ft.dropdown.Option(skill) for skill in all_skills]
    )
    description_field = ft.TextField(
        label="Description", 
        hint_text="e.g., 'Need help fixing a leaky faucet.'", 
        multiline=True, 
        min_lines=3
    )
    days  = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    hours = [str(h) for h in range(24)]
    day_dropdown   = ft.Dropdown(label="Day", options=[ft.dropdown.Option(d) for d in days])
    start_dropdown = ft.Dropdown(label="Start Hour", options=[ft.dropdown.Option(h) for h in hours])
    end_dropdown   = ft.Dropdown(label="End Hour", options=[ft.dropdown.Option(h) for h in hours])
    status_text = ft.Text("")

    def submit_listing(e):
        type_val = listing_type_dropdown.value
        skill_val = skill_dropdown.value
        desc_val = description_field.value.strip() if description_field.value else None
        day_val = day_dropdown.value
        start_val = start_dropdown.value
        end_val = end_dropdown.value

        if not all((type_val, skill_val, desc_val, day_val, start_val, end_val)):
            status_text.value = "⚠️ Please fill all fields, including the description."
            status_text.color = "red"
            page.update()
            return
            
        if int(start_val) >= int(end_val):
            status_text.value = "⚠️ End hour must be after start hour."
            status_text.color = "red"
            page.update()
            return

        availability_str = f"{day_val} {start_val}-{end_val}"
        payload = {
            "user_id": user_id, 
            "type": type_val, 
            "skill": skill_val, 
            "availability": availability_str, 
            "description": desc_val
        }
        
        try:
            resp = requests.post(f"{API_BASE}/listings/", json=payload)
            if resp.ok:
                status_text.value = "✅ Listing submitted successfully!"
                status_text.color = "green"
            else:
                status_text.value = f"❌ Error: {resp.json().get('detail', 'Unknown error')}"
                status_text.color = "red"
        except Exception as ex:
            status_text.value = f"❌ Connection Error: {ex}"
            status_text.color = "red"
        
        page.update()

    def back_to_dashboard(e):
        show_dashboard(page, full_name, user_id, location)

    page.add(ft.Container(content=ft.Column([
            ft.Text("📝 Create a New Listing", size=20, weight=ft.FontWeight.BOLD),
            listing_type_dropdown, skill_dropdown, description_field,
            ft.Text("Select availability for this listing:"),
            ft.Row([day_dropdown, start_dropdown, end_dropdown], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.ElevatedButton("📤 Submit", on_click=submit_listing), 
                ft.ElevatedButton("◀️ Back", on_click=back_to_dashboard)
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            status_text
        ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER), 
        alignment=ft.alignment.center, expand=True))
    page.update()

def show_matches(page: ft.Page, user_id: int, full_name: str, location: str):
    page.clean()
    page.title = "My Matches"
    
    matches_container = ft.Column([], spacing=10, expand=True, scroll=ft.ScrollMode.AUTO)
    loading_text = ft.Text("🔍 Loading matches...", text_align=ft.TextAlign.CENTER)
    
    def load_matches():
        try:
            # Get existing matches
            loading_text.value = "🔍 Loading existing matches..."
            page.update()
            
            matches_resp = requests.get(f"{API_BASE}/matches/", params={"user_id": user_id})
            if matches_resp.ok:
                existing_matches = matches_resp.json().get("matches", [])
                loading_text.value = f"✅ Found {len(existing_matches)} existing matches"
            else:
                existing_matches = []
                loading_text.value = f"⚠️ Error loading existing matches: {matches_resp.status_code}"
            
            page.update()
            
            # Find new potential matches for requests
            loading_text.value = "🔍 Finding potential matches for your requests..."
            page.update()
            
            find_resp = requests.post(f"{API_BASE}/matches/find/", json={
                "user_id": user_id,
                "listing_type": "request"
            })
            
            if find_resp.ok:
                potential_matches = find_resp.json().get("matches", [])
                loading_text.value = f"✅ Found {len(potential_matches)} potential request matches"
            else:
                potential_matches = []
                loading_text.value = f"⚠️ Error finding request matches: {find_resp.status_code}"
                
            page.update()
            
            # Also find matches for offers
            loading_text.value = "🔍 Finding potential matches for your offers..."
            page.update()
            
            find_offer_resp = requests.post(f"{API_BASE}/matches/find/", json={
                "user_id": user_id,
                "listing_type": "offer"
            })
            
            if find_offer_resp.ok:
                offer_matches = find_offer_resp.json().get("matches", [])
                potential_matches.extend(offer_matches)
                loading_text.value = f"✅ Total potential matches: {len(potential_matches)}"
            else:
                loading_text.value = f"⚠️ Error finding offer matches: {find_offer_resp.status_code}"
                
            page.update()
            
            matches_container.controls.clear()
            
            if existing_matches:
                matches_container.controls.append(
                    ft.Text("📋 Your Current Matches", size=18, weight=ft.FontWeight.BOLD)
                )
                
                for match in existing_matches:
                    status_color = {
                        "pending": "orange",
                        "accepted": "green", 
                        "declined": "red",
                        "completed": "blue"
                    }.get(match["status"], "gray")
                    
                    match_card = ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(f"🎯 {match['skill_name']}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"📊 Score: {match['match_score']}%"),
                                ft.Text(f"📝 Request: {match['request']['description'][:50]}..."),
                                ft.Text(f"🤝 Offer: {match['offer']['description'][:50]}..."),
                                ft.Text(f"Status: {match['status'].title()}", color=status_color),
                                ft.Row([
                                    ft.ElevatedButton(
                                        "✅ Accept", 
                                        on_click=lambda e, mid=match['match_id']: update_match_status(mid, "accepted")
                                    ) if match['status'] == 'pending' else ft.Container(),
                                    ft.ElevatedButton(
                                        "❌ Decline", 
                                        on_click=lambda e, mid=match['match_id']: update_match_status(mid, "declined")
                                    ) if match['status'] == 'pending' else ft.Container(),
                                    ft.ElevatedButton(
                                        "✅ Complete", 
                                        on_click=lambda e, mid=match['match_id']: update_match_status(mid, "completed")
                                    ) if match['status'] == 'accepted' else ft.Container(),
                                ], spacing=10)
                            ], spacing=5),
                            padding=15
                        )
                    )
                    matches_container.controls.append(match_card)
            
            if potential_matches:
                # Add some spacing before the potential matches section
                matches_container.controls.append(ft.Container(height=20))
                matches_container.controls.append(
                    ft.Text("🔍 Potential New Matches", size=18, weight=ft.FontWeight.BOLD)
                )
                
                for match in potential_matches[:10]:  # Show top 10
                    req_listing = match["request_listing"]
                    off_listing = match["offer_listing"]
                    
                    match_card = ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(f"🎯 {req_listing['skill_name']}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"📊 Match Score: {match['match_score']}%"),
                                ft.Text(f"📍 Distance: {match.get('distance_km', 'Unknown')} km"),
                                ft.Text(f"📝 Request: {req_listing['description'][:50]}..."),
                                ft.Text(f"🤝 Offer: {off_listing['description'][:50]}..."),
                                ft.Text(f"⏰ Overlap: {', '.join(match['availability_overlap']) if match['availability_overlap'] else 'None'}"),
                                ft.ElevatedButton(
                                    "🤝 Create Match", 
                                    on_click=lambda e, req_id=req_listing['listing_id'], off_id=off_listing['listing_id']: 
                                    create_match(req_id, off_id)
                                )
                            ], spacing=5),
                            padding=15
                        )
                    )
                    matches_container.controls.append(match_card)
            
            if not existing_matches and not potential_matches:
                matches_container.controls.append(
                    ft.Text("😔 No matches found. Create some listings first!", 
                           text_align=ft.TextAlign.CENTER, size=16)
                )
                
        except Exception as e:
            matches_container.controls.clear()
            matches_container.controls.append(
                ft.Text(f"❌ Error loading matches: {e}", color="red", text_align=ft.TextAlign.CENTER)
            )
        
        loading_text.value = ""
        page.update()
    
    def update_match_status(match_id: int, status: str):
        try:
            resp = requests.put(f"{API_BASE}/matches/{match_id}/status/", 
                               params={"status": status, "user_id": user_id})
            if resp.ok:
                load_matches()  # Reload matches
            else:
                print(f"Error updating match: {resp.json()}")
        except Exception as e:
            print(f"Error updating match: {e}")
    
    def create_match(req_id: int, off_id: int):
        try:
            resp = requests.post(f"{API_BASE}/matches/create/", 
                               params={"request_listing_id": req_id, "offer_listing_id": off_id})
            if resp.ok:
                load_matches()  # Reload matches
            else:
                print(f"Error creating match: {resp.json()}")
        except Exception as e:
            print(f"Error creating match: {e}")

    def back_to_dashboard(e):
        show_dashboard(page, full_name, user_id, location)

    page.add(ft.Column([
        ft.Row([
            ft.Text("🔍 My Matches", size=24, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("� Refresh", on_click=lambda e: load_matches()),
            ft.ElevatedButton("◀️ Back", on_click=back_to_dashboard)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        loading_text,
        matches_container
    ], expand=True))
    
    page.update()
    load_matches()

def show_my_listings(page: ft.Page, user_id: int, full_name: str, location: str):
    page.clean()
    page.title = "My Listings"
    
    listings_container = ft.Column([], spacing=10, expand=True, scroll=ft.ScrollMode.AUTO)
    
    def load_listings():
        try:
            resp = requests.get(f"{API_BASE}/listings/", params={"user_id": user_id})
            if resp.ok:
                listings = resp.json().get("listings", [])
            else:
                listings = []
            
            listings_container.controls.clear()
            
            if listings:
                for listing in listings:
                    type_icon = "📤" if listing["type"] == "offer" else "📥"
                    type_color = "green" if listing["type"] == "offer" else "blue"
                    
                    listing_card = ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(f"{type_icon} {listing['type'].title()}", 
                                           color=type_color, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"🎯 {listing['skill_name']}", weight=ft.FontWeight.BOLD)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Text(f"📝 {listing['description']}"),
                                ft.Text(f"⏰ {listing['availability']}"),
                                ft.Text(f"📍 {listing['location']}"),
                                ft.Text(f"� Created: {listing['created_at'][:10]}", size=12, color="gray"),
                                ft.Text(f"Status: {listing['status'].title()}", 
                                       color="green" if listing['status'] == 'active' else "gray")
                            ], spacing=5),
                            padding=15
                        )
                    )
                    listings_container.controls.append(listing_card)
            else:
                listings_container.controls.append(
                    ft.Text("📝 No listings yet. Create your first listing!", 
                           text_align=ft.TextAlign.CENTER, size=16)
                )
                
        except Exception as e:
            listings_container.controls.clear()
            listings_container.controls.append(
                ft.Text(f"❌ Error loading listings: {e}", color="red", text_align=ft.TextAlign.CENTER)
            )
        
        page.update()
    
    def back_to_dashboard(e):
        show_dashboard(page, full_name, user_id, location)

    page.add(ft.Column([
        ft.Row([
            ft.Text("📋 My Listings", size=24, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("� Refresh", on_click=lambda e: load_listings()),
            ft.ElevatedButton("◀️ Back", on_click=back_to_dashboard)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        listings_container
    ], expand=True))
    
    page.update()
    load_listings()

def show_dashboard(page: ft.Page, full_name: str, user_id: int, location: str):
    page.clean()
    page.title = "MatchWise Dashboard"
    
    welcome = ft.Text(f"Welcome, {full_name}!", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    instructions = ft.Text("Select an action below:", size=16, text_align=ft.TextAlign.CENTER)
    
    actions = ft.Column([
        ft.ElevatedButton(
            "� View Matches", 
            on_click=lambda e: show_matches(page, user_id, full_name, location),
            width=200,
            height=50
        ),
        ft.ElevatedButton(
            "📤 Create Listing", 
            on_click=lambda e: show_create_listing_form(page, user_id, location, full_name),
            width=200,
            height=50
        ),
        ft.ElevatedButton(
            "� My Listings", 
            on_click=lambda e: show_my_listings(page, user_id, full_name, location),
            width=200,
            height=50
        ),
        ft.ElevatedButton(
            "📊 Browse All Listings", 
            on_click=lambda e: show_browse_listings(page, user_id, full_name, location),
            width=200,
            height=50
        ),
        ft.ElevatedButton(
            "🚪 Logout", 
            on_click=lambda e: logout(page),
            width=200,
            height=50,
            color="red"
        )
    ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    container = ft.Container(
        content=ft.Column([
            welcome, 
            instructions, 
            actions
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), 
        alignment=ft.alignment.center, 
        expand=True
    )
    
    page.add(container)
    page.update()

def show_browse_listings(page: ft.Page, user_id: int, full_name: str, location: str):
    page.clean()
    page.title = "Browse Listings"
    
    # Filter controls
    type_filter = ft.Dropdown(
        label="Type", 
        options=[
            ft.dropdown.Option("", "All"),
            ft.dropdown.Option("offer", "Offers"),
            ft.dropdown.Option("request", "Requests")
        ],
        value=""
    )
    
    skill_filter = ft.TextField(label="Skill (optional)", hint_text="e.g., Programming")
    
    listings_container = ft.Column([], spacing=10, expand=True, scroll=ft.ScrollMode.AUTO)
    
    def load_listings():
        try:
            params = {}
            if type_filter.value:
                params["listing_type"] = type_filter.value
            if skill_filter.value and skill_filter.value.strip():
                params["skill"] = skill_filter.value.strip()
            
            resp = requests.get(f"{API_BASE}/listings/", params=params)
            if resp.ok:
                listings = resp.json().get("listings", [])
                # Filter out user's own listings
                listings = [l for l in listings if l["user_id"] != user_id]
            else:
                listings = []
            
            listings_container.controls.clear()
            
            if listings:
                for listing in listings:
                    type_icon = "📤" if listing["type"] == "offer" else "📥"
                    type_color = "green" if listing["type"] == "offer" else "blue"
                    
                    listing_card = ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(f"{type_icon} {listing['type'].title()}", 
                                           color=type_color, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"🎯 {listing['skill_name']}", weight=ft.FontWeight.BOLD)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Text(f"👤 By: {listing['user_name']}"),
                                ft.Text(f"📝 {listing['description']}"),
                                ft.Text(f"⏰ {listing['availability']}"),
                                ft.Text(f"📍 {listing['location']}"),
                                ft.Text(f"📅 Created: {listing['created_at'][:10]}", size=12, color="gray")
                            ], spacing=5),
                            padding=15
                        )
                    )
                    listings_container.controls.append(listing_card)
            else:
                listings_container.controls.append(
                    ft.Text("📝 No listings found with current filters.", 
                           text_align=ft.TextAlign.CENTER, size=16)
                )
                
        except Exception as e:
            listings_container.controls.clear()
            listings_container.controls.append(
                ft.Text(f"❌ Error loading listings: {e}", color="red", text_align=ft.TextAlign.CENTER)
            )
        
        page.update()
    
    def back_to_dashboard(e):
        show_dashboard(page, full_name, user_id, location)

    page.add(ft.Column([
        ft.Row([
            ft.Text("📊 Browse All Listings", size=24, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("◀️ Back", on_click=back_to_dashboard)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row([
            type_filter,
            skill_filter,
            ft.ElevatedButton("🔍 Filter", on_click=lambda e: load_listings())
        ], spacing=10),
        listings_container
    ], expand=True))
    
    page.update()
    load_listings()

def logout(page: ft.Page):
    page.controls.clear()
    page.title = "MatchWise - Login"
    from login_ui import main as login_main
    login_main(page)