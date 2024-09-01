from datetime import datetime

from sqlalchemy import ForeignKey, VARCHAR, INTEGER, DATE, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base


class Reservation(Base):
    __tablename__ = 'reservation'

    resno: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True, index=True)
    resdate: Mapped[datetime] = mapped_column(DATE)      # 예약 날짜
    restime: Mapped[str] = mapped_column(VARCHAR(50))   # VARCHAR로 시간 범위 저장 (예: "14:00 - 16:00")
    resstatus: Mapped[int] = mapped_column(INTEGER, default=1)  # 예약 상태 (1: 확정, 0: 대기 등)
    people: Mapped[int] = mapped_column(INTEGER)  # 예약 인원
    price: Mapped[int] = mapped_column(INTEGER)  # 예약 가격
    # id: Mapped[str] = mapped_column(VARCHAR(255), ForeignKey('user.id'))
    spaceno: Mapped[int] = mapped_column(INTEGER, ForeignKey('rental.spaceno'))
    pay = relationship("Payments", back_populates="reservation")
    rental = relationship("Rental", back_populates="reservation")