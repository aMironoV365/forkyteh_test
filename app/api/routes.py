from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import WalletRequest
from ..schemas import WalletRequestSchema, WalletResponseSchema
from ..database import get_db

router = APIRouter()


@router.post("/wallet", response_model=WalletResponseSchema, summary="Получить информацию о кошельке")
async def get_wallet_info(
    request: WalletRequestSchema,
    db: AsyncSession = Depends(get_db),
    fastapi_request: Request = None,
) -> WalletResponseSchema:
    """
    Получить информацию о кошельке Tron и сохранить запрос в базу данных.
    """
    address = request.address
    try:
        tron = fastapi_request.app.tron
        account = tron.get_account(address)
        balance = account.get("balance", 0) / 1_000_000
        bandwidth = account.get("bandwidth", 0)
        energy = account.get("energy", 0)

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


@router.get("/wallets", summary="Получить список всех кошельков")
async def get_wallet_requests(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10
):
    """
    Получить список всех записей кошельков из базы данных.
    """
    result = await db.execute(select(WalletRequest).offset(skip).limit(limit))
    wallets = result.scalars().all()
    return wallets
