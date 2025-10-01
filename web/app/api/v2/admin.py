import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from sqlalchemy import text
from sqlalchemy.sql.elements import quoted_name

from app.core.config import BaseSchema
from app.api.dependencies import admin_id_dep, db_dep
from app.core.database import engine

router = APIRouter(prefix='/admin', tags=['Admin'])

background_tasks_logger = logging.getLogger('background_tasks')


@router.get('/tables')
async def get_tables(admin_id: admin_id_dep, db: db_dep):
    sql_query = f"""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name;
"""
    result = await db.execute(text(sql_query))
    rows = result.mappings().all()
    return [{"schema": row["table_schema"], "table": row["table_name"]} for row in rows]


@router.get("/indexes")
async def get_indexes(admin_id: admin_id_dep, db: db_dep):
    sql_query = """
        SELECT schemaname, tablename, indexname, indexdef
        FROM pg_indexes
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        ORDER BY schemaname, tablename, indexname;
    """
    result = await db.execute(text(sql_query))
    rows = result.mappings().all()
    return [
        {
            "schema": row["schemaname"],
            "table": row["tablename"],
            "index": row["indexname"],
            "definition": row["indexdef"],
        }
        for row in rows
    ]


class TableData(BaseSchema):
    schema_name: str
    table_name: str

    def __repr__(self):
        return f"{self.schema_name}.{self.table_name}"


class IndexData(BaseSchema):
    schema_name: str
    table_name: str
    index_name: str

    def __repr__(self):
        return f"{self.schema_name}.{self.table_name}.{self.index_name}"


@router.post('/indexes/exists')
async def indexes_are_exists(indexes_data: list[IndexData], admin_id: admin_id_dep, db: db_dep) -> list[IndexData]:
    sql_indexes_in_db = f"""
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
    db_indexes = await db.execute(text(sql_indexes_in_db), {"index_names": index_names})
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
        db: db_dep,
        background_tasks: BackgroundTasks
):
    async def process_vacuum_full_tables(tables_data: list[TableData]):
        async with engine.connect() as conn:
            await conn.execution_options(isolation_level="AUTOCOMMIT")
            for table_name in tables_data.table_names:
                safe_table_name = quoted_name(table_name, quote=True)
                sql_query = text(f"VACUUM FULL {safe_table_name};")
                background_tasks_logger.debug(f"Start VACUUM FULL for table {table_name}")
                await conn.execute(sql_query)
                background_tasks_logger.debug(f"End VACUUM FULL for table {table_name}")

    sql_tables_in_db = """
        SELECT table_schema, table_name
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
    db_tables = await db.execute(text(sql_tables_in_db), {"table_names": table_names})
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

    return {"result": f"VACUUM FULL started", "tables": tables_data}


@router.post('/indexes/reindex')
async def reindex_indexes(
        indexes_data: list[IndexData],
        admin_id: admin_id_dep,
        db: db_dep,
        backround_tasks: BackgroundTasks
):
    async def process_reindex_indexes(indexes_data: list[IndexData]):
        async with engine.connect() as conn:
            await conn.execution_options(isolation_level="AUTOCOMMIT")
            for index_data in indexes_data:
                safe_schema_name = quoted_name(index_data.schema_name, quote=True)
                safe_index_name = quoted_name(index_data.index_name, quote=True)
                sql_query = text(f"REINDEX INDEX {safe_schema_name}.{safe_index_name};")
                background_tasks_logger.debug(f"Start reindex for index {safe_schema_name}.{safe_index_name}")
                await conn.execute(sql_query)
                background_tasks_logger.debug(f"End reindex for index {safe_schema_name}.{safe_index_name}")

    sql_indexes_in_db = f"""
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
    db_indexes = await db.execute(text(sql_indexes_in_db), {"index_names": index_names})
    db_indexes = db_indexes.mappings().fetchall()
    db_indexes = [dict(db_index) for db_index in db_indexes]

    nonexistent_indexes = []
    for index_data in indexes_data:
        if index_data.model_dump() not in db_indexes:
            nonexistent_indexes.append(index_data)

    if nonexistent_indexes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Indexes were not found: {nonexistent_indexes}")

    backround_tasks.add_task(process_reindex_indexes, indexes_data)

    return {"result": f"Reindex started", "indexes": indexes_data}
