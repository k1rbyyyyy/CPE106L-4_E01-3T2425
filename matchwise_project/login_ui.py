import flet as ft
import subprocess
import sys
from login_data import authenticate_and_get_data
from flet_dashboard import show_dashboard

def main(page: ft.Page):
    page.title = "User Login"
    username_field = ft.TextField(label="Username", width=300, autofocus=True)
    password_field = ft.TextField(label="Password", password=True, width=300, can_reveal_password=True)
    status_output = ft.Text()

    def open_register(e):
        subprocess.Popen([sys.executable, "register_ui.py"])
        sys.exit()

    def attempt_login(e):
        result = authenticate_and_get_data(username_field.value, password_field.value)
        if result.get("success"):
            # The call to show_dashboard is simplified
            show_dashboard(
                page=page,
                full_name=result["full_name"],
                user_id=result["user_id"],
                location=result["location"]
            )
        else:
            status_output.value = result.get("error_message", "An unknown error occurred.")
            page.update()

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Text("Welcome to MatchWise! Please Log in:", size=16, weight=ft.FontWeight.BOLD),
                    username_field,
                    password_field,
                    ft.ElevatedButton("Login", on_click=attempt_login, width=300),
                    status_output,
                    ft.TextButton("Create a new account", on_click=open_register)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                width=400
            ),
        )
    )

if __name__ == "__main__":
    ft.app(target=main)