import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ✅ 1. Home page loads
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


# ✅ 2. Valid form submission
def test_valid_submission(client):
    response = client.post("/", data={
        "name": "Vimal",
        "age": "25",
        "weight": "70",
        "program": "Fat Loss (FL)",
        "adherence": "80"
    })
    assert response.status_code == 200
    assert b"Vimal" in response.data


# ✅ 3. Program workout + diet rendering
def test_program_content(client):
    response = client.post("/", data={
        "name": "Test",
        "age": "30",
        "weight": "80",
        "program": "Muscle Gain (MG)",
        "adherence": "90"
    })

    assert b"Squat" in response.data   # workout check
    assert b"Eggs" in response.data    # diet check


# ✅ 4. Calories calculation
def test_calorie_calculation(client):
    response = client.post("/", data={
        "name": "CalTest",
        "age": "28",
        "weight": "70",
        "program": "Fat Loss (FL)",
        "adherence": "75"
    })

    # 70 * 22 = 1540
    assert b"1540" in response.data


# ✅ 5. Missing name (should not break)
def test_missing_name(client):
    response = client.post("/", data={
        "age": "25",
        "weight": "70",
        "program": "Fat Loss (FL)"
    })
    assert response.status_code == 200


# ✅ 6. Invalid program (edge case)
def test_invalid_program(client):
    response = client.post("/", data={
        "name": "Invalid",
        "age": "25",
        "weight": "70",
        "program": "Unknown",
        "adherence": "50"
    })
    assert response.status_code == 200


# ✅ 7. Multiple clients added
def test_multiple_clients(client):
    client.post("/", data={
        "name": "User1",
        "age": "25",
        "weight": "70",
        "program": "Fat Loss (FL)",
        "adherence": "80"
    })

    response = client.post("/", data={
        "name": "User2",
        "age": "30",
        "weight": "80",
        "program": "Muscle Gain (MG)",
        "adherence": "90"
    })

    assert b"User1" in response.data
    assert b"User2" in response.data


# ✅ 8. Zero weight edge case
def test_zero_weight(client):
    response = client.post("/", data={
        "name": "Zero",
        "age": "20",
        "weight": "0",
        "program": "Beginner (BG)",
        "adherence": "50"
    })

    assert response.status_code == 200


# ✅ 9. Adherence boundary values
def test_adherence_bounds(client):
    response = client.post("/", data={
        "name": "Max",
        "age": "25",
        "weight": "70",
        "program": "Fat Loss (FL)",
        "adherence": "100"
    })

    assert b"Max" in response.data


# ✅ 10. GET request after POST (state persistence)
def test_get_after_post(client):
    client.post("/", data={
        "name": "Persist",
        "age": "25",
        "weight": "70",
        "program": "Fat Loss (FL)",
        "adherence": "80"
    })

    response = client.get("/")
    assert b"Persist" in response.data