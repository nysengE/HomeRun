from datetime import datetime

from sqlalchemy import ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base

class Club(Base):
    __tablename__ = 'club'
    __table_args__ = {'sqlite_autoincrement': True}

    clubno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String(500),nullable=False)
    contents: Mapped[str] = mapped_column(String(500),nullable=False)
    people: Mapped[int] = mapped_column(Integer, default=0)
    registdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    modifydate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    views: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(10), default='open', nullable=False)
    closed_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    sportsno: Mapped[int] = mapped_column(ForeignKey('sports.sportsno'), nullable=False)
    sigunguno: Mapped[int] = mapped_column(ForeignKey('regions.sigunguno'), nullable=False)
    userid: Mapped[str] = mapped_column(String(255), ForeignKey('users.userid'), nullable=False)
    attachs = relationship('ClubAttach', back_populates='clubs')
    replys = relationship('Reply', back_populates='clubs')

    # 각 동호회는 하나의 스포츠 카테고리에 속함
    sports = relationship('Sports', back_populates='clubs')
    # 각 동호회는 하나의 지역에 속함
    regions = relationship('Regions', back_populates='clubs')
    # 각 동호회는 하나의 사용자에 의해 작성됨
    users = relationship('Users', back_populates='clubs')

class ClubAttach(Base):
    __tablename__ = 'clubattach'
    __table_args__ = {'sqlite_autoincrement': True}

    cano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    clubno: Mapped[int] = mapped_column(Integer, ForeignKey('club.clubno'), index=True)
    fname: Mapped[str] = mapped_column(String(1000), nullable=False)
    fsize: Mapped[int] = mapped_column(Integer, default=0)
    regdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    clubs = relationship('Club', back_populates='attachs')

class Apply(Base):
    __tablename__ = 'apply'
    __table_args__ = {'sqlite_autoincrement': True}

    ano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    regdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    status: Mapped[str] = mapped_column(String(255),default='대기중', nullable=True)
    userid: Mapped[str] = mapped_column(String(255),ForeignKey('users.userid'))
    clubno: Mapped[int] = mapped_column(Integer, ForeignKey('club.clubno'))

class Reply(Base):
    __tablename__ = 'reply'
    __table_args__ = {'sqlite_autoincrement': True}

    rno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    reply: Mapped[str] = mapped_column(String(255),index=True)
    regdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    userid: Mapped[str] = mapped_column(String(255),ForeignKey('users.userid'), index=True)
    clubno: Mapped[int] = mapped_column(Integer, ForeignKey('club.clubno'))
    rpno: Mapped[int] = mapped_column(Integer, ForeignKey('reply.rno'))
    clubs = relationship('Club', back_populates='replys')
