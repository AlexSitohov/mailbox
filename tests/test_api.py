import asyncio
import os

import asyncpg
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import status

from database import get_session
from main import app

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost/mailbox_test"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "zxc"')
    os.system("alembic upgrade heads")


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    async with async_session_test() as session:
        async with session.begin():
            await session.execute(f"""DELETE FROM users;""")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


async def get_test_session():
    try:
        test_engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL, future=True, echo=True
        )

        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )

        yield test_async_session()

    finally:
        pass


@pytest.fixture(scope="function")
async def client():
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(SQLALCHEMY_DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    pool.close()


async def test_registration(client):
    response = client.post('/users',
                           json=
                           {
                               "email": "merc@example.com",
                               "password": "123",
                               "name": "merc",
                               "surname": "mercsan"
                           })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('email') == "merc@example.com"
    assert response.json().get("name") == "merc"
    assert response.json().get("surname") == "mercsan"


async def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == status.HTTP_200_OK
    print('!!!!!!!!!!!!!!!!!!!!!!', response.json())
    # assert response.json()[0].get('email') == "merc@example.com"


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    async with async_session_test() as session:
        async with session.begin():
            await session.execute(f"""DELETE FROM users;""")
