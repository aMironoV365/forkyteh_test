from pydantic import BaseModel


class WalletRequestSchema(BaseModel):
    address: str


class WalletResponseSchema(BaseModel):
    address: str
    balance: float
    bandwidth: int
    energy: int
