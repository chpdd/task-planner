from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    dflt_day_work_hours: int = 4
    dflt_task_work_hours: int = 2


settings = Settings()
