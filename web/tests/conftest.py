import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text
from pathlib import Path
from alembic.config import Config
from alembic import command

from app.core.dependencies import get_db
from app.main import app
from app.core.config import settings

# Construct Postgres URL from settings
# pytest-dotenv ensures settings are loaded from .test.env
SQLALCHEMY_DATABASE_URL = settings.db_url

async def ensure_test_db():
    # Connect to default 'postgres' db to create the test db
    # We explicitly construct the URL for the 'postgres' database
    default_db_url = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/postgres"
    engine = create_async_engine(default_db_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        # Check if db exists
        result = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_NAME}'"))
        if not result.scalar():
            await conn.execute(text(f"CREATE DATABASE {settings.DB_NAME}"))
    await engine.dispose()

# Run the check (blocking, but okay for test session startup)
try:
    asyncio.run(ensure_test_db())
except Exception as e:
    print(f"Warning: Could not check/create database: {e}")

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=NullPool,
)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    # Ensure we are using the test database by checking the name in settings
    # This prevents accidental migration of production DB if env vars are wrong
    assert "test" in settings.DB_NAME, f"Dangerous operation! Attempting to run tests against {settings.DB_NAME}"
    
    assert "test" in settings.DB_NAME, f"Dangerous operation! Attempting to run tests against {settings.DB_NAME}"
    
    base_dir = Path(__file__).resolve().parent.parent
    alembic_ini_path = base_dir / "alembic.ini"
    alembic_script_path = base_dir / "alembic"

    alembic_cfg = Config(str(alembic_ini_path))
    # Override sqlalchemy.url in alembic config to use the constructed URL
    alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    alembic_cfg.set_main_option("script_location", str(alembic_script_path))
    
    # Run migrations
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    # Simple truncation for common tables:
    async with engine.begin() as conn:
        # Truncate all tables except alembic_version
        await conn.execute(text("TRUNCATE TABLE users, tasks, day_plans, plans CASCADE;"))

    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_db] = override_get_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
