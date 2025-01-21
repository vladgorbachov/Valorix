import logging
import httpx

BINANCE_API_URL = "https://api.binance.com/api/v3/klines"

async def fetch_candlestick_data(symbol: str, interval: str = "1h"):
    """
    Получение данных свечей с Binance API.
    symbol: Пара (например, BTCUSDT).
    interval: Интервал свечей (например, 15m, 1h, 1d).
    """
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 100,  # Количество свечей
    }

    if not symbol or not interval:
        raise ValueError("Symbol and interval must be provided.")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BINANCE_API_URL, params=params)
            response.raise_for_status()
            logging.info(f"Response from Binance: {response.json()}")
            return response.json()
        except Exception as e:
            logging.error(f"Error fetching data from Binance: {e}")
            raise
