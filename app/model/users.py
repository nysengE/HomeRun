from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model.base import Base

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}

    userno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    userid: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    passwd: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(255))
    birth: Mapped[datetime] = mapped_column(Date)
    registdate: Mapped[datetime] = mapped_column(default=datetime.now)
    modifydate: Mapped[datetime] = mapped_column(default=datetime.now)
    status: Mapped[int] = mapped_column(Integer, default=None, nullable=True)
    suspension: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    # Club과 관계
    clubs = relationship('Club', back_populates='users')
    # Rental 과 관계
    rentals = relationship('Rental', back_populates='users')
    # UserManage와 관계
    usermanages = relationship('UserManage', back_populates='users', cascade='all, delete-orphan')
