
from src.schemas.user import CreateUserSchema, UserSchema
from src.models import User
from src.crud import SchemaCRUD


class UserCRUD(SchemaCRUD[User, CreateUserSchema, UserSchema]):
    pass


user_crud: UserCRUD = UserCRUD(User, CreateUserSchema, UserSchema)
