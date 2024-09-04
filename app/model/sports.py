from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.model.base import Base


class Sports(Base):
    __tablename__ = 'sports'
    __table_args__ = {'sqlite_autoincrement': True}

    sportsno: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))