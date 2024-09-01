from datetime import datetime

from sqlalchemy import ForeignKey, VARCHAR, INTEGER, DATE, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base


class Payments(Base):
    __tablename__ = 'payments'

    payno: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True, index=True)
    totalprice: Mapped[int] = mapped_column(INTEGER)
    paydate: Mapped[datetime] = mapped_column(DATE, default=datetime.now)
    resno: Mapped[int] = mapped_column(INTEGER, ForeignKey('reservation.resno'))
    reservation = relationship("Reservation", back_populates="pay")