from fastapi import Depends, APIRouter
from sqlalchemy import select


from src.core.dependencies import db_dep, get_user_id, get_admin_id

from src.models import User
from src.schemas.user import UserSchema, AdminSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def list_users(session: db_dep, user_id: int = Depends(get_admin_id)):
    request = select(User)
    users = (await session.execute(request)).scalars()
    return [AdminSchema.model_validate(user) for user in users]


@router.get("/me")
async def actual_user(session: db_dep, user_id: int = Depends(get_user_id)):
    user = await session.get(User, user_id)
    return UserSchema.model_validate(user)
