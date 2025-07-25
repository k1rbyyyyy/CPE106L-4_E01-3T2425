import flet as ft
import requests
import subprocess
import sys

def main(page: ft.Page):
    page.title = "User Registration"

    def open_login(e):
        subprocess.Popen([sys.executable, "flet-login.py"])
        sys.exit()

    # Form fields
    full_name = ft.TextField(label="Full Name")
    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True)
    email = ft.TextField(label="Email")
    location = ft.TextField(label="Location")
    output = ft.Text()

    # Skills dropdowns (up to 5)
    skill_options = [
        ft.dropdown.Option("Cooking"),
        ft.dropdown.Option("Tutoring"),
        ft.dropdown.Option("Programming"),
        ft.dropdown.Option("Plumbing"),
        ft.dropdown.Option("Driving"),
        ft.dropdown.Option("Cleaning"),
        ft.dropdown.Option("Gardening"),
        ft.dropdown.Option("Nursing"),
        ft.dropdown.Option("Carpentry"),
    ]

    skill_dropdowns = [
        ft.Dropdown(label=f"Skill {i+1}", options=skill_options) for i in range(5)
    ]

    # Availability components
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    hours = list(range(0, 24))
    availability_list = []

    day_dropdown = ft.Dropdown(label="Day", options=[ft.dropdown.Option(day) for day in days])
    start_dropdown = ft.Dropdown(label="Start Hour", options=[ft.dropdown.Option(str(h)) for h in hours])
    end_dropdown = ft.Dropdown(label="End Hour", options=[ft.dropdown.Option(str(h)) for h in hours])
    availability_display = ft.Text()

    def add_availability(e):
        if day_dropdown.value and start_dropdown.value and end_dropdown.value:
            slot = f"{day_dropdown.value} {start_dropdown.value}-{end_dropdown.value}"
            availability_list.append(slot)
            availability_display.value = "Selected: " + ", ".join(availability_list)
            page.update()

    add_avail_btn = ft.ElevatedButton(text="Add Availability", on_click=add_availability)

    # Register handler
    def register_user(e):
        name = (full_name.value or "").strip()
        user = (username.value or "").strip()
        pwd = (password.value or "").strip()
        mail = (email.value or "").strip()
        loc = (location.value or "").strip()
        skill_values = list({d.value for d in skill_dropdowns if d.value})
        availability_str = ",".join(availability_list) if availability_list else ""

        # Validation checks
        if not name:
            output.value = "⚠️ Please enter your full name."
        elif not user:
            output.value = "⚠️ Please enter a username."
        elif not pwd:
            output.value = "⚠️ Please enter a password."
        elif not mail:
            output.value = "⚠️ Please enter an email."
        elif not loc:
            output.value = "⚠️ Please enter a location."
        elif not skill_values:
            output.value = "⚠️ Please select at least one skill."
        elif not availability_str:
            output.value = "⚠️ Please add at least one availability slot."
        else:
            # All fields are valid, proceed with API call
            data = {
                "username": user,
                "password": pwd,
                "email": mail,
                "full_name": name,
                "location": loc,
                "skills": skill_values,
                "availability": availability_str
            }

            try:
                response = requests.post("http://127.0.0.1:8000/register/", json=data)
                if response.status_code == 200:
                    output.value = "✅ Registered successfully!"
                else:
                    output.value = f"❌ Error: {response.json().get('detail', 'Unknown error')}"
            except Exception as ex:
                output.value = f"⚠️ Failed to connect to backend: {ex}"

        page.update()

    register_btn = ft.ElevatedButton(text="Register", on_click=register_user)

    page.add(
        ft.Column([
            full_name,
            username,
            password,
            email,
            location,
            ft.Text("Select up to 5 skills:"),
            ft.Row(skill_dropdowns, wrap=True),
            ft.Text("Availability:"),
            ft.Row([day_dropdown, start_dropdown, end_dropdown]),
            add_avail_btn,
            availability_display,
            register_btn,
            output,
            ft.TextButton(text="Already have an account? Login", on_click=open_login)
        ], scroll=ft.ScrollMode.AUTO)
    )

ft.app(target=main)
