import asyncio

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

from app.core.database import get_session
from app.main import app
from app.models.base import Base


@pytest.fixture(scope="session")
def pg_container():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg


@pytest.fixture(scope="session")
def db_url(pg_container) -> str:
    return pg_container.get_connection_url().replace(
        "postgresql+psycopg2", "postgresql+asyncpg"
    )


@pytest.fixture(scope="session", autouse=True)
def create_tables(db_url: str):
    async def _create():
        engine = create_async_engine(db_url)
        last_error: Exception | None = None
        for attempt in range(10):
            try:
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                await engine.dispose()
                return
            except Exception as exc:
                last_error = exc
                await asyncio.sleep(1.0 + attempt * 0.5)
        await engine.dispose()
        raise RuntimeError(
            f"Could not connect to DB after 10 attempts: {last_error}"
        ) from last_error

    asyncio.run(_create())


@pytest_asyncio.fixture
async def client(db_url: str):
    engine = create_async_engine(db_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
    await engine.dispose()
