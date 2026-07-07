import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

# Shared test data dictionary (Acts like Postman Collection Variables)
@pytest.fixture(scope="module")
def suite_context():
    return {
        "auth_token": None,
        "booking_id": None
    }

# 1. TEST: Create Auth Token (POST)
def test_create_token(suite_context):
    url = f"{BASE_URL}/auth"
    payload = {
        "username": "admin",
        "password": "password123"
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    
    # Assertions (Equivalents of pm.test)
    assert response.status_code == 200
    assert "token" in response.json()
    
    # Save token dynamically for later tests
    suite_context["auth_token"] = response.json()["token"]


# 2. TEST: Create Booking (POST)
def test_create_booking(suite_context):
    url = f"{BASE_URL}/booking"
    payload = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-01-01",
            "checkout": "2027-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "bookingid" in data
    assert data["booking"]["firstname"] == "Jim"
    
    # Save booking ID dynamically
    suite_context["booking_id"] = data["bookingid"]


# 3. TEST: Get Booking Details (GET)
def test_get_booking(suite_context):
    booking_id = suite_context["booking_id"]
    url = f"{BASE_URL}/booking/{booking_id}"
    headers = {"Accept": "application/json"}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["firstname"] == "Jim"
    assert data["lastname"] == "Brown"


# 4. TEST: Update Booking (PUT)
def test_update_booking(suite_context):
    booking_id = suite_context["booking_id"]
    token = suite_context["auth_token"]
    
    url = f"{BASE_URL}/booking/{booking_id}"
    payload = {
        "firstname": "James",
        "lastname": "Brown",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-01-01",
            "checkout": "2027-01-01"
        },
        "additionalneeds": "Dinner"
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}" # Passing dynamic token in header
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    assert response.status_code == 200
    assert response.json()["firstname"] == "James"
    assert response.json()["totalprice"] == 150


# 5. TEST: Delete Booking (DELETE)
def test_delete_booking(suite_context):
    booking_id = suite_context["booking_id"]
    token = suite_context["auth_token"]
    
    url = f"{BASE_URL}/booking/{booking_id}"
    headers = {"Cookie": f"token={token}"}
    
    response = requests.delete(url, headers=headers)
    
    # Restful-booker returns 201 for successful deletion
    assert response.status_code == 201