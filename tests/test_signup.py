from urllib.parse import quote

from src import app as app_module


def _signup_endpoint(activity_name):
    encoded_name = quote(activity_name, safe="")
    return f"/activities/{encoded_name}/signup"


def test_signup_succeeds_for_new_student(client):
    # Arrange
    activity_name = "Debate Team"
    email = "newstudent@mergington.edu"
    endpoint = _signup_endpoint(activity_name)

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_for_missing_activity(client):
    # Arrange
    endpoint = _signup_endpoint("Nonexistent Club")
    email = "student@mergington.edu"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_student(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    endpoint = _signup_endpoint(activity_name)

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_400_when_activity_is_full(client):
    # Arrange
    activity_name = "Basketball Team"
    endpoint = _signup_endpoint(activity_name)
    activity = app_module.activities[activity_name]
    activity["participants"] = [
        f"player{i}@mergington.edu" for i in range(activity["max_participants"])
    ]
    email = "lateplayer@mergington.edu"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_signup_returns_422_when_email_missing(client):
    # Arrange
    endpoint = _signup_endpoint("Debate Team")

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 422
