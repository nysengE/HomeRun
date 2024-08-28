from datetime import datetime
from sqlalchemy import ForeignKey, VARCHAR, INTEGER, DATE, String
from sqlalchemy.orm import Mapped, mapped_column

from app.model.base import Base


class Rental(Base):
    __tablename__ = 'rental'

    spaceno: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(VARCHAR(500))
    contents: Mapped[str] = mapped_column(VARCHAR(500))
    people: Mapped[int] = mapped_column(INTEGER, default=0)
    price: Mapped[int] = mapped_column(INTEGER, default=0)
    regisdate: Mapped[datetime] = mapped_column(DATE, default=datetime.now)
    modifydate: Mapped[datetime] = mapped_column(DATE, onupdate=datetime.now)
    zipcode: Mapped[str] = mapped_column(String(10))
    businessno: Mapped[int] = mapped_column(INTEGER)
    sportsno: Mapped[int] = mapped_column(INTEGER)
    sigunguno: Mapped[int] = mapped_column(INTEGER)
    # businessno: Mapped[int] = mapped_column(INTEGER, ForeignKey('business.id'))
    # sportsno: Mapped[int] = mapped_column(INTEGER, ForeignKey('sports.id'))
    # sigunguno: Mapped[int] = mapped_column(INTEGER, ForeignKey('region.id'))
