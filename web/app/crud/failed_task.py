from app.schemas.failed_task import CreateFailedTaskSchema, FailedTaskSchema
from app.models import FailedTask
from app.crud import SchemaCRUD


class FailedTaskCRUD(SchemaCRUD[FailedTask, CreateFailedTaskSchema, FailedTaskSchema]):
    pass


failed_task_crud: FailedTaskCRUD = FailedTaskCRUD(FailedTask, CreateFailedTaskSchema, FailedTaskSchema)
