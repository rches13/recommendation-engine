# Recommendation Engine

A real-time learning-path recommendation API built with **FastAPI** and **collaborative filtering**. Given a learner's course interaction history, it identifies users with similar learning patterns and recommends courses they've engaged with that the target user hasn't seen yet.

Built as part of the Marvel AI ecosystem to personalise learning paths and career pathways.

---

## How it works

1. Users log interactions (course completions / ratings) via the REST API.
2. The engine builds a **user × course** rating matrix from all interactions.
3. **Cosine similarity** is computed between users to find the closest learners.
4. Courses rated highly by similar users — but not yet seen by the target user — are ranked by a weighted average score and returned.

```
User A ──► rated [Python, FastAPI, SQL]
User B ──► rated [Python, FastAPI, Docker]   ← similar to A
                                               ► recommend Docker to A
```

---

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI + Uvicorn |
| ML | scikit-learn (cosine similarity), NumPy |
| Validation | Pydantic v2 |
| Tests | pytest + HTTPX |
| Container | Docker |

---

## Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload

# Open interactive docs
open http://localhost:8000/docs
```

### Docker

```bash
docker build -t recommendation-engine .
docker run -p 8000:8000 recommendation-engine
```

---

## API overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/courses` | List all available courses |
| `GET` | `/courses/{id}` | Get a single course |
| `POST` | `/users` | Create a user |
| `GET` | `/users/{id}` | Get a user |
| `POST` | `/users/{id}/interactions` | Log a course interaction (rating 1–5) |
| `GET` | `/users/{id}/interactions` | Get a user's interaction history |
| `GET` | `/users/{id}/recommendations` | Get personalised course recommendations |

Full interactive docs available at `/docs` (Swagger UI) and `/redoc`.

---

## Example

```bash
# Create a user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'
# → {"id": "a1b2c3d4", "name": "Alice"}

# Log interactions
curl -X POST http://localhost:8000/users/a1b2c3d4/interactions \
  -H "Content-Type: application/json" \
  -d '{"course_id": "c001", "rating": 5}'

curl -X POST http://localhost:8000/users/a1b2c3d4/interactions \
  -H "Content-Type: application/json" \
  -d '{"course_id": "c004", "rating": 4}'

# Get recommendations
curl http://localhost:8000/users/a1b2c3d4/recommendations
```

---

## Frontend

A React demo UI lives in `frontend/`. It lets you create a user, rate courses, and watch recommendations update in real time.

```bash
# Start the API first
uvicorn app.main:app --reload

# In a second terminal
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

---

## Running tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

---

## Project structure

```
recommendation-engine/
├── app/
│   ├── main.py              # FastAPI app + lifespan
│   ├── state.py             # Shared in-memory state + seed loader
│   ├── data/
│   │   └── seed_data.py     # Course catalogue + historical interactions
│   ├── models/
│   │   └── recommender.py   # Collaborative filtering engine
│   ├── routes/
│   │   ├── courses.py
│   │   ├── recommendations.py
│   │   └── users.py
│   └── schemas/
│       └── schemas.py       # Pydantic request/response models
├── tests/
│   └── test_recommendations.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── index.css
│   │   └── components/
│   │       ├── CourseCard.jsx
│   │       ├── RecommendationList.jsx
│   │       ├── StarRating.jsx
│   │       └── UserSetup.jsx
│   └── package.json
├── Dockerfile
├── requirements.txt
└── requirements-dev.txt
```
