import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from tronpy import Tron

from app.main import app, tron
from app.models import Base, get_db # Импортируйте ваши модели SQLAlchemy

# Настройки тестовой БД (можно использовать SQLite для тестов)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture()
async def async_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture()
async def async_session(async_engine):
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
async def client(async_session):
    # Здесь можно добавить зависимости, которые нужно переопределить в тестах
    async def override_get_db():
        yield async_session
    
    app.dependency_overrides[get_db] = override_get_db  # если у вас есть зависимость get_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
# @pytest_asyncio.fixture()
# async def client(async_session):
#     # Мокаем Tron client
#     mock_tron = Tron()
#     mock_account = {
#         "balance": 10_000_000,
#         "bandwidth": 1000,
#         "energy": 500
#     }
#     mock_tron.get_account = lambda address: mock_account
    
#     # Сохраняем и подменяем tron client в приложении
#     original_tron = getattr(app, 'tron', None)
#     app.tron = mock_tron
    
#     # Переопределяем зависимость БД
#     async def override_get_db():
#         yield async_session
    
#     app.dependency_overrides[get_db] = override_get_db
    
#     # Создаем тестовый клиент (новый синтаксис)
#     async with AsyncClient(app=app, base_url="http://test") as test_client:
#         yield test_client
    
#     # Восстанавливаем оригинальный tron client
#     if original_tron is not None:
#         app.tron = original_tron
#     else:
#         delattr(app, 'tron')
    
#     # Очищаем переопределения
#     app.dependency_overrides.clear()