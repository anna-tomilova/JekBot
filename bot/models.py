from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, BigInteger

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    user_id = mapped_column(BigInteger, primary_key=True)
    score = mapped_column(Integer, default=1000)
    spins = mapped_column(Integer, default=0)
    loss_streak = mapped_column(Integer, default=0)
