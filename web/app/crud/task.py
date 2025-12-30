from app.schemas.task import CreateTaskSchema, TaskSchema
from app.models import Task
from app.crud import SchemaCRUD


class TaskCRUD(SchemaCRUD[Task, CreateTaskSchema, TaskSchema]):
    pass


task_crud: TaskCRUD = TaskCRUD(Task, CreateTaskSchema, TaskSchema)
