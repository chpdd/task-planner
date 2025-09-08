import uvicorn
from fastapi import FastAPI, Request, Response
from starlette.middleware import Middleware

from src.api import api_router
from src.logging_middleware import LoggingMiddleware, log_config

middleware = [Middleware(LoggingMiddleware)]

app = FastAPI(middleware=middleware)
app.include_router(api_router)

# import datetime as dt
# import time
# @app.middleware("http")
# async def execution_time(request: Request, call_next):
#     start_datetime = dt.datetime.now()
#
#     response = await call_next(request)
#
#     duration_datetime = dt.datetime.now() - start_datetime
#     response.headers["execution_time"] = str(duration_datetime)
#     print(f"\nExecution time in seconds:{duration_datetime.microseconds / 1_000_000}")
#
#     return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, access_log=False, log_config=log_config)
