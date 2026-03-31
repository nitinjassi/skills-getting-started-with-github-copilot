from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "index.html" in response.url.path


def test_get_activities_returns_activity_list():
    response = client.get("/activities")
    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()


def test_signup_for_activity_adds_participant():
    activity_name = "Chess Club"
    email = "test.user@example.com"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_for_invalid_activity_returns_404():
    response = client.post("/activities/Nonexistent/signup", params={"email": "test.user@example.com"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
