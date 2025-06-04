from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src import security
from src.api.dependencies import user_id_dep, admin_id_dep, db_dep

from src.models import User
from src.crud import user_crud
from src.schemas import auth

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register_user(auth_schema: auth.AuthSchema, session: db_dep):
    user_schema = await user_crud.schema_get_by_name(session, auth_schema.name)
    if user_schema is None:
        raise HTTPException(detail="This username is already taken", status_code=status.HTTP_409_CONFLICT)
    hashed_password = security.hash_password(auth_schema.password)
    user = User(hashed_password=hashed_password, name=auth_schema.name)
    await user_crud.create(session, user)
    await session.commit()
    return security.create_access_token(security.FullPayload(sub=str(user_schema.id)))


@router.post("/login")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: db_dep):
    user = await user_crud.get_by_name(session, form_data.username)
    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this name and password not found")
    return security.create_access_token(security.FullPayload(sub=str(user.id)))
