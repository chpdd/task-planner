import pytest
import datetime as dt
from app.crud import task_crud, user_crud
from app.schemas.task import CreateTaskSchema
from app.models import User
from app.core import security

@pytest.fixture
async def test_user(db_session):
    # Use UserCRUD base create method
    user = User(
        name="taskowner", 
        hashed_password=security.hash_password("password123")
    )
    await user_crud.create(db_session, user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.mark.asyncio
async def test_create_task(db_session, test_user):
    task_in = CreateTaskSchema(
        name="Test Task",
        deadline=dt.date(2025, 12, 31),
        interest=5,
        importance=8,
        work_hours=2
    )
    task = await task_crud.schema_owner_create(db_session, task_in, owner_id=test_user.id)
    assert task.name == "Test Task"
    assert task.owner_id == test_user.id
    assert task.deadline == dt.date(2025, 12, 31)

@pytest.mark.asyncio
async def test_get_task(db_session, test_user):
    task_in = CreateTaskSchema(name="Get Task")
    task = await task_crud.schema_owner_create(db_session, task_in, owner_id=test_user.id)
    
    stored_task = await task_crud.schema_owner_get(db_session, task.id, owner_id=test_user.id)
    assert stored_task
    assert stored_task.id == task.id
    assert stored_task.name == "Get Task"

@pytest.mark.asyncio
async def test_list_owner_tasks(db_session, test_user):
    await task_crud.schema_owner_create(db_session, CreateTaskSchema(name="Task 1"), owner_id=test_user.id)
    await task_crud.schema_owner_create(db_session, CreateTaskSchema(name="Task 2"), owner_id=test_user.id)
    
    tasks = await task_crud.schema_owner_list(db_session, owner_id=test_user.id)
    assert len(tasks) >= 2
    names = [t.name for t in tasks]
    assert "Task 1" in names

@pytest.mark.asyncio
async def test_update_task(db_session, test_user):
    task = await task_crud.schema_owner_create(
        db_session, 
        CreateTaskSchema(name="Old Name"), 
        owner_id=test_user.id
    )
    
    update_data = CreateTaskSchema(name="New Name")
    # schema_update takes ORM obj and schema. We need to fetch ORM obj first or use update_by_id logic?
    # SchemaCRUD.schema_update takes (session, obj, schema).
    # SchemaCRUD.schema_update_by_id is what we likely want if we just have ID.
    
    updated_task = await task_crud.schema_update_by_id(db_session, task.id, update_data)
    assert updated_task.name == "New Name"
