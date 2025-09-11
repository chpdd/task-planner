from app.schemas.day import CreateDaySchema, DaySchema
from app.models import Day
from app.crud import SchemaCRUD


class DayCRUD(SchemaCRUD[Day, CreateDaySchema, DaySchema]):
    pass


day_crud: DayCRUD = DayCRUD(Day, CreateDaySchema, DaySchema)
