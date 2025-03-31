import pytest
from fastapi.testclient import TestClient
from .main import app


@pytest.fixture
def api_client():
    """Фикстура для API-клиента."""
    return TestClient(app)

# @pytest.fixture(autouse=True)
# def setup_test_db():
#     # Создаем тестовую БД
#     Base.metadata.create_all(bind=test_engine)
#     yield
#     # Очищаем после тестов
#     Base.metadata.drop_all(bind=test_engine)