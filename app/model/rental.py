from datetime import datetime, time
from sqlalchemy import ForeignKey, VARCHAR, INTEGER, DATE, String, Float, TIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base


class Rental(Base):
    __tablename__ = 'rental'

    spaceno: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(VARCHAR(500))
    contents: Mapped[str] = mapped_column(VARCHAR(500))
    people: Mapped[int] = mapped_column(INTEGER, default=0)
    price: Mapped[int] = mapped_column(INTEGER, default=0)
    address: Mapped[str] = mapped_column(VARCHAR(300))
    regisdate: Mapped[datetime] = mapped_column(DATE, default=datetime.now)
    modifydate: Mapped[datetime] = mapped_column(DATE, default=datetime.now, onupdate=datetime.now)
    availdate: Mapped[datetime] = mapped_column(DATE)     # 공간이용가능 날짜
    availtime: Mapped[time] = mapped_column(TIME)     # 공간이용가능 시간
    latitude: Mapped[float] = mapped_column(Float)  # 위도
    longitude: Mapped[float] = mapped_column(Float)  # 경도
    sportsno: Mapped[int] = mapped_column(INTEGER, ForeignKey('sports.sportsno'))
    sigunguno: Mapped[int] = mapped_column(INTEGER, ForeignKey('regions.sigunguno'))
    # businessno: Mapped[int] = mapped_column(INTEGER, ForeignKey('business.id'))
    attachs = relationship('RentalAttach', back_populates='rental')  # 하나의 gallery는 하나 이상의 attach 존재 (1:n)
    sports = relationship("Sports", back_populates="rental")
    payment = relationship('Payment', back_populates='rental')  # Reservation과의 관계 설정
    sigungu = relationship('Region', back_populates='rental')  # Reservation과의 관계 설정
    # avail_dates = relationship('RentalAvail', back_populates='rental')  # RentalAvail과의 관계 설정




class RentalAttach(Base):
    __tablename__ = 'rentalattach'

    scano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    spaceno: Mapped[int] = mapped_column(INTEGER, ForeignKey('rental.spaceno'), index=True)
    fname: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
    fsize: Mapped[int] = mapped_column(INTEGER, default=0)
    regdate: Mapped[datetime] = mapped_column(DATE, default=datetime.now)
    rental = relationship('Rental', back_populates='attachs')



# class RentalAvail(Base):
#     __tablename__ = 'rentalavail'
#
#     availno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
#     availdate: Mapped[datetime] = mapped_column(DATE)
#     starttime: Mapped[time] = mapped_column(TIME)  # 시작 시간
#     endtime: Mapped[time] = mapped_column(TIME)    # 종료 시간
#     availstatus: Mapped[int] = mapped_column(INTEGER, default=1)
#     spaceno: Mapped[int] = mapped_column(INTEGER, ForeignKey('rental.spaceno'))
#     rental = relationship('Rental', back_populates='avail_dates')  # Rental과의 관계 설정
#
#
#
#
#
