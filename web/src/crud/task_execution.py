from src.schemas.task_execution import CreateTaskExecutionSchema, TaskExecutionSchema
from src.models import TaskExecution
from src.crud import SchemaCRUD


class TaskExecutionCRUD(SchemaCRUD[TaskExecution, CreateTaskExecutionSchema, TaskExecutionSchema]):
    pass


task_execution_crud: TaskExecutionCRUD = TaskExecutionCRUD(TaskExecution, CreateTaskExecutionSchema, TaskExecutionSchema)
