import logging
import logging.config

from enum import Enum
from fastapi import APIRouter
from sqlalchemy import text, select

from app.core.log import log_config
from app.core.dependencies import db_dep, admin_id_dep
from app.models.user import User

router = APIRouter(prefix='/logging', tags=['Logging'])

logger = logging.getLogger("fastapi")


@router.get("/drop_logs")
async def drop_logs(admin_id: admin_id_dep):
    for level_name, value in logging.getLevelNamesMapping().items():
        logger.log(msg=f"Drop log with level={level_name}", level=value)
    return {"result": "successful"}


@router.get("/check_multiline")
async def check_multiline(admin_id: admin_id_dep):
    logger.info(
        "dsaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\ndsadsadsadjnsajdnsakjdsajkdnsa\n\ndsaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n")
    return {"status": "successful"}


@router.get("/check_multiline_sqlalchemy")
async def check_multiline_sqlalchemy(session: db_dep, admin_id: admin_id_dep):
    sql_query = """
    SELECT 
        *
    FROM users;
    """
    result = await session.execute(text(sql_query))

    sql_orm = select(User)
    result_orm = await session.scalars(sql_orm)
    logger.debug(f"{result_orm=}")
    logger.debug("test log")

    users = result.mappings().fetchall()
    return users


@router.get("/check_errors")
async def check_logger_erros(session: db_dep, admin_id: admin_id_dep):
    results = await session.execute("no text query")
    return results.mappings().fetchall()


class LogLevel(Enum):
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


@router.post("/set_default_log_config")
async def set_default_log_config(admin_id: admin_id_dep):
    logging.config.dictConfig(log_config)
    return {"status": "successful"}


@router.get("/loggers")
async def check_loggers(admin_id: admin_id_dep):
    result = []
    for name, logger_ in [("root", logging.getLogger())] + list(logging.Logger.manager.loggerDict.items()):
        result.append(
            f"Logger: {name}, Level: {getattr(logger_, "level", None)}, Handlers: {getattr(logger_, 'handlers', [])}, Propagate: {getattr(logger_, 'propagate', None)}")
    return result


@router.post("/loggers/level")
async def set_loggers_level(log_level: LogLevel, admin_id: admin_id_dep):
    log_level_value = logging.getLevelNamesMapping()[log_level.value]
    for name, logger in logging.Logger.manager.loggerDict.items():
        if hasattr(logger, "level"):
            logger.setLevel(log_level_value)
    return {"result": f"All loggers set to level '{log_level.name}'"}


@router.post("/loggers/propagate")
async def set_loggers_propagate(propagate: bool, admin_id: admin_id_dep):
    for name, logger in logging.Logger.manager.loggerDict.items():
        if hasattr(logger, "propagate"):
            logger.propagate = propagate
    return {"result": f"Propagate in all loggers set to '{propagate}'"}


@router.get("/root_level")
async def get_root_level(admin_id: admin_id_dep):
    return {"result": logging.getLevelName(logging.root.level)}


@router.post("/root_level")
async def set_root_level(log_level: LogLevel, admin_id: admin_id_dep):
    log_level_value = logging.getLevelNamesMapping()[log_level.value]
    logging.root.setLevel(log_level_value)
    return {"result": f"Root logger level set to {log_level.name}"}
