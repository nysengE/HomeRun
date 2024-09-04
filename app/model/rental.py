from datetime import datetime, time
from sqlalchemy import ForeignKey, VARCHAR, INTEGER, DATE, String, Float, TIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base


class RentalAttach(Base):
    __tablename__ = 'rentalattach'

    scano: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True, index=True)
    spaceno: Mapped[int] = mapped_column(INTEGER, ForeignKey('rental.spaceno'), index=True)
    fname: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
    fsize: Mapped[int] = mapped_column(INTEGER, default=0)
    regdate: Mapped[datetime] = mapped_column(DATE, default=datetime.now)
    rentals = relationship('Rental', back_populates='attachs')


class Rental(Base):
    __tablename__ = 'rental'
    __table_args__ = {'sqlite_autoincrement': True}

    spaceno: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(VARCHAR(500))
    contents: Mapped[str] = mapped_column(VARCHAR(500))
    people: Mapped[int] = mapped_column(INTEGER, default=0)
    price: Mapped[int] = mapped_column(INTEGER, default=0)
    address: Mapped[str] = mapped_column(VARCHAR(300))
    regisdate: Mapped[datetime] = mapped_column(DATE, default=datetime.now)
    modifydate: Mapped[datetime] = mapped_column(DATE, default=datetime.now, onupdate=datetime.now)
    availdate: Mapped[datetime] = mapped_column(DATE)     # 공간이용가능 날짜
    availtime: Mapped[datetime] = mapped_column(TIME)     # 공간이용가능 시간
    latitude: Mapped[float] = mapped_column(Float)  # 위도
    longitude: Mapped[float] = mapped_column(Float)  # 경도
    sportsno: Mapped[int] = mapped_column(INTEGER, ForeignKey('sports.sportsno'))
    sigunguno: Mapped[int] = mapped_column(INTEGER, ForeignKey('regions.sigunguno'))
    userid: Mapped[int] = mapped_column(INTEGER, ForeignKey('users.userid'))
    attachs = relationship('RentalAttach', back_populates='rentals')  # 하나의 gallery는 하나 이상의 attach 존재 (1:n)
    sports = relationship("Sports", back_populates="rentals")
    payments = relationship('Payment', back_populates='rentals')  # Reservation과의 관계 설정
    regions = relationship('Regions', back_populates='rentals')  # Reservation과의 관계 설정
    users = relationship('Users', back_populates='rentals')


