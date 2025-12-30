from fastapi import FastAPI

from app.api import api_router
from app.core.middleware import middleware

app = FastAPI(middleware=middleware)
app.include_router(api_router)
