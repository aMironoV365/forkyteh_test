import pytest
from sqlalchemy import select
from app.models import WalletRequest


@pytest.mark.asyncio
async def test_get_wallet_info(client, async_session) -> None:
    """
    Интеграционный тест для POST /wallet:
    - Проверяет успешный ответ от сервера.
    - Проверяет корректность возвращённых данных (баланс, энергия и пропускная способность).
    - Проверяет, что адрес кошелька был сохранён в базу данных.
    """
    test_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

    response = await client.post("/wallet", json={"address": test_address})

    assert response.status_code == 200
    data = response.json()
    assert data["address"] == test_address
    assert data["balance"] == 10.0
    assert data["bandwidth"] == 1000
    assert data["energy"] == 500

    result = await async_session.execute(select(WalletRequest))
    wallet = result.scalars().first()
    assert wallet is not None
    assert wallet.address == test_address
