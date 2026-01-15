from src.schemas.manual_day import CreateManualDaySchema, ManualDaySchema
from src.models import ManualDay
from src.crud import SchemaCRUD


class ManualDayCRUD(SchemaCRUD[ManualDay, CreateManualDaySchema, ManualDaySchema]):
    pass


manual_day_crud: ManualDayCRUD = ManualDayCRUD(ManualDay, CreateManualDaySchema, ManualDaySchema)

