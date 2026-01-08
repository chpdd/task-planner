from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import ExpiredSignatureError, InvalidTokenError
from typing import Annotated

from app.core.database import engine, session_factory
from app.models import User
from app.core.security import oauth2_scheme, decode_access_token, FullPayload


async def get_autocommit_conn():
    async with engine.connect() as conn:
        await conn.execution_options(isolation_level="AUTOCOMMIT")

        yield conn


async def get_db():
    async with session_factory() as session:
        yield session


db_dep = Annotated[AsyncSession, Depends(get_db)]


def get_payload(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = FullPayload(**decode_access_token(token))
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access token has ended")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token is invalid")
    return payload


def get_user_id(payload: Annotated[FullPayload, Depends(get_payload)]):
    return int(payload.sub)


user_id_dep = Annotated[int, Depends(get_user_id)]


async def get_admin_id(user_id: user_id_dep, session: db_dep):
    user = await session.get(User, user_id)
    if user.is_admin:
        return user_id
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access forbidden. This route is available only for admins.")


admin_id_dep = Annotated[int, Depends(get_admin_id)]
