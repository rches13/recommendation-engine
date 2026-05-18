from fastapi import APIRouter, HTTPException
from app.schemas.schemas import CourseOut
from app.state import courses_by_id

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[CourseOut])
def list_courses():
    return [CourseOut(**c) for c in courses_by_id.values()]


@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: str):
    course = courses_by_id.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return CourseOut(**course)
