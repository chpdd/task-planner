from fastapi import FastAPI

from src.api_routers import api_router

app = FastAPI()
app.include_router(api_router)

