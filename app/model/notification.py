from datetime import datetime

from sqlalchemy import ForeignKey, Column, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base

class Notification(Base):
    __tablename__ = 'notification'

    notino: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    userid: Mapped[str] = mapped_column(default='Joseph')
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    contents: Mapped[str]
    attachs = relationship('NotiAttach', back_populates='notification')  # 하나의 notification에는 여러 attach 가능 (1:n)
    last_modified = Column(DateTime, onupdate=func.now())

class NotiAttach(Base):
    __tablename__ = 'notiattach'

    attno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    notino: Mapped[int] = mapped_column(ForeignKey('notification.notino'), index=True)
    fname: Mapped[str] = mapped_column(nullable=False)
    fsize: Mapped[int] = mapped_column(default=0)
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    notification = relationship('Notification', back_populates='attachs')  # 하나의 attach는 하나의 notification에 속함 (1:1)
