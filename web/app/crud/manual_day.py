from app.schemas.manual_day import CreateManualDaySchema, ManualDaySchema
from app.models import ManualDay
from app.crud import SchemaCRUD


class ManualDayCRUD(SchemaCRUD[ManualDay, CreateManualDaySchema, ManualDaySchema]):
    pass


manual_day_crud: ManualDayCRUD = ManualDayCRUD(ManualDay, CreateManualDaySchema, ManualDaySchema)

