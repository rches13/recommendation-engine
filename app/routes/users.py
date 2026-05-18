import uuid
from fastapi import APIRouter, HTTPException
from app.schemas.schemas import UserCreate, UserOut
from app.state import cf, users

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=201)
def create_user(body: UserCreate):
    user_id = str(uuid.uuid4())[:8]
    users[user_id] = {"id": user_id, "name": body.name}
    cf.record.__func__  # ensure user appears in interactions map
    # seed with an empty entry so user_exists returns True
    cf._interactions[user_id]  # type: ignore[attr-defined]
    return UserOut(id=user_id, name=body.name)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user)
