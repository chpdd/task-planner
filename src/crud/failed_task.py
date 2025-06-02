from src.schemas.failed_task import CreateFailedTaskSchema, FailedTaskSchema
from src.models import FailedTask
from src.crud import SchemaCRUD


class FailedTaskCRUD(SchemaCRUD[FailedTask, CreateFailedTaskSchema, FailedTaskSchema]):
    pass


failed_task_crud = FailedTaskCRUD(FailedTask, CreateFailedTaskSchema, FailedTaskSchema)
