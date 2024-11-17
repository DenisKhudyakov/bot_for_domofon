import asyncio

from sqlalchemy import delete, select, distinct, text
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User
from bot.database.database import connections, engine


@connections
async def add_user(session: AsyncSession, username: str, telephone: int) -> None:
    user = User(
        username=username, telephone=telephone
    )
    session.add(user)
    await session.commit()


@connections
async def get_all_telephones(session: AsyncSession):
    result = await session.execute(select(User.telephone))  # Запрашиваем только поле telephone
    telephones = result.scalars().all()
    return telephones


@connections
async def get_telephone(session: AsyncSession, name: str) -> str:
    """
    Функция получения телефона по имени
    :param session:
    :param name:
    :return:
    """
    result = await session.execute(select(User.telephone).where(User.username == name))
    return result.scalar()


@connections
async def clear_database(session: AsyncSession) -> None:
    """
    Функция для очистки базы данных (удаление всех данных из всех таблиц).

    :param session: Асинхронная сессия SQLAlchemy.
    """
    try:
        await session.execute(delete(User))
        await session.commit()
    except Exception as e:
        await session.rollback()
        print(f"Ошибка при очистке таблицы Product: {e}")


