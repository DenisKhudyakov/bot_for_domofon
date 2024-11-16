import asyncio

from sqlalchemy import delete, select, distinct
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


async def main():
    telephones = await get_all_telephones()
    print(f"Список телефонов пользователей: {telephones}")

# Запуск функции
asyncio.run(main())