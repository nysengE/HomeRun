from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base

class Regions(Base):
    __tablename__ = 'regions'

    sigunguno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # 관계 설정
    clubs = relationship('Club', back_populates='regions')
    rentals = relationship('Rental', back_populates='regions')