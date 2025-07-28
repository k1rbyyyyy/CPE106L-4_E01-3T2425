import requests

API_BASE_URL = "http://127.0.0.1:8000"

def process_registration(full_name, username, password, email, location, skills, availability):
    """
    Sends user registration data to the backend API.

    Args:
        All arguments are strings or lists of strings from the UI form.

    Returns:
        dict: A dictionary containing the registration status.
              e.g., {"success": True, "message": "✅ Registered successfully!"}
    """
    payload = {
        "full_name": full_name,
        "username": username,
        "password": password,
        "email": email,
        "location": location,
        "skills": skills,
        "availability": availability
    }

    try:
        resp = requests.post(f"{API_BASE_URL}/register/", json=payload)
        # Check if the request was successful
        if resp.status_code == 200:
            return {"success": True, "message": "✅ Registered successfully!"}
        else:
            # Get the error detail from the server's JSON response
            error_detail = resp.json().get('detail', 'An unknown error occurred.')
            return {"success": False, "message": f"❌ {error_detail}"}

    except requests.RequestException as ex:
        # Handle connection errors
        return {"success": False, "message": f"⚠️ Connection failed: {ex}"}