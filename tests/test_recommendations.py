import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.state import load_seed_data, cf, users, courses_by_id


@pytest.fixture(autouse=True)
def seed():
    cf._interactions.clear()
    users.clear()
    load_seed_data()


client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "recommendation-engine"


def test_list_courses():
    r = client.get("/courses")
    assert r.status_code == 200
    assert len(r.json()) == 15


def test_get_course():
    r = client.get("/courses/c001")
    assert r.status_code == 200
    assert r.json()["title"] == "Python Fundamentals"


def test_get_course_not_found():
    r = client.get("/courses/c999")
    assert r.status_code == 404


def test_create_user():
    r = client.post("/users", json={"name": "Alice"})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Alice"
    assert "id" in data


def test_get_user():
    created = client.post("/users", json={"name": "Bob"}).json()
    r = client.get(f"/users/{created['id']}")
    assert r.status_code == 200
    assert r.json()["name"] == "Bob"


def test_get_user_not_found():
    r = client.get("/users/doesnotexist")
    assert r.status_code == 404


def test_add_interaction():
    created = client.post("/users", json={"name": "Charlie"}).json()
    uid = created["id"]
    r = client.post(f"/users/{uid}/interactions", json={"course_id": "c001", "rating": 4})
    assert r.status_code == 201
    assert r.json()["rating"] == 4.0


def test_add_interaction_bad_course():
    created = client.post("/users", json={"name": "Dave"}).json()
    uid = created["id"]
    r = client.post(f"/users/{uid}/interactions", json={"course_id": "c999", "rating": 4})
    assert r.status_code == 404


def test_recommendations_returned_for_seed_user():
    r = client.get("/users/u001/recommendations")
    assert r.status_code == 200
    recs = r.json()
    assert len(recs) > 0
    # u001 has rated c001-c005; recommendations should not include those
    seen_by_u001 = {"c001", "c002", "c003", "c004", "c005"}
    for rec in recs:
        assert rec["course_id"] not in seen_by_u001


def test_recommendations_shape():
    r = client.get("/users/u002/recommendations?top_n=3")
    assert r.status_code == 200
    recs = r.json()
    assert len(recs) <= 3
    for rec in recs:
        assert "course_id" in rec
        assert "title" in rec
        assert "score" in rec


def test_recommendations_user_not_found():
    r = client.get("/users/ghost/recommendations")
    assert r.status_code == 404
