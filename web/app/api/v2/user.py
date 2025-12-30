from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.dependencies import get_db, get_user_id, get_admin_id

from app.crud import user_crud
from app.schemas import user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_mine_user(session: AsyncSession = Depends(get_db), user_id: int = Depends(get_user_id)) -> user.UserSchema:
    return await user_crud.schema_get(session, user_id)


@router.get("")
async def list_users(session: AsyncSession = Depends(get_db),  admin_id: int =  Depends(get_admin_id)) -> list[user.UserSchema]:
    return await user_crud.schema_list(session)


@router.get("/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_db),  admin_id: int =  Depends(get_admin_id)):
    return await user_crud.schema_get(session, user_id)
