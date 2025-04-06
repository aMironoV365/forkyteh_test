from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()


class WalletRequest(Base):
    __tablename__ = "wallet_requests"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


async def get_db():
    async with async_session_maker() as session:
        yield session
