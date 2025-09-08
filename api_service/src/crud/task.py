from src.schemas.task import CreateTaskSchema, TaskSchema
from src.models import Task
from src.crud import SchemaCRUD


class TaskCRUD(SchemaCRUD[Task, CreateTaskSchema, TaskSchema]):
    pass


task_crud: TaskCRUD = TaskCRUD(Task, CreateTaskSchema, TaskSchema)
