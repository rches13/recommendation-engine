from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class UserOut(BaseModel):
    id: str
    name: str


class InteractionIn(BaseModel):
    course_id: str
    rating: float = Field(..., ge=1, le=5)


class InteractionOut(BaseModel):
    user_id: str
    course_id: str
    rating: float


class RecommendationOut(BaseModel):
    course_id: str
    title: str
    category: str
    tags: list[str]
    score: float


class CourseOut(BaseModel):
    id: str
    title: str
    category: str
    tags: list[str]
