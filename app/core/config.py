from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str

    # API Keys
    binance_api_key: str
    okx_api_key: str
    okx_secret_key: str
    coinmarketcap_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()

