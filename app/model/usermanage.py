from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey  # DateTime 타입 추가
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model.base import Base

class UserManage(Base):
    __tablename__ = 'usermanage'

    umno: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    userid: Mapped[str] = mapped_column(String(255), ForeignKey('users.userid'), nullable=False)  # 외래 키 설정
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=True)  # 중복 가능하게 설정
    regdate: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)  # 중복 가능하게 설정

    # User와의 관계 설정
    users = relationship('Users', back_populates='usermanages')
