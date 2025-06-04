from src.schemas.day import CreateDaySchema, DaySchema
from src.models import Day
from src.crud import SchemaCRUD


class DayCRUD(SchemaCRUD[Day, CreateDaySchema, DaySchema]):
    pass


day_crud: DayCRUD = DayCRUD(Day, CreateDaySchema, DaySchema)
