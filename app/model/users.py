from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.model.base import Base


class Regions(Base):
    __tablename__ = 'users'

    userno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    userid: Mapped[str] = mapped_column(unique=True, nullable=False)
    passwd: Mapped[str]
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    registdate: Mapped[datetime] = mapped_column(default=datetime.now)
    modifydate: Mapped[datetime] = mapped_column(default=datetime.now)
    birth: Mapped[str]