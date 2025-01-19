from app.core.config import settings

def test_settings():
    assert settings.database_url is not None
    assert settings.binance_api_key is not None
    assert settings.okx_api_key is not None
    assert settings.okx_secret_key is not None
    assert settings.coinmarketcap_api_key is not None
