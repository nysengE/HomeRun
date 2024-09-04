from datetime import datetime, date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.model.base import Base


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}

    userno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    userid: Mapped[str] = mapped_column(String(255),unique=True, nullable=False)
    passwd: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(255))
    registdate: Mapped[datetime] = mapped_column(default=datetime.now)
    modifydate: Mapped[datetime] = mapped_column(default=datetime.now)
    birth: Mapped[datetime] = mapped_column(Date)