import httpx

OKX_API_URL = "https://www.okx.com/api/v5/market/candles"

async def fetch_candlestick_data_okx(symbol: str, interval: str = "1h"):
    """
    Получение данных свечей с OKX API.
    symbol: Пара (например, BTC-USDT).
    interval: Интервал свечей (например, 15m, 1H, 1D).
    """
    params = {
        "instId": symbol,
        "bar": interval,
        "limit": 100,  # Количество свечей
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(OKX_API_URL, params=params)
        response.raise_for_status()
        return response.json()["data"]
