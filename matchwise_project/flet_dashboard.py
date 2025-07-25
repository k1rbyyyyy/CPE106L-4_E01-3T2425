import flet as ft
import requests

# ─── Dashboard ────────────────────────────────────────────────────────────────
def show_dashboard(page: ft.Page,
                   full_name: str,
                   user_id: int,
                   current_skills: list,
                   existing_slots: list):
    page.clean()
    page.title = "Dashboard"

    # Welcome + instructions
    welcome = ft.Text(
        f"Welcome, {full_name}!",
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    instructions = ft.Text(
        "Select an action below:",
        size=16,
        text_align=ft.TextAlign.CENTER
    )

    # Action buttons
    actions = ft.Column(
        [
            ft.ElevatedButton("🔍 View Matches", on_click=lambda e: print("View Matches clicked")),
            ft.ElevatedButton("📤 Create Listing", on_click=lambda e: print("Create Listing clicked")),
            ft.ElevatedButton("📥 My Requests", on_click=lambda e: print("My Requests clicked")),
            ft.ElevatedButton("📈 View Stats", on_click=lambda e: print("View Stats clicked")),
            ft.ElevatedButton("📝 Submit Feedback", on_click=lambda e: print("Submit Feedback clicked")),
            ft.ElevatedButton(
                "🛠️ Skills",
                on_click=lambda e: show_skill_editor(page, user_id, current_skills, full_name, existing_slots)
            ),
            ft.ElevatedButton(
                "⏰ Availability",
                on_click=lambda e: show_availability_editor(page, user_id, existing_slots, full_name, current_skills)
            ),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Centered container
    container = ft.Container(
        content=ft.Column(
            [welcome, instructions, actions],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
    )

    page.add(container)
    page.update()

# ─── Skills Editor ───────────────────────────────────────────────────────────
def show_skill_editor(page: ft.Page,
                      user_id: int,
                      current_skills: list,
                      full_name: str,
                      existing_slots: list):
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

    # Build 5 dropdowns
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
            resp = requests.post(
                "http://127.0.0.1:8000/update_skills/",
                params={"user_id": user_id},
                json=selected
            )
            if resp.ok:
                status_text.value = "✅ Skills updated!"
                show_dashboard(page, full_name, user_id, selected, existing_slots)
            else:
                status_text.value = f"❌ {resp.json().get('detail','Update failed')}"
        page.update()

    # Initial dedupe
    update_options()

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("🎯 Edit Your Skills (up to 5)", size=20, weight=ft.FontWeight.BOLD),
                    *dropdowns,
                    ft.ElevatedButton("💾 Save Skills", on_click=save_skills),
                    status_text
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            expand=True
        )
    )
    page.update()

# ─── Availability Editor ──────────────────────────────────────────────────────
def show_availability_editor(page: ft.Page,
                             user_id: int,
                             existing_slots: list,
                             full_name: str,
                             current_skills: list):
    page.clean()
    page.title = "Edit Availability"

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    hours = [str(h) for h in range(24)]

    slot_controls = []
    slot_rows = []
    status = ft.Text()

    # Pad to 3 entries if fewer
    while len(existing_slots) < 3:
        existing_slots.append("")

    def make_reset(refs):
        def _reset(_):
            for ref in refs:
                ref.current.value = ""
                ref.current.update()
        return _reset

    for i in range(3):
        d = s = e = None
        if existing_slots[i]:
            parts = existing_slots[i].split(" ", 1)
            if len(parts) == 2 and "-" in parts[1]:
                d, times = parts
                s, e = times.split("-", 1)

        day_ref = ft.Ref[ft.Dropdown]()
        start_ref = ft.Ref[ft.Dropdown]()
        end_ref = ft.Ref[ft.Dropdown]()

        dc = ft.Dropdown(label="Day", options=[ft.dropdown.Option(x) for x in days], value=d, ref=day_ref)
        sc = ft.Dropdown(label="Start", options=[ft.dropdown.Option(x) for x in hours], value=s, ref=start_ref)
        ec = ft.Dropdown(label="End", options=[ft.dropdown.Option(x) for x in hours], value=e, ref=end_ref)

        clear_btn = ft.TextButton("Reset", on_click=make_reset([day_ref, start_ref, end_ref]))

        slot_controls.append((day_ref, start_ref, end_ref))
        slot_rows.append(
            ft.Row([dc, sc, ec, clear_btn], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        )

    def save(e):
        slots, errors = [], []

        for idx, (day_ref, start_ref, end_ref) in enumerate(slot_controls, start=1):
            dc = day_ref.current
            sc = start_ref.current
            ec = end_ref.current

            if not (dc.value or sc.value or ec.value):
                continue
            if not (dc.value and sc.value and ec.value):
                errors.append(f"Row {idx}: all three fields required")
                continue
            try:
                if int(sc.value) >= int(ec.value):
                    errors.append(f"Row {idx}: end must be after start")
                else:
                    slots.append(f"{dc.value} {sc.value}-{ec.value}")
            except ValueError:
                errors.append(f"Row {idx}: invalid time")

        if errors:
            status.value = "\n".join(errors)
            page.update()
            return

        if len(slots) > 3:
            status.value = "⚠️ Max 3 slots allowed"
            page.update()
            return

        try:
            resp = requests.post(
                "http://127.0.0.1:8000/update_availability/",
                params={"user_id": user_id},
                json=slots
            )
            resp.raise_for_status()
            r2 = requests.get(f"http://127.0.0.1:8000/users/{user_id}/availability")
            r2.raise_for_status()
            updated_slots = r2.json().get("availability", [])
            show_dashboard(page, full_name, user_id, current_skills, updated_slots)

        except requests.RequestException as ex:
            status.value = f"❌ Network error: {str(ex)}"
            page.update()

    # Layout
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
