from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.schemas.user import CreateUserSchema, UserSchema
from src.models import User
from src.crud import SchemaCRUD


class UserCRUD(SchemaCRUD[User, CreateUserSchema, UserSchema]):
    pass


user_crud = UserCRUD(User, CreateUserSchema, UserSchema)