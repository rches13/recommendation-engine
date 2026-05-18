import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
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
