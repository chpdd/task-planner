
from app.schemas.user import CreateUserSchema, UserSchema
from app.models import User
from app.crud import SchemaCRUD


class UserCRUD(SchemaCRUD[User, CreateUserSchema, UserSchema]):
    pass


user_crud: UserCRUD = UserCRUD(User, CreateUserSchema, UserSchema)
