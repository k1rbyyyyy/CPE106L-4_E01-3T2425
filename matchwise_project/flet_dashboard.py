import flet as ft
import requests

def show_create_listing_form(page: ft.Page, user_id: int, location: str, full_name: str):
    page.clean()
    page.title = "Create Listing"
    
    try:
        # FIX: The IP address typo is corrected here.
        all_skills_resp = requests.get("http://127.0.0.1:8000/skills/")
        all_skills_resp.raise_for_status()
        all_skills = all_skills_resp.json().get("skills", [])
    except requests.RequestException as e:
        print(f"DEBUG: Could not fetch skills from API. Error: {e}") # Added for debugging
        all_skills = ["Cooking", "Programming", "Cleaning"]

    listing_type_dropdown = ft.Dropdown(label="I want to...", hint_text="Offer or Request a skill?", options=[ft.dropdown.Option("offer"), ft.dropdown.Option("request")])
    skill_dropdown = ft.Dropdown(label="Skill", hint_text="What skill is this for?", options=[ft.dropdown.Option(skill) for skill in all_skills])
    description_field = ft.TextField(label="Description", hint_text="e.g., 'Need help fixing a leaky faucet.'", multiline=True, min_lines=3)
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
        payload = {"user_id": user_id, "type": type_val, "skill": skill_val, "availability": availability_str, "description": desc_val}
        
        try:
            resp = requests.post("http://127.0.0.1:8000/listings/", json=payload)
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
            ft.Row([ft.ElevatedButton("📤 Submit", on_click=submit_listing), ft.ElevatedButton("◀️ Back", on_click=back_to_dashboard)], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            status_text
        ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center, expand=True))
    page.update()

def show_dashboard(page: ft.Page, full_name: str, user_id: int, location: str):
    page.clean()
    page.title = "Dashboard"
    welcome = ft.Text(f"Welcome, {full_name}!", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    instructions = ft.Text("Select an action below:", size=16, text_align=ft.TextAlign.CENTER)
    
    actions = ft.Column([
            ft.ElevatedButton("🔍 View Matches", on_click=lambda e: print("View Matches clicked")),
            ft.ElevatedButton("📤 Create Listing", on_click=lambda e: show_create_listing_form(page, user_id, location, full_name)),
            ft.ElevatedButton("📥 My Requests", on_click=lambda e: print("My Requests clicked")),
            ft.ElevatedButton("📈 View Stats", on_click=lambda e: print("View Stats clicked")),
            ft.ElevatedButton("📝 Submit Feedback", on_click=lambda e: print("Submit Feedback clicked")),
        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    container = ft.Container(content=ft.Column([welcome, instructions, actions], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center, expand=True)
    page.add(container)
    page.update()