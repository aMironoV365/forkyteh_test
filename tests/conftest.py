import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from tronpy import Tron

from app.main import app
from app.models import Base, get_db


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture()
async def async_engine():
    """
    Фикстура для создания асинхронного SQLAlchemy движка.
    Возвращает engine и закрывает его после тестов.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture()
async def async_session(async_engine: async_engine) -> async_engine:
    """
    Фикстура для создания новой тестовой базы данных и сессии.
    Удаляет и пересоздаёт все таблицы перед запуском.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )

    session = async_session()
    try:
        yield session
    finally:
        await session.close()


@pytest_asyncio.fixture()
async def client(async_session: async_engine) -> async_session:
    """
    Фикстура для создания клиента для тестирования API.
    Устанавливает заглушки для Tron и переопределяет get_db.
    """
    mock_tron = Tron()
    mock_account = {"balance": 10_000_000, "bandwidth": 1000, "energy": 500}
    mock_tron.get_account = lambda address: mock_account

    original_tron = getattr(app, "tron", None)
    app.tron = mock_tron

    async def override_get_db():
        yield async_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client

    if original_tron is not None:
        app.tron = original_tron
    else:
        delattr(app, "tron")

    app.dependency_overrides.clear()
