from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.market_data import MarketData

router = APIRouter()

@router.get("/market-data")
async def get_market_data(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM market_data")
    data = result.fetchall()
    return [{"id": row.id, "symbol": row.symbol, "price": row.price, "timestamp": row.timestamp} for row in data]
