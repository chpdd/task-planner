import jwt
import datetime as dt
import fastapi.security

from passlib.context import CryptContext
from pydantic import Field
from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy import select

from app.core.config import BaseSchema, settings

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="/api/v2/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Header(BaseSchema):
    alg: str = settings.JWT_ALGORITHM
    typ: str = "JWT"


class FullPayload(BaseSchema):
    sub: Annotated[str | None, Field(default=None)]
    exp: Annotated[int | None, Field(default=None)]


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: FullPayload | dict, expires_delta_minutes: int = 30):
    match data:
        case FullPayload(sub=sub) | {"sub": sub}:
            exp = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=expires_delta_minutes)).timestamp()
        case _:
            raise TypeError("Payload must be of type dict with filled data or Payload with filled data")
    full_payload = FullPayload(sub=sub, exp=int(exp))
    access_token = jwt.encode(payload=full_payload.model_dump(), key=settings.JWT_SECRET_KEY,
                              algorithm=settings.JWT_ALGORITHM)

    result = {"access_token": access_token, "token_type": "bearer"}
    return result


def decode_access_token(token):
    decoded_token = jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
    return decoded_token
