from sqlalchemy import ForeignKey, VARCHAR, INTEGER, DATE, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base


class Sport(Base):
    __tablename__ = 'sports'

    sportsno: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(VARCHAR(200))
    rentals = relationship("Rental", back_populates="sport")