import logging
from datetime import datetime

from fastapi import Depends, APIRouter, BackgroundTasks, HTTPException, status
from sqlalchemy import text, quoted_name
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import engine
from src.core.dependencies import db_dep, admin_id_dep, get_autocommit_conn

from src.schemas.admin import TableData, TableDataExecution, IndexData, IndexDataExecution

router = APIRouter(prefix='/admin', tags=['Admin'])

background_tasks_logger = logging.getLogger('background_tasks')


@router.get('/tables')
async def get_tables(session: db_dep, admin_id: admin_id_dep):
    sql_query = """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name;
"""
    result = await session.execute(text(sql_query))
    rows = result.mappings().all()
    return [{"schema_name": row["table_schema"], "table_name": row["table_name"]} for row in rows]


@router.get("/indexes")
async def get_indexes(session: db_dep, admin_id: admin_id_dep):
    sql_query = """
        SELECT schemaname, tablename, indexname, indexdef
        FROM pg_indexes
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        ORDER BY schemaname, tablename, indexname;
    """
    result = await session.execute(text(sql_query))
    rows = result.mappings().all()
    return [
        {
            "schema_name": row["schemaname"],
            "table_name": row["tablename"],
            "index_name": row["indexname"],
            "definition": row["indexdef"],
        }
        for row in rows
    ]


@router.post('/indexes/exists')
async def indexes_are_exists(session: db_dep, indexes_data: list[IndexData], admin_id: admin_id_dep) -> list[IndexData]:
    sql_indexes_in_db = """
        SELECT schemaname as schema_name, tablename as table_name, indexname as index_name
        FROM pg_indexes
        WHERE indexname = ANY(:index_names);
    """

    indexes_data = {tuple(index_data.model_dump().values()) for index_data in indexes_data}
    indexes_data = [
        IndexData(schema_name=index_data[0], table_name=index_data[1], index_name=index_data[2])
        for index_data in indexes_data
    ]
    index_names = [index_data.index_name for index_data in indexes_data]
    db_indexes = await session.execute(text(sql_indexes_in_db), {"index_names": index_names})
    db_indexes = db_indexes.mappings().fetchall()

    result = []
    for index_data in indexes_data:
        if index_data.model_dump() in db_indexes:
            result.append(index_data)
    return result


@router.post('/tables/vacuum_full')
async def vacuum_full_tables(
        tables_data: list[TableData],
        admin_id: admin_id_dep,
        conn: AsyncSession = Depends(get_autocommit_conn),
):
    sql_tables_in_db = """
        SELECT table_schema as schema_name, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
          AND table_name = ANY(:table_names);
    """

    tables_data = set(tuple(table_data.model_dump().values()) for table_data in tables_data)
    tables_data = [
        TableData(schema_name=table_data[0], table_name=table_data[1])
        for table_data in tables_data
    ]

    table_names = [table_data.table_name for table_data in tables_data]
    db_tables = await conn.execute(text(sql_tables_in_db), {"table_names": table_names})
    db_tables = db_tables.mappings().fetchall()
    db_tables = [dict(db_table) for db_table in db_tables]

    nonexistent_tables = []
    for table_data in tables_data:
        if table_data.model_dump() not in db_tables:
            nonexistent_tables.append(table_data)

    if nonexistent_tables:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tables were not found: {nonexistent_tables}")

    tables_data = [TableDataExecution(**table_data.model_dump()) for table_data in tables_data]
    for table_data in tables_data:
        safe_schema_name = quoted_name(table_data.schema_name, quote=True)
        safe_table_name = quoted_name(table_data.table_name, quote=True)
        sql_query = text(f"VACUUM FULL {safe_schema_name}.{safe_table_name};")
        start_time = datetime.now()
        # background_tasks_logger.debug(f"Start VACUUM FULL for table {table_data.table_name}")
        await conn.execute(sql_query)
        table_data.execution_time_sec = round((datetime.now() - start_time).total_seconds(), 3)
        background_tasks_logger.debug(
            f"End VACUUM FULL for table {table_data} ({table_data.execution_time_sec}s)")

    return {"successful": True, "tables": tables_data}


@router.post('/tables/vacuum_full_background')
async def background_vacuum_full_tables(
        session: db_dep,
        tables_data: list[TableData],
        background_tasks: BackgroundTasks,
        admin_id: admin_id_dep
):
    async def process_vacuum_full_tables(tables_data: list[TableData], ):
        async with engine.connect() as conn:
            await conn.execution_options(isolation_level="AUTOCOMMIT")

            for table_data in tables_data:
                safe_schema_name = quoted_name(table_data.schema_name, quote=True)
                safe_table_name = quoted_name(table_data.table_name, quote=True)
                sql_query = text(f"VACUUM FULL {safe_schema_name}.{safe_table_name};")
                start_time = datetime.now()
                # background_tasks_logger.debug(f"Start VACUUM FULL for table {table_data}")
                await conn.execute(sql_query)
                execution_time = round((datetime.now() - start_time).total_seconds(), 3)
                background_tasks_logger.debug(
                    f"End VACUUM FULL for table {table_data} ({execution_time}s)")

    sql_tables_in_db = """
        SELECT table_schema as schema_name, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
          AND table_name = ANY(:table_names);
    """

    tables_data = set(tuple(table_data.model_dump().values()) for table_data in tables_data)
    tables_data = [
        TableData(schema_name=table_data[0], table_name=table_data[1])
        for table_data in tables_data
    ]

    table_names = [table_data.table_name for table_data in tables_data]
    db_tables = await session.execute(text(sql_tables_in_db), {"table_names": table_names})
    db_tables = db_tables.mappings().fetchall()
    db_tables = [dict(db_table) for db_table in db_tables]

    nonexistent_tables = []
    for table_data in tables_data:
        if table_data.model_dump() not in db_tables:
            nonexistent_tables.append(table_data)

    if nonexistent_tables:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tables were not found: {nonexistent_tables}")

    background_tasks.add_task(process_vacuum_full_tables, tables_data)

    return {"result": "VACUUM FULL started", "tables": tables_data}


@router.post('/indexes/reindex')
async def reindex_indexes(
        indexes_data: list[IndexData],
        admin_id: admin_id_dep,
        conn: AsyncSession = Depends(get_autocommit_conn),
):
    sql_indexes_in_db = """
            SELECT schemaname as schema_name, tablename as table_name, indexname as index_name
            FROM pg_indexes
            WHERE indexname = ANY(:index_names);
        """

    indexes_data = set(tuple(index_data.model_dump().values()) for index_data in indexes_data)
    indexes_data = [
        IndexData(schema_name=index_data[0], table_name=index_data[1], index_name=index_data[2])
        for index_data in indexes_data
    ]

    index_names = [index_data.index_name for index_data in indexes_data]
    db_indexes = await conn.execute(text(sql_indexes_in_db), {"index_names": index_names})
    db_indexes = db_indexes.mappings().fetchall()
    db_indexes = [dict(db_index) for db_index in db_indexes]

    nonexistent_indexes = []
    for index_data in indexes_data:
        if index_data.model_dump() not in db_indexes:
            nonexistent_indexes.append(index_data)

    if nonexistent_indexes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Indexes were not found: {nonexistent_indexes}")

    indexes_data = [IndexDataExecution(**index_data.model_dump()) for index_data in indexes_data]
    for index_data in indexes_data:
        safe_schema_name = quoted_name(index_data.schema_name, quote=True)
        safe_index_name = quoted_name(index_data.index_name, quote=True)
        sql_query = text(f"REINDEX INDEX {safe_schema_name}.{safe_index_name};")
        start_time = datetime.now()
        # background_tasks_logger.debug(f"Start reindex for index {index_data}")
        await conn.execute(sql_query)
        index_data.execution_time_sec = round((datetime.now() - start_time).total_seconds(), 3)
        background_tasks_logger.debug(
            f"End reindex for index {index_data} ({index_data.execution_time_sec}s)")

    return {"successful": True, "indexes": indexes_data}


@router.post('/indexes/reindex_background')
async def background_reindex_indexes(
        session: db_dep,
        indexes_data: list[IndexData],
        background_tasks: BackgroundTasks,
        admin_id: admin_id_dep
):
    async def process_reindex_indexes(indexes_data: list[IndexData]):
        async with engine.connect() as conn:
            await conn.execution_options(isolation_level="AUTOCOMMIT")

            for index_data in indexes_data:
                safe_schema_name = quoted_name(index_data.schema_name, quote=True)
                safe_index_name = quoted_name(index_data.index_name, quote=True)
                sql_query = text(f"REINDEX INDEX {safe_schema_name}.{safe_index_name};")
                start_time = datetime.now()
                # background_tasks_logger.debug(f"Start reindex for index {index_data}")
                await conn.execute(sql_query)
                execution_time_sec = round((datetime.now() - start_time).total_seconds(), 3)
                background_tasks_logger.debug(
                    f"End reindex for index {index_data} ({execution_time_sec}s)")

    sql_indexes_in_db = """
            SELECT schemaname as schema_name, tablename as table_name, indexname as index_name
            FROM pg_indexes
            WHERE indexname = ANY(:index_names);
        """

    indexes_data = set(tuple(index_data.model_dump().values()) for index_data in indexes_data)
    indexes_data = [
        IndexData(schema_name=index_data[0], table_name=index_data[1], index_name=index_data[2])
        for index_data in indexes_data
    ]

    index_names = [index_data.index_name for index_data in indexes_data]
    db_indexes = await session.execute(text(sql_indexes_in_db), {"index_names": index_names})
    db_indexes = db_indexes.mappings().fetchall()
    db_indexes = [dict(db_index) for db_index in db_indexes]

    nonexistent_indexes = []
    for index_data in indexes_data:
        if index_data.model_dump() not in db_indexes:
            nonexistent_indexes.append(index_data)

    if nonexistent_indexes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Indexes were not found: {nonexistent_indexes}")

    background_tasks.add_task(process_reindex_indexes, indexes_data)

    return {"result": "Reindex started", "indexes": indexes_data}
