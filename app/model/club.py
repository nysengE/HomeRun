from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base


class Club(Base):
    __tablename__ = 'club'

    clubno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    contents: Mapped[str]
    people: Mapped[int] = mapped_column(default=0)
    registdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    modifydate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    views: Mapped[int] = mapped_column(default=0)
    sportsno: Mapped[int] = mapped_column(ForeignKey('sports.sportsno'))
    sigunguno: Mapped[int] = mapped_column(ForeignKey('regions.sigunguno'))
    userid: Mapped[str]
    attachs = relationship('ClubAttach', back_populates='club')
    replys = relationship('Reply', back_populates='club')

class ClubAttach(Base):
    __tablename__ = 'clubattach'

    cano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    clubno: Mapped[int] = mapped_column(ForeignKey('club.clubno'), index=True)
    fname: Mapped[str] = mapped_column(nullable=False)
    fsize: Mapped[int] = mapped_column(default=0)
    regdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    club = relationship('Club', back_populates='attachs')

class Apply(Base):
    __tablename__ = 'apply'

    ano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    regdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    status: Mapped[str] = mapped_column(default='대기중', nullable=True)
    userid: Mapped[str] = mapped_column(ForeignKey('users.userid'))
    clubno: Mapped[int] = mapped_column(ForeignKey('club.clubno'))

class Reply(Base):
    __tablename__ = 'reply'

    rno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    reply: Mapped[str] = mapped_column(index=True)
    regdate: Mapped[datetime] = mapped_column(default=lambda: datetime.now().replace(microsecond=0))
    userid: Mapped[str] = mapped_column(ForeignKey('users.userid'), index=True)
    clubno: Mapped[int] = mapped_column(ForeignKey('club.clubno'))
    rpno: Mapped[int] = mapped_column(ForeignKey('reply.rno'))
    club = relationship('Club', back_populates='replys')

