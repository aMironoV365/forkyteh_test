from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class WalletRequest(Base):
    """
    Модель запроса на получение информации о кошельке Tron.
    """

    __tablename__ = "wallet_requests"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
