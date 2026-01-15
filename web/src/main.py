from fastapi import FastAPI

from src.api import api_router
from src.core.middleware import middleware

app = FastAPI(middleware=middleware)
app.include_router(api_router)
