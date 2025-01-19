from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.services.binance import fetch_candlestick_data

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
        raw_data = await fetch_candlestick_data(symbol, interval)
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
        return {"error": str(e)}
