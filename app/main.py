from fastapi import FastAPI, HTTPException, Depends
from models import WalletRequest, get_db, Base, engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tronpy import Tron
from schemas import WalletRequestSchema, WalletResponseSchema
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Закрываем соединения при остановке
    await engine.dispose()


tron = Tron()
app = FastAPI(lifespan=lifespan)


@app.post("/wallet", response_model=WalletResponseSchema)
async def get_wallet_info(
    request: WalletRequestSchema, db: AsyncSession = Depends(get_db)
):
    address = request.address
    try:
        account = tron.get_account(address)
        balance = account.get("balance", 0) / 1_000_000
        bandwidth = account.get("bandwidth", 0)
        energy = account.get("energy", 0)

        # Save request to DB
        db_request = WalletRequest(address=address)
        db.add(db_request)
        await db.commit()
        await db.refresh(db_request)

        return {
            "address": address,
            "balance": balance,
            "bandwidth": bandwidth,
            "energy": energy,
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/wallets")
async def get_wallet_requests(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10
):
    result = await db.execute(select(WalletRequest).offset(skip).limit(limit))
    wallets = result.scalars().all()
    return wallets
