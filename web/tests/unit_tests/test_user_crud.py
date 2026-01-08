import pytest
from app.crud.user import user_crud
from app.schemas.user import CreateUserSchema
from app.models import User
from app.core import security

@pytest.mark.asyncio
async def test_create_user_base(db_session):
    # Test base create method (bypassing schema_create which lacks password)
    password = "password123"
    hashed_password = security.hash_password(password)
    user = User(
        name="crud_test_user",
        hashed_password=hashed_password
    )
    
    await user_crud.create(db_session, user)
    await db_session.commit()
    
    # Verify persistence
    stored_user = await user_crud.get(db_session, user.id)
    assert stored_user is not None
    assert stored_user.name == "crud_test_user"
    assert stored_user.hashed_password == hashed_password

@pytest.mark.asyncio
async def test_get_user(db_session):
    # Setup
    password = security.hash_password("password123")
    user = User(name="get_user_test", hashed_password=password)
    await user_crud.create(db_session, user)
    await db_session.commit()
    
    # Test schema_get
    fetched_user = await user_crud.schema_get(db_session, user.id)
    assert fetched_user.id == user.id
    assert fetched_user.name == "get_user_test"

    # Test schema_get_by_name
    fetched_by_name = await user_crud.schema_get_by_name(db_session, "get_user_test")
    assert fetched_by_name.id == user.id

@pytest.mark.asyncio
async def test_update_user(db_session):
    # Setup
    user = User(name="update_test_user", hashed_password=security.hash_password("pass"))
    await user_crud.create(db_session, user)
    await db_session.commit()
    
    # Update via schema_update_by_id
    update_data = CreateUserSchema(name="updated_name")
    updated_user = await user_crud.schema_update_by_id(db_session, user.id, update_data)
    
    assert updated_user.name == "updated_name"
    
    # Verify in DB
    refreshed_user = await user_crud.get(db_session, user.id)
    assert refreshed_user.name == "updated_name"

@pytest.mark.asyncio
async def test_delete_user(db_session):
    # Setup
    user = User(name="delete_test_user", hashed_password=security.hash_password("pass"))
    await user_crud.create(db_session, user)
    await db_session.commit()
    
    # Delete
    await user_crud.delete(db_session, user) # Base delete takes ORM obj
    await db_session.commit()
    
    # Verify
    stored_user = await user_crud.get(db_session, user.id)
    assert stored_user is None
