from fastapi.testclient import TestClient
from src.app import app, activities
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset activities to initial state before each test
    for activity in activities.values():
        activity['participants'].clear()
    activities['Chess Club']['participants'].extend([
        "michael@mergington.edu", "daniel@mergington.edu"
    ])
    activities['Programming Class']['participants'].extend([
        "emma@mergington.edu", "sophia@mergington.edu"
    ])
    activities['Gym Class']['participants'].extend([
        "john@mergington.edu", "olivia@mergington.edu"
    ])
    activities['Basketball Team']['participants'].extend([
        "alex@mergington.edu"
    ])
    activities['Tennis Club']['participants'].extend([
        "sarah@mergington.edu", "james@mergington.edu"
    ])
    activities['Art Studio']['participants'].extend([
        "maya@mergington.edu"
    ])
    activities['Music Ensemble']['participants'].extend([
        "lucas@mergington.edu", "isabella@mergington.edu"
    ])
    activities['Debate Club']['participants'].extend([
        "noah@mergington.edu"
    ])
    activities['Science Lab']['participants'].extend([
        "ava@mergington.edu", "ethan@mergington.edu"
    ])


def test_get_activities():
    # Arrange: None needed, uses fixture
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)


def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert "Signed up" in response.json()["message"]


def test_signup_already_registered():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_success():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    assert "Unregistered" in response.json()["message"]


def test_unregister_not_registered():
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
