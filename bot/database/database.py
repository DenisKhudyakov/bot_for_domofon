from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from bot.config import DATABASE_URL
from bot.database.models import Base

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def connections(func):
    """
    Декоратор для подключения к БД
    :param func: Любая из функций, которая работает с БД
    :return:
    """
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper


async def init_database():
    """
    Функция создания таблицы и инициализации БД
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
