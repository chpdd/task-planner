from app.schemas.task_execution import CreateTaskExecutionSchema, TaskExecutionSchema
from app.models import TaskExecution
from app.crud import SchemaCRUD


class TaskExecutionCRUD(SchemaCRUD[TaskExecution, CreateTaskExecutionSchema, TaskExecutionSchema]):
    pass


task_execution_crud: TaskExecutionCRUD = TaskExecutionCRUD(TaskExecution, CreateTaskExecutionSchema, TaskExecutionSchema)
