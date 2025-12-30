from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.dependencies import get_db, get_user_id, get_admin_id

from app.models import User
from app.schemas.user import UserSchema, AdminSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def list_users(session: AsyncSession = Depends(get_db), user_id: int = Depends(get_admin_id)):
    request = select(User)
    users = (await session.execute(request)).scalars()
    return [AdminSchema.model_validate(user) for user in users]


@router.get("/me")
async def actual_user(session: AsyncSession = Depends(get_db), user_id: int = Depends(get_user_id)):
    user = await session.get(User, user_id)
    return UserSchema.model_validate(user)
