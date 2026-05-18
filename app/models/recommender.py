"""
Collaborative filtering engine using cosine similarity on a user-item matrix.
"""

from collections import defaultdict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class CollaborativeFilter:
    def __init__(self):
        # user_id -> {course_id: rating}
        self._interactions: dict[str, dict[str, float]] = defaultdict(dict)
        self._course_ids: list[str] = []
        self._user_ids: list[str] = []
        self._matrix: np.ndarray | None = None
        self._dirty = True

    def record(self, user_id: str, course_id: str, rating: float) -> None:
        self._interactions[user_id][course_id] = rating
        self._dirty = True

    def _rebuild(self) -> None:
        self._user_ids = sorted(self._interactions.keys())
        course_set: set[str] = set()
        for ratings in self._interactions.values():
            course_set.update(ratings.keys())
        self._course_ids = sorted(course_set)

        n_users = len(self._user_ids)
        n_courses = len(self._course_ids)
        course_idx = {c: i for i, c in enumerate(self._course_ids)}

        matrix = np.zeros((n_users, n_courses))
        for u_idx, uid in enumerate(self._user_ids):
            for cid, rating in self._interactions[uid].items():
                if cid in course_idx:
                    matrix[u_idx, course_idx[cid]] = rating

        self._matrix = matrix
        self._dirty = False

    def recommend(self, user_id: str, top_n: int = 5) -> list[dict]:
        if self._dirty:
            self._rebuild()

        if self._matrix is None or len(self._user_ids) < 2:
            return []

        if user_id not in self._user_ids:
            return []

        u_idx = self._user_ids.index(user_id)
        user_vec = self._matrix[u_idx].reshape(1, -1)

        sims = cosine_similarity(user_vec, self._matrix)[0]
        sims[u_idx] = -1  # exclude self

        # Weight ratings of all other users by similarity score
        seen = set(self._interactions[user_id].keys())
        course_idx = {c: i for i, c in enumerate(self._course_ids)}
        scores: dict[str, float] = defaultdict(float)
        weights: dict[str, float] = defaultdict(float)

        for other_idx, sim in enumerate(sims):
            if sim <= 0:
                continue
            other_uid = self._user_ids[other_idx]
            for cid, rating in self._interactions[other_uid].items():
                if cid not in seen:
                    scores[cid] += sim * rating
                    weights[cid] += sim

        ranked = [
            {"course_id": cid, "score": round(scores[cid] / weights[cid], 3)}
            for cid in scores
            if weights[cid] > 0
        ]
        ranked.sort(key=lambda x: x["score"], reverse=True)
        return ranked[:top_n]

    def user_exists(self, user_id: str) -> bool:
        return user_id in self._interactions

    def interactions_for(self, user_id: str) -> dict[str, float]:
        return dict(self._interactions.get(user_id, {}))
