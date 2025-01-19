import httpx
from app.core.config import settings

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"
COINMARKETCAP_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

async def fetch_binance_data(symbol: str):
    headers = {"X-MBX-APIKEY": settings.binance_api_key}
    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_API_URL, params={"symbol": symbol}, headers=headers)
        return response.json()

async def fetch_coinmarketcap_data():
    headers = {"X-CMC_PRO_API_KEY": settings.coinmarketcap_api_key}
    async with httpx.AsyncClient() as client:
        response = await client.get(COINMARKETCAP_API_URL, headers=headers)
        return response.json()
