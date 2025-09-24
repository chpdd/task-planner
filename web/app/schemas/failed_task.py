from app.core.config import BaseSchema


class CreateFailedTaskSchema(BaseSchema):
    task_id: int


class FailedTaskSchema(CreateFailedTaskSchema):
    id: int


class OwnerFailedTaskSchema(FailedTaskSchema):
    owner_id: int
