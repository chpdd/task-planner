from fastapi import Depends, APIRouter


from app.core.dependencies import db_dep, get_user_id, get_admin_id

from app.crud import user_crud
from app.schemas import user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_mine_user(session: db_dep, user_id: int = Depends(get_user_id)) -> user.UserSchema:
    return await user_crud.schema_get(session, user_id)


@router.get("")
async def list_users(session: db_dep,  admin_id: int =  Depends(get_admin_id)) -> list[user.UserSchema]:
    return await user_crud.schema_list(session)


@router.get("/{user_id}")
async def get_user(user_id: int, session: db_dep,  admin_id: int =  Depends(get_admin_id)):
    return await user_crud.schema_get(session, user_id)
