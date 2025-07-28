import requests

API_BASE_URL = "http://127.0.0.1:8000"

def authenticate_and_get_data(username, password):
    try:
        login_payload = {"username": username, "password": password}
        response = requests.post(f"{API_BASE_URL}/login/", json=login_payload)
        response.raise_for_status()
        login_result = response.json()

        # No longer fetches availability, as it is not used.
        return {
            "success": True,
            "user_id": login_result["user_id"],
            "full_name": login_result["full_name"],
            "location": login_result.get("location", ""),
        }
    except requests.HTTPError:
        return {"success": False, "error_message": "❌ Invalid credentials"}
    except requests.RequestException as req_err:
        return {"success": False, "error_message": f"⚠️ Connection failed: {req_err}"}