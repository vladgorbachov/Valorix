def validate_and_process_binance(raw_data):
    """
    Обработка данных свечей с Binance API.
    """
    return [
        {
            "time": int(candle[0] / 1000),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
        }
        for candle in raw_data if all(float(candle[i]) > 0 for i in range(1, 5))
    ]


def validate_and_process_okx(raw_data):
    """
    Обработка данных свечей с OKX API.
    """
    return [
        {
            "time": int(int(candle[0]) / 1000),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
        }
        for candle in raw_data if all(float(candle[i]) > 0 for i in range(1, 5))
    ]


def process_market_data_cmc(raw_data):
    """
    Обработка данных с CoinMarketCap API.
    """
    return [
        {
            "name": item["name"],
            "symbol": item["symbol"],
            "price": item["quote"]["USD"]["price"],
            "market_cap": item["quote"]["USD"]["market_cap"],
            "volume_24h": item["quote"]["USD"]["volume_24h"],
        }
        for item in raw_data
    ]
