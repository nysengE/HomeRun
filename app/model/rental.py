from datetime import datetime
from sqlalchemy import ForeignKey, VARCHAR, INTEGER, DATE, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    sportsno: Mapped[int] = mapped_column(INTEGER, ForeignKey('sports.sportsno'))
    sigunguno: Mapped[int] = mapped_column(INTEGER, ForeignKey('regions.sigunguno'))
    # businessno: Mapped[int] = mapped_column(INTEGER, ForeignKey('business.id'))



class RentalAttach(Base):
    __tablename__ = 'rentalattach'

    scano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    spaceno: Mapped[int] = mapped_column(INTEGER, ForeignKey('rental.spaceno'), index=True)
    fname: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
    fsize: Mapped[int] = mapped_column(INTEGER, default=0)
    regdate: Mapped[datetime] = mapped_column(DATE, default=datetime.now)
