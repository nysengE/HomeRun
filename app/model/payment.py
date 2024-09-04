from datetime import datetime, time, date

from sqlalchemy import ForeignKey, INTEGER, DATE, String, TIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base


class Payment(Base):
    __tablename__ = 'payment'
    __tablename_args__ = {'sqlite_autoincrement': True}

    payno: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True, index=True)
    paydate: Mapped[date] = mapped_column(DATE, default=datetime.now().date())    #결제일
    totalprice: Mapped[int] = mapped_column(INTEGER)   # 총가격
    resdate: Mapped[date] = mapped_column(DATE)      # 예약 날짜
    restime: Mapped[time] = mapped_column(TIME)      # 예약 시간
    resprice: Mapped[int] = mapped_column(INTEGER)  # 예약 가격
    respeople: Mapped[int] = mapped_column(INTEGER)  # 예약 인원
    userid: Mapped[str] = mapped_column(String(255), ForeignKey('users.userid'), nullable=False)
    spaceno: Mapped[int] = mapped_column(INTEGER, ForeignKey('rental.spaceno'))   # 공간번호
    rentals = relationship("Rental", back_populates="payments")


    # resend: Mapped[time] = mapped_column(TIME)    # 예약 종료 시간
    # resstart: Mapped[time] = mapped_column(TIME)  # 예약 시작 시간

