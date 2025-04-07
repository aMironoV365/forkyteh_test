from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./Forkytech.db")

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()


class WalletRequest(Base):
    """
    Модель запроса на получение информации о кошельке Tron.
    """

    __tablename__ = "wallet_requests"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))


async def get_db():
    """
    Зависимость FastAPI: возвращает асинхронную сессию базы данных.
    """
    async with async_session_maker() as session:
        yield session
