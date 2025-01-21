from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.services.binance import fetch_candlestick_data
import requests
import logging


app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение статики и шаблонов
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Рендер главной страницы.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/v1/candlestick")
async def get_candlestick_data(
        symbol: str = "BTCUSDT",
        interval: str = "1h"
):
    """
    Эндпоинт для получения данных свечей с Binance API.
    """
    try:
        if not symbol or not interval:
            raise ValueError("Missing required query parameters: 'symbol' or 'interval'.")

        raw_data = await fetch_candlestick_data(symbol, interval)
        if not raw_data:
            raise ValueError("No data received from Binance API.")

        processed_data = [
            {
                "time": int(item[0]),
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
            }
            for item in raw_data
        ]
        return {"data": processed_data}
    except Exception as e:
        logging.error(f"Error in /api/v1/candlestick: {e}")
        return {"error": str(e)}


@app.get("/api/v1/forex")
async def get_forex_data():
    try:
        response = requests.get(
            "https://api.exchangeratesapi.io/latest",
            params={"access_key": "ae8d07b623865365dbb3ffe104c884f4"}
        )
        data = response.json()
        rates = data.get("rates", {})
        base_currency = data.get("base", "EUR")
        forex = [
            {
                "name": f"{base_currency}/{currency}",
                "value": round(rate, 2),
                "change_percent": round((rate - 1) * 100, 2) if rate > 1 else -round((1 - rate) * 100, 2),
            }
            for currency, rate in list(rates.items())[:10]
        ]
        return forex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching forex data: {str(e)}")



@app.get("/api/v1/crypto")
async def get_crypto_data():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/24hr")
        data = response.json()
        top_10 = [
            {
                "symbol": item["symbol"],
                "price": float(item["lastPrice"]),
                "change_percent": float(item["priceChangePercent"]),
            }
            for item in data[:10]
        ]
        return top_10
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching crypto data: {str(e)}")



@app.get("/api/v1/market")
async def get_market_data():
    try:
        indices = ["DJI", "SPX", "NDX", "FTSE", "DAX", "CAC", "NIKKEI", "HSI", "ASX", "SSE"]
        results = []

        for index in indices:
            response = requests.get(
                "https://www.alphavantage.co/query",
                params={
                    "function": "TIME_SERIES_INTRADAY",
                    "symbol": index,
                    "interval": "60min",
                    "apikey": "GDY2XBHWPWTIMTV8",
                }
            )
            data = response.json()
            time_series = data.get("Time Series (60min)", {})
            latest_time = max(time_series.keys(), default=None) if time_series else None
            if latest_time:
                latest_data = time_series[latest_time]
                results.append({
                    "name": index,
                    "value": float(latest_data["1. open"]),
                    "change_percent": round(float(latest_data["1. open"]) * 0.01, 2),
                })

        # Если результаты пустые, возвращаем фолбэк
        if not results:
            results = [
                {"name": "S&P 500", "value": 4500, "change_percent": 1.2},
                {"name": "Dow Jones", "value": 35000, "change_percent": 0.8},
                {"name": "Nasdaq", "value": 15000, "change_percent": 2.0},
            ]

        return {"data": results}
    except Exception as e:
        # Если произошла ошибка, возвращаем фолбэк
        return {"data": [
            {"name": "S&P 500", "value": 4500, "change_percent": 1.2},
            {"name": "Dow Jones", "value": 35000, "change_percent": 0.8},
            {"name": "Nasdaq", "value": 15000, "change_percent": 2.0},
        ], "error": str(e)}


