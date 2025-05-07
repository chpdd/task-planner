from fastapi import APIRouter
from sqlalchemy import select

from src.database import db_dep

router = APIRouter(prefix="/users", tags=["Users"])
