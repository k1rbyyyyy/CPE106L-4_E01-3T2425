import flet as ft
import requests
import subprocess
import sys
from flet_dashboard import show_dashboard  # Ensure this file exists

def main(page: ft.Page):
    page.title = "User Login"

    # Define fields at the top
    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True)
    output = ft.Text()

    # Open Register UI
    def open_register(e):
        subprocess.Popen([sys.executable, "flet-register.py"])
        sys.exit()

    # Handle Login
    def login_user(e):
        data = {
            "username": username.value,
            "password": password.value
        }

        try:
            response = requests.post("http://127.0.0.1:8000/login/", json=data)
            if response.status_code == 200:
                result = response.json()
                full_name = result["full_name"]
                user_id = result["user_id"]

                # Fetch current skills
                skills_resp = requests.get(f"http://127.0.0.1:8000/users/{user_id}/skills")
                if skills_resp.status_code == 200:
                    current_skills = skills_resp.json().get("skills", [])
                else:
                    current_skills = []

                show_dashboard(page, full_name, user_id, current_skills)

            else:
                output.value = f"❌ Error: {response.json().get('detail', 'Invalid credentials')}"

        except Exception as ex:
            output.value = f"⚠️ Connection failed: {ex}"

        page.update()

    # Add elements to the page
    login_btn = ft.ElevatedButton(text="Login", on_click=login_user)

    page.add(
        ft.Column([
            username,
            password,
            login_btn,
            output,
            ft.TextButton(text="Create a new account", on_click=open_register)
        ])
    )

# Run app
ft.app(target=main)
