from src.config import BaseSchema


class FailedTaskSchema(BaseSchema):
    id: int
    task_id: int


class OwnerFailedTaskSchema(FailedTaskSchema):
    owner_id: int
