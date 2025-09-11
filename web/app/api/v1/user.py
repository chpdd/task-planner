from fastapi import APIRouter
from sqlalchemy import select

from app.api.dependencies import db_dep, user_id_dep, admin_id_dep
from app.models import User
from app.schemas.user import UserSchema, AdminSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def list_users(session: db_dep, user_id: admin_id_dep):
    request = select(User)
    users = (await session.execute(request)).scalars()
    return [AdminSchema.model_validate(user) for user in users]


@router.get("/me")
async def actual_user(session: db_dep, user_id: user_id_dep):
    user = await session.get(User, user_id)
    return UserSchema.model_validate(user)
