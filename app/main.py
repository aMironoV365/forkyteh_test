from fastapi import FastAPI
from .database import engine
from .models import Base
from contextlib import asynccontextmanager
from tronpy import Tron
from .api.routes import router as wallet_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекст жизненного цикла приложения:
    - создание таблиц при запуске
    - закрытие соединения при остановке
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.tron = Tron()


app.include_router(wallet_router, tags=["Wallet"])
