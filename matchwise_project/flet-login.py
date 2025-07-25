import flet as ft
import requests
import subprocess
import sys
from flet_dashboard import show_dashboard

def main(page: ft.Page):
    page.title = "User Login"

    # Input fields
    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True)
    output = ft.Text()

    # Register Button Action
    def open_register(e):
        subprocess.Popen([sys.executable, "flet-register.py"])
        sys.exit()

    # Login Button Action
    def login_user(e):
    # 1) build your payload
        login_data = {
            "username": username.value,
            "password": password.value
    }

        try:
        # 2) POST to /login/
            response = requests.post("http://127.0.0.1:8000/login/", json=login_data)
            response.raise_for_status()
            result = response.json()
            full_name = result["full_name"]
            user_id   = result["user_id"]

        # 3) fetch skills
            skills_resp = requests.get(f"http://127.0.0.1:8000/users/{user_id}/skills")
            current_skills = skills_resp.json().get("skills", []) if skills_resp.status_code == 200 else []

        # 4) fetch availability
            availability_resp = requests.get(f"http://127.0.0.1:8000/users/{user_id}/availability")
            existing_slots = availability_resp.json().get("availability", []) \
                            if availability_resp.headers.get("content-type","").startswith("application/json") \
                            else []

        # 5) now call dashboard with both lists in hand
            show_dashboard(page, full_name, user_id, current_skills, existing_slots)

        except requests.HTTPError:
            detail = response.json().get("detail","Invalid credentials")
            output.value = f"❌ {detail}"
            page.update()
        except Exception as ex:
            output.value = f"⚠️ Connection failed: {ex}"
            page.update()

    # Login Button
    login_btn = ft.ElevatedButton(text="Login", on_click=login_user)

    # Layout
    page.add(
        ft.Container(
            content=ft.Column([
                username,
                password,
                login_btn,
                output,
                ft.TextButton(text="Create a new account", on_click=open_register)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True
        )
    )

ft.app(target=main)
