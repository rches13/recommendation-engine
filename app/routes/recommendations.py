from fastapi import APIRouter, HTTPException
from app.schemas.schemas import InteractionIn, InteractionOut, RecommendationOut
from app.state import cf, users, courses_by_id

router = APIRouter(prefix="/users/{user_id}", tags=["recommendations"])


@router.post("/interactions", response_model=InteractionOut, status_code=201)
def add_interaction(user_id: str, body: InteractionIn):
    if not cf.user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if body.course_id not in courses_by_id:
        raise HTTPException(status_code=404, detail="Course not found")

    cf.record(user_id, body.course_id, body.rating)
    return InteractionOut(user_id=user_id, course_id=body.course_id, rating=body.rating)


@router.get("/interactions")
def get_interactions(user_id: str):
    if not cf.user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return cf.interactions_for(user_id)


@router.get("/recommendations", response_model=list[RecommendationOut])
def get_recommendations(user_id: str, top_n: int = 5):
    if not cf.user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")

    raw = cf.recommend(user_id, top_n=top_n)
    results = []
    for item in raw:
        course = courses_by_id.get(item["course_id"])
        if course:
            results.append(RecommendationOut(
                course_id=course["id"],
                title=course["title"],
                category=course["category"],
                tags=course["tags"],
                score=item["score"],
            ))
    return results
