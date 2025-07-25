import flet as ft
import requests
import subprocess
import sys

def main(page: ft.Page):
    page.title = "User Registration"

    def open_login(e):
        subprocess.Popen([sys.executable, "flet-login.py"])
        sys.exit()

    full_name = ft.TextField(label="Full Name")
    username  = ft.TextField(label="Username")
    password  = ft.TextField(label="Password", password=True)
    email     = ft.TextField(label="Email")
    location  = ft.TextField(label="Location")
    output    = ft.Text()

    skill_options = [
        ft.dropdown.Option(key="Cooking",     text="Cooking"),
        ft.dropdown.Option(key="Tutoring",    text="Tutoring"),
        ft.dropdown.Option(key="Programming", text="Programming"),
        ft.dropdown.Option(key="Plumbing",    text="Plumbing"),
        ft.dropdown.Option(key="Driving",     text="Driving"),
        ft.dropdown.Option(key="Cleaning",    text="Cleaning"),
        ft.dropdown.Option(key="Gardening",   text="Gardening"),
        ft.dropdown.Option(key="Nursing",     text="Nursing"),
        ft.dropdown.Option(key="Carpentry",   text="Carpentry"),
    ]

    skill_dropdowns = [
        ft.Dropdown(label=f"Skill {i+1}", options=skill_options)
        for i in range(5)
    ]

    # 4) Availability selectors
    days  = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    hours = list(range(24))
    day_dropdown   = ft.Dropdown(label="Day",         options=[ft.dropdown.Option(key=d, text=d) for d in days])
    start_dropdown = ft.Dropdown(label="Start Hour",  options=[ft.dropdown.Option(key=str(h), text=str(h)) for h in hours])
    end_dropdown   = ft.Dropdown(label="End Hour",    options=[ft.dropdown.Option(key=str(h), text=str(h)) for h in hours])

    def register_user(e):
        # Gather inputs
        name   = (full_name.value or "").strip()
        user   = (username.value  or "").strip()
        pwd    = (password.value  or "").strip()
        mail   = (email.value     or "").strip()
        loc    = (location.value  or "").strip()
        skills = [d.value for d in skill_dropdowns if d.value]
        avail_list = [f"{day_dropdown.value} {start_dropdown.value}-{end_dropdown.value}"]

        # Validation
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
        elif not skills:
            output.value = "⚠️ Please select at least one skill."
        elif len(skills) != len(set(skills)):
            output.value = "⚠️ You have selected the same skill more than once."
        elif None in (day_dropdown.value, start_dropdown.value, end_dropdown.value):
            output.value = "⚠️ Please select day, start and end hours."
        else:
            payload = {
                "username":    user,
                "password":    pwd,
                "email":       mail,
                "full_name":   name,
                "location":    loc,
                "skills":      skills,
                "availability": avail_list
            }
            try:
                resp = requests.post("http://127.0.0.1:8000/register/", json=payload)
                if resp.status_code == 200:
                    output.value = "✅ Registered successfully!"
                else:
                    output.value = f"❌ {resp.json().get('detail','Unknown error')}"
            except Exception as ex:
                output.value = f"⚠️ Connection failed: {ex}"

        page.update()

    register_btn = ft.ElevatedButton("Register", on_click=register_user)

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column([
                full_name, username, password, email, location,
                ft.Text("Select up to 5 skills:"),
                ft.Row(skill_dropdowns, wrap=True, alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([day_dropdown, start_dropdown, end_dropdown], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                register_btn,
                output,
                ft.TextButton("Already have an account? Login", on_click=open_login)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
        )
    )

ft.app(target=main)
