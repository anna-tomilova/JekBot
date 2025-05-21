from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, BigInteger

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    score: Mapped[int] = mapped_column(default=1000)
    spins: Mapped[int] = mapped_column(default=0)
    loss_streak: Mapped[int] = mapped_column(default=0)
