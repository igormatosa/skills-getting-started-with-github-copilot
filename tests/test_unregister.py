from urllib.parse import quote

from src import app as app_module


def _signup_endpoint(activity_name):
    encoded_name = quote(activity_name, safe="")
    return f"/activities/{encoded_name}/signup"


def test_unregister_succeeds_for_enrolled_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = _signup_endpoint(activity_name)

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_404_for_missing_activity(client):
    # Arrange
    endpoint = _signup_endpoint("Nonexistent Club")
    email = "student@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_non_enrolled_student(client):
    # Arrange
    activity_name = "Debate Team"
    endpoint = _signup_endpoint(activity_name)
    email = "notenrolled@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_returns_422_when_email_missing(client):
    # Arrange
    endpoint = _signup_endpoint("Chess Club")

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 422
