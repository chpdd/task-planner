import pytest
from fastapi import HTTPException

from src.crud.user import user_crud
from src.schemas.user import CreateUserSchema
from src.models import User
from src.core import security


@pytest.mark.asyncio
async def test_create_user_base(db_session):
    password = "password123"
    hashed_password = security.hash_password(password)
    user = User(
        name="crud_test_user",
        hashed_password=hashed_password
    )

    await user_crud.create(db_session, user)
    await db_session.commit()

    stored_user = await user_crud.get(db_session, user.id)
    assert stored_user is not None
    assert stored_user.name == "crud_test_user"
    assert stored_user.hashed_password == hashed_password


@pytest.mark.asyncio
async def test_get_user(db_session):
    password = security.hash_password("password123")
    user = User(name="get_user_test", hashed_password=password)
    await user_crud.create(db_session, user)
    await db_session.commit()

    fetched_user = await user_crud.schema_get(db_session, user.id)
    assert fetched_user.id == user.id
    assert fetched_user.name == "get_user_test"

    fetched_by_name = await user_crud.schema_get_by_name(db_session, "get_user_test")
    assert fetched_by_name.id == user.id


@pytest.mark.asyncio
async def test_update_user(db_session):
    user = User(name="update_test_user", hashed_password=security.hash_password("pass"))
    await user_crud.create(db_session, user)
    await db_session.commit()

    update_data = CreateUserSchema(name="updated_name")
    updated_user = await user_crud.schema_update_by_id(db_session, user.id, update_data)

    assert updated_user.name == "updated_name"

    refreshed_user = await user_crud.get(db_session, user.id)
    assert refreshed_user.name == "updated_name"


@pytest.mark.asyncio
async def test_delete_user(db_session):
    user = User(name="delete_test_user", hashed_password=security.hash_password("pass"))
    await user_crud.create(db_session, user)
    await db_session.commit()

    await user_crud.delete(db_session, user)
    await db_session.commit()

    with pytest.raises(HTTPException) as exc:
        await user_crud.get(db_session, user.id)
    assert exc.value.status_code == 404
