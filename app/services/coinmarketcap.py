import httpx

COINMARKETCAP_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
COINMARKETCAP_API_KEY = "ваш_ключ"

async def fetch_market_data_cmc():
    """
    Получение данных с CoinMarketCap API.
    """
    headers = {"X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.get(COINMARKETCAP_API_URL, headers=headers)
        response.raise_for_status()
        return response.json()["data"]
