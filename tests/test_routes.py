import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ✅ Test home page loads
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


# ✅ Test form submission (POST)
def test_submit_client(client):
    response = client.post("/", data={
        "name": "Vimal",
        "age": "25",
        "weight": "70",
        "program": "Fat Loss (FL)",
        "adherence": "80",
        "notes": "Good progress"
    })

    assert response.status_code == 200
    assert b"Vimal" in response.data


# ✅ Test program selection logic
def test_program_display(client):
    response = client.post("/", data={
        "name": "Test",
        "age": "30",
        "weight": "80",
        "program": "Muscle Gain (MG)",
        "adherence": "90",
        "notes": "Strong"
    })

    assert b"Squat" in response.data  # workout text
    assert b"Eggs" in response.data   # diet text


# ✅ Test empty submission
def test_empty_submission(client):
    response = client.post("/", data={})
    assert response.status_code == 200