import flet as ft
import requests


def show_dashboard(page: ft.Page, full_name: str, user_id: int, current_skills: list):
    page.controls.clear()
    page.title = "Dashboard"

    # Welcome Text
    welcome = ft.Text(
        f"👋 Welcome, {full_name}!",
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )

    # Instruction Text
    instructions = ft.Text(
        "Select an action below:",
        size=16,
        text_align=ft.TextAlign.CENTER
    )

    # Action Buttons
    actions = ft.Column(
        [
            ft.ElevatedButton("🔍 View Matches", on_click=lambda e: print("View Matches clicked")),
            ft.ElevatedButton("📤 Create Listing", on_click=lambda e: print("Create Listing clicked")),
            ft.ElevatedButton("📥 My Requests", on_click=lambda e: print("My Requests clicked")),
            ft.ElevatedButton("📈 View Stats", on_click=lambda e: print("View Stats clicked")),
            ft.ElevatedButton("📝 Submit Feedback", on_click=lambda e: print("Submit Feedback clicked")),
            ft.ElevatedButton(
                "🛠️ Skills",
                on_click=lambda e: show_skill_editor(page, user_id, full_name, current_skills)
            ),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Centered layout using Container
    content = ft.Container(
        content=ft.Column(
            [welcome, instructions, actions],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
    )

    page.add(content)
    page.update()


def show_skill_editor(page: ft.Page, user_id: int, full_name: str, current_skills: list):
    page.controls.clear()
    page.title = "Edit Skills"

    # Define skill options
    skill_options = [
        ft.dropdown.Option("Cooking"),
        ft.dropdown.Option("Tutoring"),
        ft.dropdown.Option("Programming"),
        ft.dropdown.Option("Plumbing"),
        ft.dropdown.Option("Driving"),
        ft.dropdown.Option("Cleaning"),
        ft.dropdown.Option("Gardening"),
        ft.dropdown.Option("Nursing"),
        ft.dropdown.Option("Carpentry")
    ]

    # Create 5 dropdowns prefilled with current skills
    dropdowns = [
        ft.Dropdown(
            label=f"Skill {i+1}",
            options=skill_options,
            value=current_skills[i] if i < len(current_skills) else None
        )
        for i in range(5)
    ]

    status_text = ft.Text()

    def save_skills(e):
        selected = list({d.value for d in dropdowns if d.value})
        if not selected:
            status_text.value = "⚠️ Select at least one skill."
        else:
            try:
                response = requests.post(
                    f"http://127.0.0.1:8000/login/?user_id={user_id}",
                    json=selected
                )
                if response.status_code == 200:
                    status_text.value = "✅ Skills updated!"
                    show_dashboard(page, full_name, user_id, selected)
                else:
                    status_text.value = f"❌ {response.json().get('detail', 'Update failed')}"
            except Exception as ex:
                status_text.value = f"⚠️ Server error: {ex}"
        page.update()

    page.add(
        ft.Column([
            ft.Text("🎯 Edit Your Skills (up to 5)", size=20, weight=ft.FontWeight.BOLD),
            *dropdowns,
            ft.ElevatedButton("💾 Save Skills", on_click=save_skills),
            status_text
        ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    page.update()

