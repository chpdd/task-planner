import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from pathlib import Path
from alembic.config import Config
from alembic import command

from src.core.dependencies import get_db
from src.main import app
from src.core.config import settings

engine = create_async_engine(
    settings.db_url,
    poolclass=NullPool,
)
test_session_factory = async_sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    assert settings.MODE == "test", f"A non-test environment has been set up ({settings.DB_MODE=})"
    assert "test" in settings.DB_NAME, f'The test database name "{settings.DB_NAME}" does not have the word "test" in it'

    base_dir = Path("/app")
    alembic_ini_path = base_dir / "alembic.ini"
    alembic_cfg = Config(str(alembic_ini_path))
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


@pytest.fixture(scope="function")
async def db_session():
    async with engine.connect() as connection:
        # Beginning the transaction
        transaction = await connection.begin()
        # Create session in connection
        # With join_transaction_mode="create_savepoint", rollback will rollback the nested transaction(savepoint),
        # not the entire session
        async with test_session_factory(bind=connection, join_transaction_mode="create_savepoint") as session:
            yield session

        # Rollback all changes made during the transaction
        await transaction.rollback()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession):
    async def test_get_db():
        yield db_session

    app.dependency_overrides[get_db] = test_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client
    app.dependency_overrides.clear()
