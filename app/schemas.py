from pydantic import BaseModel


class WalletRequestSchema(BaseModel):
    """
    Схема для POST-запроса к /wallet.
    """

    address: str


class WalletResponseSchema(BaseModel):
    """
    Схема для ответа от /wallet.
    """

    address: str
    balance: float
    bandwidth: int
    energy: int
