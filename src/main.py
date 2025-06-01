import uvicorn
from fastapi import FastAPI, Request, Response
import datetime as dt
import time

from src.api import api_router

app = FastAPI()
app.include_router(api_router)


@app.middleware("http")
async def execution_time(request: Request, call_next):
    start_datetime = dt.datetime.now()

    response = await call_next(request)

    duration_datetime = dt.datetime.now() - start_datetime
    response.headers["execution_time"] = str(duration_datetime)
    print(f"\tExecution time in seconds:{duration_datetime.microseconds / 1_000_000}")

    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
