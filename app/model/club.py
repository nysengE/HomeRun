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
    registdate: Mapped[datetime] = mapped_column(default=datetime.now)
    modifydate: Mapped[datetime] = mapped_column(default=datetime.now)
    views: Mapped[int] = mapped_column(default=0)
    sportsno: Mapped[int] = mapped_column(ForeignKey('sports.sportsno'))
    sigunguno: Mapped[int] = mapped_column(ForeignKey('regions.sigunguno'))
    userid: Mapped[str]
    attachs = relationship('ClubAttach', back_populates='club')

class ClubAttach(Base):
    __tablename__ = 'clubattach'

    cano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    clubno: Mapped[int] = mapped_column(ForeignKey('club.clubno'), index=True)
    fname: Mapped[str] = mapped_column(nullable=False)
    fsize: Mapped[int] = mapped_column(default=0)
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    club = relationship('Club', back_populates='attachs')

class Apply(Base):
    __tablename__ = 'apply'

    ano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    regdate: Mapped[datetime] = mapped_column(default=datetime.now, nullable=True)
    status: Mapped[str] = mapped_column(default='대기중', nullable=True)
    userid: Mapped[str] = mapped_column(ForeignKey('users.userid'))
    clubno: Mapped[int] = mapped_column(ForeignKey('club.clubno'))


