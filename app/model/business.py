from datetime import datetime

from sqlalchemy import String, Integer, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base

class Business(Base):
    __tablename__ = 'business'

    business_no: Mapped[int] =  mapped_column(primary_key=True, autoincrement=True, index=True)  # 회원 번호
    business_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)  # 아이디
    business_pwd: Mapped[str] = mapped_column(String(255))  # 비밀번호
    business_name: Mapped[str] = mapped_column(String(255))  # 이름
    businessno: Mapped[str] = mapped_column(String(255))  # 사업자 등록번호
    business_birth: Mapped[datetime] = mapped_column(Date)
    business_phone: Mapped[str] = mapped_column(String(50))
    registdate: Mapped[datetime] = mapped_column(default=datetime.now)
    modifydate: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    status: Mapped[int] = mapped_column(Integer, default=None, nullable=True)
    suspension: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)

    # 관계 설정 (1:N 관계)
    #rentals = relationship('Rental', back_populates='business')