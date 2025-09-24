import time
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
from fastapi import Request
from multipart.multipart import parse_options_header

logger = logging.getLogger("fastapi")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        request_id = request.headers.get('X-Request-Id')
        if path in {'/api/worker/my_notify'}:
            response = await call_next(request)
            return response

        content_type, _ = parse_options_header(request.headers.get('content-type'))

        if content_type == b'multipart/form-data':
            request_body = ''
        else:
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


middleware = [Middleware(LoggingMiddleware)]
