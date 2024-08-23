from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.model.base import Base

class Notification(Base):
    __tablename__ = 'notification'

    notino: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    contents: Mapped[str]
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    userid: Mapped[str] = mapped_column(default='Joseph', index=True)
