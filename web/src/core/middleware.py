import time
import datetime as dt
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
from fastapi import Request

logger = logging.getLogger("fastapi")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        request_id = request.headers.get('X-Request-Id')
        raw_request_body = await request.body()
        request_body = raw_request_body.decode()

        logger.debug(
            f' =>: [{request_id}] {request.method} {path} {request_body}  '
        )
        time_start = time.time()
        response = await call_next(request)
        logger.debug(
            f' <=: [{request_id}] {request.method} {path} {response.status_code} '
            f'{request_body} ({round(time.time() - time_start, 3)}s)'
        )
        return response


class ExecutionTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_datetime = dt.datetime.now()

        response = await call_next(request)

        duration_datetime = dt.datetime.now() - start_datetime
        response.headers["execution_time"] = str(duration_datetime)
        print(f"\nExecution time in seconds:{duration_datetime.microseconds / 1_000_000}")

        return response


middleware = [Middleware(LoggingMiddleware)]
