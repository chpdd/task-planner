import logging
import time

from fastapi import Request
from multipart.multipart import parse_options_header
from starlette.middleware.base import BaseHTTPMiddleware
from uvicorn.config import LOGGING_CONFIG

date_format = '%Y-%m-%d %H:%M:%S'
tz = time.strftime('%z')
log_format = '%(asctime)s.%(msecs)03d ' + tz + ' %(levelname)s - %(name)s (%(filename)s:%(lineno)d): %(message)s'

logging.basicConfig(level=logging.DEBUG, datefmt=date_format, format=log_format)
logging.getLogger('uvicorn').setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel('INFO')

log_config = LOGGING_CONFIG.copy()
log_config["formatters"]["default"]["fmt"] = log_format
log_config["formatters"]["default"]["datefmt"] = date_format
log_config["formatters"]["access"]["fmt"] = log_format
log_config["formatters"]["access"]["datefmt"] = date_format

logger = logging.getLogger('fastapi')


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
