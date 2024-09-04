from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base


class Club(Base):
    __tablename__ = 'club'
    __table_args__ = {'sqlite_autoincrement': True}

    clubno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String(255),nullable=False)
    contents: Mapped[str] = mapped_column(String(255))
    people: Mapped[int] = mapped_column(default=0)
    registdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    modifydate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    views: Mapped[int] = mapped_column(default=0)
    sportsno: Mapped[int] = mapped_column(ForeignKey('sports.sportsno'))
    sigunguno: Mapped[int] = mapped_column(ForeignKey('regions.sigunguno'))
    userid: Mapped[str] = mapped_column(String(255))
    attachs = relationship('ClubAttach', back_populates='club')
    replys = relationship('Reply', back_populates='club')

class ClubAttach(Base):
    __tablename__ = 'clubattach'
    __table_args__ = {'sqlite_autoincrement': True}

    cano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    clubno: Mapped[int] = mapped_column(ForeignKey('club.clubno'), index=True)
    fname: Mapped[str] = mapped_column(String(255), nullable=False)
    fsize: Mapped[int] = mapped_column(default=0)
    regdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    club = relationship('Club', back_populates='attachs')

class Apply(Base):
    __tablename__ = 'apply'
    __table_args__ = {'sqlite_autoincrement': True}

    ano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    regdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    status: Mapped[str] = mapped_column(String(255),default='대기중', nullable=True)
    userid: Mapped[str] = mapped_column(String(255),ForeignKey('users.userid'))
    clubno: Mapped[int] = mapped_column(ForeignKey('club.clubno'))

class Reply(Base):
    __tablename__ = 'reply'
    __table_args__ = {'sqlite_autoincrement': True}

    rno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    reply: Mapped[str] = mapped_column(String(255),index=True)
    regdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    userid: Mapped[str] = mapped_column(String(255),ForeignKey('users.userid'), index=True)
    clubno: Mapped[int] = mapped_column(ForeignKey('club.clubno'))
    rpno: Mapped[int] = mapped_column(ForeignKey('reply.rno'))
    club = relationship('Club', back_populates='replys')

