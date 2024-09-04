from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Integer, String, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model.base import Base


class Notification(Base):
    __tablename__ = 'notification'
    __tablename_args__ = {'sqlite_autoincrement': True}

    notino: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(VARCHAR(255), index=True)
    userid: Mapped[str] = mapped_column(VARCHAR(255), ForeignKey('users.userid'), nullable=False)
    registdate: Mapped[datetime] = mapped_column(default=datetime.now)
    contents: Mapped[str] = mapped_column(VARCHAR(1000))
    modifydate = mapped_column(DateTime, onupdate=datetime.now)

    attachs = relationship('NotiAttach', back_populates='notifications')  # 하나의 notification에는 여러 attach 가능 (1:n)

class NotiAttach(Base):
    __tablename__ = 'notiattach'

    attno: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    notino: Mapped[int] = mapped_column(Integer, ForeignKey('notification.notino'), index=True)
    fname: Mapped[str] = mapped_column(VARCHAR(1000), nullable=False)  # String 타입 지정
    fsize: Mapped[int] = mapped_column(Integer, default=0)  # Integer 타입 지정
    regdate: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)  # DateTime 타입 지정

    notifications = relationship('Notification', back_populates='attachs')  # 하나의 attach는 하나의 notification에 속함 (1:1)