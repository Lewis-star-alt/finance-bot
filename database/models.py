from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from sqlalchemy import Float, Integer, String, DateTime
from typing import Optional



class Base(DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(index=True)

    amount: Mapped[float] = mapped_column(Float)

    category: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(200), default=None)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


