from app.core.config import BaseSchema


class TableData(BaseSchema):
    schema_name: str
    table_name: str

    def __str__(self):
        return f"{self.schema_name}.{self.table_name}"

    def __repr__(self):
        return f"{self.schema_name}.{self.table_name}"


class TableDataExecution(TableData):
    execution_time_sec: float | None = None


class IndexData(BaseSchema):
    schema_name: str
    table_name: str
    index_name: str

    def __str__(self):
        return f"{self.schema_name}.{self.table_name}.{self.index_name}"

    def __repr__(self):
        return f"{self.schema_name}.{self.table_name}.{self.index_name}"


class IndexDataExecution(IndexData):
    execution_time_sec: float | None = None
