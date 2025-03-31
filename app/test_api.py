from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_post_wallet(client):
    # Тестовый адрес Tron (можете заменить на валидный для вашего случая)
    test_address = "TMwFHYXLJaRUPeW6421aqXL4ZEzPRFGkGT"

    response = client.post("/wallet", json={"address": test_address})

    # Проверяем успешный статус код
    assert response.status_code == 200

    # Проверяем структуру ответа
    response_data = response.json()
    assert "address" in response_data
    assert "balance" in response_data
    assert "bandwidth" in response_data
    assert "energy" in response_data

    # Проверяем, что адрес в ответе совпадает с отправленным
    assert response_data["address"] == test_address


# Тест для GET /wallets
def test_get_wallets(client):
    # Сначала создаем тестовый кошелек
    test_address = "TMwFHYXLJaRUPeW6421aqXL4ZEzPRFGkGT"
    client.post("/wallet", json={"address": test_address})

    # Теперь получаем список
    response = client.get("/wallets")

    # Проверяем успешный статус код
    assert response.status_code == 200

    # Проверяем, что ответ - список
    wallets = response.json()
    assert isinstance(wallets, list)

    # Проверяем, что наш тестовый кошелек есть в списке
    assert any(wallet["address"] == test_address for wallet in wallets)


# Дополнительный тест для пагинации
def test_wallets_pagination(client):
    # Добавляем несколько тестовых адресов
    test_addresses = [
        "TMwFHYXLJaRUPeW6421aqXL4ZEzPRFGkGT",
        "TNPZqQNXE8JN2dQNkj8jY7Y1Y7Y1Y7Y1Y7Y",
        "TNPZqQNXE8JN2dQNkj8jY7Y1Y7Y1Y7Y1Y8",
    ]

    for addr in test_addresses:
        client.post("/wallet", json={"address": addr})

    # Проверяем пагинацию
    response = client.get("/wallets?skip=1&limit=2")
    assert response.status_code == 200
    wallets = response.json()
    assert len(wallets) == 2  # Должно вернуть 2 кошелька согласно limit
