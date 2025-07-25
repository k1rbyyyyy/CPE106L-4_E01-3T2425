import flet as ft
import requests

def show_dashboard(page: ft.Page, full_name: str, user_id: int, current_skills: list, existing_slots: list):
    page.clean()
    page.title = "Dashboard"

    # Welcome Text
    welcome = ft.Text(
        f"Welcome, {full_name}!",
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
            ft.ElevatedButton( "🛠️ Skills",on_click=lambda e: show_skill_editor(page, user_id, current_skills, full_name, existing_slots)),
            ft.ElevatedButton( "⏰ Availability",on_click=lambda e: show_availability_editor(page, user_id, existing_slots, full_name, current_skills)),
        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Create container (only once)
    content = ft.Container(
        content=ft.Column(
            [welcome, instructions, actions],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
    )
    
    # Add to page only once
    page.add(content)
    page.update()

def show_skill_editor(page: ft.Page, user_id: int, current_skills: list, full_name: str, existing_slots: list):
    page.clean()
    page.title = "Edit Skills"

    skill_names = [
        "Cooking", "Tutoring", "Programming", "Plumbing", "Driving",
        "Cleaning", "Gardening", "Nursing", "Carpentry"
    ]

    dropdowns: list[ft.Dropdown] = []
    status_text = ft.Text()

    def update_options(*_):
        selected = {d.value for d in dropdowns if d.value}
        for dd in dropdowns:
            current = dd.value
            dd.options = [
                ft.dropdown.Option(text=s)
                for s in skill_names
                if s == current or s not in selected
            ]
        page.update()

    # build and wire up five dropdowns
    for i in range(5):
        dd = ft.Dropdown(
            label=f"Skill {i+1}",
            options=[ft.dropdown.Option(text=s) for s in skill_names],
            value=current_skills[i] if i < len(current_skills) else None,
            on_change=update_options
        )
        dropdowns.append(dd)

    def save_skills(e):
        selected = [d.value for d in dropdowns if d.value]
        if not selected:
            status_text.value = "⚠️ Select at least one skill."
        else:
            try:
                resp = requests.post(
                    "http://127.0.0.1:8000/update_skills/",
                    params={"user_id": user_id},
                    json=selected
                )
                resp.raise_for_status()
                status_text.value = "✅ Skills updated!"
                show_dashboard(page, full_name, user_id, selected, existing_slots)
            except Exception as ex:
                status_text.value = f"❌ {getattr(ex, 'response', ex)}"
        page.update()

    # initial dedupe
    update_options()

    # **only one** add!
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("🎯 Edit Your Skills (up to 5)", size=20, weight=ft.FontWeight.BOLD),
                    *dropdowns,
                    ft.ElevatedButton("💾 Save Skills", on_click=save_skills),
                    status_text
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            alignment=ft.alignment.center,
            expand=True
        )
    )
    page.update()

    update_options()  # Run initially to remove duplicates from start
    
def show_availability_editor(page, user_id, existing_slots, full_name, current_skills):
    page.clean()
    page.title = "Edit Availability"

    days  = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    hours = [str(h) for h in range(24)]

    slot_controls = []
    slot_rows     = []
    status        = ft.Text()

    # helper to clear exactly that row’s three dropdowns
    def make_clear_fn(ctrls):
        def _clear_row(e):
            for c in ctrls:
                c.value = None
            page.update()
        return _clear_row

    # build up to 3 rows
    for i in range(3):
        # pre‑fill if we have existing data
        day = start = end = None
        if i < len(existing_slots):
            parts = existing_slots[i].split(" ", 1)
            if len(parts) == 2:
                day, times = parts
                if "-" in times:
                    start, end = times.split("-", 1)

        dc = ft.Dropdown(label="Day",   options=[ft.dropdown.Option(d) for d in days],  value=day)
        sc = ft.Dropdown(label="Start", options=[ft.dropdown.Option(h) for h in hours], value=start)
        ec = ft.Dropdown(label="End",   options=[ft.dropdown.Option(h) for h in hours], value=end)

        slot_controls.append((dc, sc, ec))
        clear_btn = ft.TextButton("Remove", on_click=make_clear_fn([dc, sc, ec]))
        slot_rows.append(
            ft.Row([dc, sc, ec, clear_btn],
                   spacing=10,
                   alignment=ft.MainAxisAlignment.CENTER)
        )

        def save(e):
            slots, errors = [], []
            for idx, (dc, sc, ec) in enumerate(slot_controls, start=1):
            # if any field is touched, require all three
                if dc.value or sc.value or ec.value:
                    if not (dc.value and sc.value and ec.value):
                        errors.append(f"Row {idx}: all fields required")
                    else:
                        if int(sc.value) >= int(ec.value):
                            errors.append(f"Row {idx}: end must be after start")
                        else:
                            slots.append(f"{dc.value} {sc.value}-{ec.value}")

            if errors:
                status.value = "\n".join(errors)
                page.update()
                return

            if len(slots) > 3:
                status.value = "Max 3 slots allowed"
                page.update()
                return

        # POST the new slots
            try:
                resp = requests.post(
                    "http://127.0.0.1:8000/update_availability/",
                    params={"user_id": user_id},
                    json=slots
            )
                resp.raise_for_status()
            except Exception as ex:
                status.value = f"⚠️ Network error: {ex}"
                page.update()
                return

        # on success, re‑fetch from the API so we see exactly what’s in the DB
            new_slots = slots
            try:
                r2 = requests.get(f"http://127.0.0.1:8000/users/{user_id}/availability")
                new_slots = r2.json().get("availability", slots)
            except:
                pass

        # finally: pop you back to the dashboard
            show_dashboard(page, full_name, user_id, current_skills, new_slots)

    # only one add:
    page.add(
      ft.Container(
        content=ft.Column(
          [
           ft.Text("⏰ Edit Your Availability (max 3)", size=20, weight=ft.FontWeight.BOLD),
           *slot_rows,
           ft.ElevatedButton("💾 Save Availability", on_click=save),
           status
          ],
          spacing=15,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
      )
    )
    page.update()
