from sqlalchemy.orm import Mapped, mapped_column

from app.model.base import Base


class Sports(Base):
    __tablename__ = 'sports'

    sportsno: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]