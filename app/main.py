from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.state import load_seed_data
from app.routes import users, courses, recommendations


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_seed_data()
    yield


app = FastAPI(
    title="Recommendation Engine",
    description=(
        "Real-time learning-path recommendation API using collaborative filtering. "
        "Records user interactions with courses and recommends personalised learning paths "
        "based on the behaviour of similar learners."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router)
app.include_router(courses.router)
app.include_router(recommendations.router)


@app.get("/", tags=["health"])
def root():
    return {
        "service": "recommendation-engine",
        "version": "1.0.0",
        "docs": "/docs",
    }
