from datetime import datetime, time, date

from sqlalchemy import ForeignKey, VARCHAR, INTEGER, DATE, String, TIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base


class Payment(Base):
    __tablename__ = 'payment'

    payno: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True, index=True)
    paydate: Mapped[date] = mapped_column(DATE, default=datetime.now().date())    #결제일
    totalprice: Mapped[int] = mapped_column(INTEGER)   # 총가격
    resdate: Mapped[date] = mapped_column(DATE)      # 예약 날짜
    restime: Mapped[time] = mapped_column(TIME)      # 예약 시간
    resprice: Mapped[int] = mapped_column(INTEGER)  # 예약 가격
    respeople: Mapped[int] = mapped_column(INTEGER)  # 예약 인원
    # id: Mapped[str] = mapped_column(VARCHAR(255), ForeignKey('user.id'))
    spaceno: Mapped[int] = mapped_column(INTEGER, ForeignKey('rental.spaceno'))   # 공간번호
    rental = relationship("Rental", back_populates="payment")


    # resend: Mapped[time] = mapped_column(TIME)    # 예약 종료 시간
    # resstart: Mapped[time] = mapped_column(TIME)  # 예약 시작 시간

