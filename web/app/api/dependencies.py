from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import datetime as dt

from app.database import get_db
from app.models import User
from app.security import oauth2_scheme, create_access_token, decode_access_token, FullPayload

db_dep = Annotated[AsyncSession, Depends(get_db)]


def get_payload(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = FullPayload(**decode_access_token(token))
    if payload.exp < int(dt.datetime.now(dt.timezone.utc).timestamp()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access token has ended")
    return payload


def get_actual_user_id(payload: Annotated[FullPayload, Depends(get_payload)]):
    return int(payload.sub)


async def only_admin(user_id: Annotated[int, Depends(get_actual_user_id)], session: db_dep):
    user = await session.get(User, user_id)
    if user.is_admin:
        return user_id
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access forbidden. This route is available only for admins.")


payload_dep = Annotated[FullPayload, Depends(get_payload)]
user_id_dep = Annotated[int, Depends(get_actual_user_id)]
admin_id_dep = Annotated[int, Depends(only_admin)]
