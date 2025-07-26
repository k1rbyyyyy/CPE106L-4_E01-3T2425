import flet as ft
import requests
import subprocess
import sys
from flet_dashboard import show_dashboard

#Login menu---------------------------------------------
import flet as ft
import requests
import subprocess
import sys
from flet_dashboard import show_dashboard

import flet as ft
import requests
import subprocess
import sys
from flet_dashboard import show_dashboard

def main(page: ft.Page):
    page.title = "User Login"

    # Input fields
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", password=True, width=300)
    output = ft.Text()

    def open_register(e):
        subprocess.Popen([sys.executable, "flet-register.py"])
        sys.exit()

    def login_user(e):
        login_data = {"username": username.value, "password": password.value}
        try:
            response = requests.post("http://127.0.0.1:8000/login/", json=login_data)
            response.raise_for_status()
            result = response.json()
            full_name = result["full_name"]
            user_id   = result["user_id"]

            skills_resp = requests.get(f"http://127.0.0.1:8000/users/{user_id}/skills")
            current_skills = skills_resp.json().get("skills", []) if skills_resp.ok else []
            avail_resp = requests.get(f"http://127.0.0.1:8000/users/{user_id}/availability")
            existing_slots = avail_resp.json().get("availability", []) if avail_resp.ok else []

            show_dashboard(page, full_name, user_id, current_skills, existing_slots)

        except requests.HTTPError:
            output.value = "❌ Invalid credentials"
        except Exception as ex:
            output.value = f"⚠️ Connection failed: {ex}"
        page.update()

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Welcome to MatchWise! Please Log in:", size=16, weight=ft.FontWeight.BOLD),
                    username,
                    password,
                    ft.ElevatedButton("Login", on_click=login_user, width=300),
                    output,
                    ft.TextButton("Create a new account", on_click=open_register)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                width=400
            ),
        )
    )

ft.app(target=main)
