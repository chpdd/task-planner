from fastapi import APIRouter
from sqlalchemy import select
from pydantic import Field

from src.database import db_dep
from src.security import actual_user_id_dep
from src.models import User
from src.schemas.user import UserSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def actual_user(session: db_dep, user_id: actual_user_id_dep):
    user = await session.get(User, user_id)
    return UserSchema.model_validate(user)

