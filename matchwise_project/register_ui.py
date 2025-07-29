import flet as ft
import subprocess
import sys
import requests
# Import the data logic from our new file
from register_data import process_registration

def main(page: ft.Page):
    page.title = "User Registration"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def open_login(e):
        """Navigate back to login within the same window."""
        page.controls.clear()
        from login_ui import main as login_main
        login_main(page)

    # --- UI Components ---
    full_name_field = ft.TextField(label="Full Name")
    username_field  = ft.TextField(label="Username")
    password_field  = ft.TextField(label="Password", password=True, can_reveal_password=True)
    email_field     = ft.TextField(label="Email")
    location_field  = ft.TextField(label="Location")
    status_output    = ft.Text()

    # Fetch skills from API
    def fetch_skills():
        try:
            response = requests.get("http://127.0.0.1:8000/skills/")
            if response.ok:
                return response.json().get("skills", [])
            else:
                print(f"Failed to fetch skills: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching skills: {e}")
            return []

    # Get all available skills from the database
    all_skills = fetch_skills()
    
    # Fallback to basic skills if API is not available
    if not all_skills:
        all_skills = [
            "Programming", "Web Development", "Cooking", "Tutoring", "Math", 
            "English", "Spanish", "French", "Graphic Design", "Photography",
            "Plumbing", "Carpentry", "Electrical Work", "Gardening", "Cleaning",
            "Music Lessons", "Piano", "Guitar", "Singing", "Dancing",
            "Fitness Training", "Yoga", "Massage Therapy", "Pet Care", "Driving",
            "Writing", "Editing", "Translation", "Data Analysis", "Accounting"
        ]
        status_output.value = "⚠️ Using offline skills list. Start the server for full skill list."
        status_output.color = "orange"
    
    skill_dropdowns = []

    def update_skill_options(*_):
        """Prevents the same skill from being selected twice."""
        selected = {dd.value for dd in skill_dropdowns if dd.value}
        for dd in skill_dropdowns:
            current_val = dd.value
            dd.options = [
                ft.dropdown.Option(s)
                for s in all_skills
                if s == current_val or s not in selected
            ]
        page.update()

    for i in range(5):
        dd = ft.Dropdown(
            label=f"Skill {i+1}",
            options=[ft.dropdown.Option(s) for s in all_skills],
            on_change=update_skill_options
        )
        skill_dropdowns.append(dd)

    days  = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    hours = [str(h) for h in range(24)]
    day_dropdown   = ft.Dropdown(label="Day", options=[ft.dropdown.Option(d) for d in days])
    start_dropdown = ft.Dropdown(label="Start Hour", options=[ft.dropdown.Option(h) for h in hours])
    end_dropdown   = ft.Dropdown(label="End Hour", options=[ft.dropdown.Option(h) for h in hours])

    # --- UI Event Handler ---
    def register_user_clicked(e):
        """Handles the register button click event."""
        # 1. Gather all inputs from the UI fields
        name   = (full_name_field.value or "").strip()
        user   = (username_field.value  or "").strip()
        pwd    = (password_field.value  or "").strip()
        mail   = (email_field.value     or "").strip()
        loc    = (location_field.value  or "").strip()
        skills = [d.value for d in skill_dropdowns if d.value]
        
        # 2. Perform client-side validation
        if not all([name, user, pwd, mail, loc]):
            status_output.value = "⚠️ Please fill all personal detail fields."
            status_output.color = "red"
        elif not skills:
            status_output.value = "⚠️ Please select at least one skill."
            status_output.color = "red"
        elif None in (day_dropdown.value, start_dropdown.value, end_dropdown.value):
            status_output.value = "⚠️ Please select a full availability timeslot."
            status_output.color = "red"
        else:
            # 3. If validation passes, call the data layer
            status_output.value = "🔄 Creating account..."
            status_output.color = "blue"
            page.update()
            
            avail_list = [f"{day_dropdown.value} {start_dropdown.value}-{end_dropdown.value}"]
            result = process_registration(name, user, pwd, mail, loc, skills, avail_list)
            
            if result.get("success", False):
                status_output.value = "✅ Account created successfully! Redirecting to login..."
                status_output.color = "green"
                page.update()
                
                # Wait a moment then redirect to login
                import time
                page.update()
                time.sleep(2)  # Show success message for 2 seconds
                open_login(None)  # Redirect to login
            else:
                status_output.value = result["message"] # Display the error
                status_output.color = "red"

        page.update()

    register_btn = ft.ElevatedButton("Register", on_click=register_user_clicked)

    # --- Page Layout ---
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Create a New Account", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(f"Choose from {len(all_skills)} available skills!", size=14, color="blue"),
                full_name_field, username_field, password_field, email_field, location_field,
                ft.Text("Select up to 5 skills:", weight=ft.FontWeight.BOLD),
                ft.Text("Tip: You can add different skills later in your profile", size=12, color="gray"),
                ft.Row(skill_dropdowns, wrap=True, alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Select your general availability:", weight=ft.FontWeight.BOLD),
                ft.Text("You can create specific time slots for each skill later", size=12, color="gray"),
                ft.Row([day_dropdown, start_dropdown, end_dropdown], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                register_btn,
                status_output,
                ft.TextButton("Already have an account? Login", on_click=open_login)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
            alignment=ft.alignment.center,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)