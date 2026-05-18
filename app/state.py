"""
Application-level shared state (in-memory for demo).
Initialised once at startup with seed data.
"""

from app.models.recommender import CollaborativeFilter
from app.data.seed_data import COURSES, SEED_INTERACTIONS

cf = CollaborativeFilter()
users: dict[str, dict] = {}
courses_by_id: dict[str, dict] = {c["id"]: c for c in COURSES}


def load_seed_data() -> None:
    for user_id, course_id, rating in SEED_INTERACTIONS:
        users.setdefault(user_id, {"id": user_id, "name": f"Learner {user_id}"})
        cf.record(user_id, course_id, float(rating))
