import jwt
import datetime as dt
import fastapi.security

from passlib.context import CryptContext
from pydantic import Field
from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy import select

from src.config import BaseSchema, settings

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Header(BaseSchema):
    alg: str = settings.JWT_ALGORITHM
    typ: str = "JWT"


class Payload(BaseSchema):
    sub: Annotated[str | None, Field(default=None)]
    exp: Annotated[dt.datetime | None, Field(default=None)]


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: Payload | dict, expires_delta_minutes: int | None = 30):
    match data:
        case Payload(sub=None, exp=None) | {}:
            sub = "None"
            exp = dt.datetime.now() + dt.timedelta(minutes=expires_delta_minutes)
        case Payload(sub=sub, exp=None) | {"sub": sub}:
            exp = dt.datetime.now() + dt.timedelta(minutes=expires_delta_minutes)
        case Payload(sub=sub, exp=exp) | {"sub": sub, "exp": exp}:
            ...
        case _:
            raise TypeError("Payload must be of type dict or Payload")
    payload = Payload(sub=sub, exp=exp)
    access_token = jwt.encode(payload=payload.model_dump(), key=settings.JWT_SECRET_KEY,
                              algorithm=settings.JWT_ALGORITHM)
    result = {"access_token": access_token, "token_type": "bearer"}
    return result


def decode_access_token(token):
    return jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
