import flet as ft
import requests
from flet import Ref

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

    skill_names = ["Cooking","Tutoring","Programming","Plumbing",
                   "Driving","Cleaning","Gardening","Nursing","Carpentry"]

    dropdowns: list[ft.Dropdown] = []
    status_text = ft.Text()

    def update_options(*_):
        selected = {d.value for d in dropdowns if d.value}
        for dd in dropdowns:
            curr = dd.value
            dd.options = [
                ft.dropdown.Option(text=s)
                for s in skill_names
                if s == curr or s not in selected
            ]
        page.update()

    # Build centered rows of Dropdown + Reset
    rows = []
    for i in range(5):
        dd = ft.Dropdown(
            label=f"Skill {i+1}",
            options=[ft.dropdown.Option(text=s) for s in skill_names],
            value=current_skills[i] if i < len(current_skills) else None,
            on_change=update_options
        )
        dropdowns.append(dd)

        def make_reset(dd=dd):
            def _reset(_):
                dd.value = None
                dd.update()
                update_options()
            return _reset

        reset_btn = ft.TextButton("Reset", on_click=make_reset())

        rows.append(
            ft.Row(
                [dd, reset_btn],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def save_skills(e):
        selected = [d.value for d in dropdowns if d.value]
        if not selected:
            status_text.value = "⚠️ Select at least one skill."
            page.update()
            return
        resp = requests.post(
            "http://127.0.0.1:8000/update_skills/",
            params={"user_id": user_id},
            json=selected
        )
        if resp.ok:
            r2 = requests.get(f"http://127.0.0.1:8000/users/{user_id}/skills")
            fresh = r2.json().get("skills", [])
            status_text.value = "✅ Saved!"
            show_skill_editor(page, user_id, fresh, full_name, existing_slots)
            return
        else:
            status_text.value = f"❌ {resp.json().get('detail','Update failed')}"
        page.update()

    def back_to_dashboard(e):
        from flet_dashboard import show_dashboard
        show_dashboard(page, full_name, user_id,
                       [d.value for d in dropdowns if d.value],
                       existing_slots)

    # initial dedupe
    update_options()

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("🎯 Edit Your Skills (up to 5)", size=20, weight=ft.FontWeight.BOLD),
                    *rows,
                    ft.Row([
                        ft.ElevatedButton("💾 Save", on_click=save_skills),
                        ft.ElevatedButton("◀️ Back", on_click=back_to_dashboard),
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                    status_text
                ],
                spacing=12,
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

    days  = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    hours = [str(h) for h in range(24)]

    slot_controls = []
    slot_rows     = []
    status        = ft.Text()

    def make_clear_fn(dc, sc, ec):
        def _clear(_):
            dc.value = None
            sc.value = None
            ec.value = None
            dc.update()
            sc.update()
            ec.update()
        return _clear

    # build up to 3 rows
    for i in range(3):
        d = s = e = None
        if i < len(existing_slots):
            parts = existing_slots[i].split(" ", 1)
            if len(parts) == 2 and "-" in parts[1]:
                d, times = parts
                s, e     = times.split("-", 1)

        dc = ft.Dropdown(label="Day",   options=[ft.dropdown.Option(x) for x in days],   value=d)
        sc = ft.Dropdown(label="Start", options=[ft.dropdown.Option(x) for x in hours], value=s)
        ec = ft.Dropdown(label="End",   options=[ft.dropdown.Option(x) for x in hours], value=e)

        clear_btn = ft.TextButton("Reset", on_click=make_clear_fn(dc, sc, ec))
        slot_controls.append((dc, sc, ec))
        slot_rows.append(
            ft.Row([dc, sc, ec, clear_btn],
                   spacing=10,
                   alignment=ft.MainAxisAlignment.CENTER)
        )

    def save_slots(e):
        slots, errors = [], []
        for idx, (dc, sc, ec) in enumerate(slot_controls, start=1):
            # skip empty rows
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
            # persist to backend
            resp = requests.post(
                "http://127.0.0.1:8000/update_availability/",
                params={"user_id": user_id},
                json=slots
            )
            resp.raise_for_status()

            # re‑fetch current slots
            r2 = requests.get(f"http://127.0.0.1:8000/users/{user_id}/availability")
            r2.raise_for_status()
            updated = r2.json().get("availability", slots)

            # rebuild this editor in place
            status.value = "✅ Saved!"
            show_availability_editor(page, user_id, updated, full_name, current_skills)
            return

        except Exception as ex:
            status.value = f"❌ {ex}"
            page.update()

    def back_to_dashboard(e):
        from flet_dashboard import show_dashboard
        show_dashboard(page, full_name, user_id, current_skills, existing_slots)

    # layout
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("⏰ Edit Your Availability (max 3)", size=20, weight=ft.FontWeight.BOLD),
                    *slot_rows,
                    ft.Row([
                        ft.ElevatedButton("💾 Save", on_click=save_slots),
                        ft.ElevatedButton("◀️ Back to Dashboard", on_click=back_to_dashboard),
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
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
