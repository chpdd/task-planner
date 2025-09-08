from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import user_id_dep, admin_id_dep, db_dep
from src.crud import user_crud
from src.schemas import user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_mine_user(session: db_dep, user_id: user_id_dep) -> user.UserSchema:
    return await user_crud.schema_get(session, user_id)


@router.get("")
async def list_users(session: db_dep, admin_id: admin_id_dep) -> list[user.UserSchema]:
    return await user_crud.schema_list(session)


@router.get("/{user_id}")
async def get_user(user_id: int, session: db_dep, admin_id: admin_id_dep):
    return await user_crud.schema_get(session, user_id)
