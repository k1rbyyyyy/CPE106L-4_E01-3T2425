import flet as ft
import subprocess
import sys
# Import the data logic from our new file
from register_data import process_registration

def main(page: ft.Page):
    page.title = "User Registration"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def open_login(e):
        """Launches the login script."""
        subprocess.Popen([sys.executable, "login_ui.py"]) # Updated to launch the new UI file
        sys.exit()

    # --- UI Components ---
    full_name_field = ft.TextField(label="Full Name")
    username_field  = ft.TextField(label="Username")
    password_field  = ft.TextField(label="Password", password=True, can_reveal_password=True)
    email_field     = ft.TextField(label="Email")
    location_field  = ft.TextField(label="Location")
    status_output    = ft.Text()

    skill_names = [
        "Cooking", "Tutoring", "Programming", "Plumbing", "Driving",
        "Cleaning", "Gardening", "Nursing", "Carpentry"
    ]
    skill_dropdowns = []

    def update_skill_options(*_):
        """Prevents the same skill from being selected twice."""
        selected = {dd.value for dd in skill_dropdowns if dd.value}
        for dd in skill_dropdowns:
            current_val = dd.value
            dd.options = [
                ft.dropdown.Option(s)
                for s in skill_names
                if s == current_val or s not in selected
            ]
        page.update()

    for i in range(5):
        dd = ft.Dropdown(
            label=f"Skill {i+1}",
            options=[ft.dropdown.Option(s) for s in skill_names],
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
        elif not skills:
            status_output.value = "⚠️ Please select at least one skill."
        elif None in (day_dropdown.value, start_dropdown.value, end_dropdown.value):
            status_output.value = "⚠️ Please select a full availability timeslot."
        else:
            # 3. If validation passes, call the data layer
            avail_list = [f"{day_dropdown.value} {start_dropdown.value}-{end_dropdown.value}"]
            result = process_registration(name, user, pwd, mail, loc, skills, avail_list)
            status_output.value = result["message"] # Display the result

        page.update()

    register_btn = ft.ElevatedButton("Register", on_click=register_user_clicked)

    # --- Page Layout ---
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Create a New Account", size=20, weight=ft.FontWeight.BOLD),
                full_name_field, username_field, password_field, email_field, location_field,
                ft.Text("Select up to 5 skills:"),
                ft.Row(skill_dropdowns, wrap=True, alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Select one availability slot:"),
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