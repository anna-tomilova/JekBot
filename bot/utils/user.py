from sqlalchemy import select
from bot.database import SessionLocal
from bot.models import User

async def get_or_create_user(user_id: int, session) -> User:
    result = await session.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()

    if user:
        return user

    # Создаем нового пользователя, если не найден
    user = User(user_id=user_id)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
