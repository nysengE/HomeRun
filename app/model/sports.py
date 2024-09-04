from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base

class Sports(Base):
    __tablename__ = 'sports'

    sportsno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # 관계 설정
    clubs = relationship('Club', back_populates='sports')
    rentals = relationship('Rental', back_populates='sports')