from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Подключение к базе данных
DATABASE_URL = settings.database_url
engine = create_async_engine(DATABASE_URL, echo=True)

# Настройка сессии
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Декларативная база для моделей
Base = declarative_base()

# Генератор для работы с сессиями
async def get_db():
    async with SessionLocal() as session:
        yield session
