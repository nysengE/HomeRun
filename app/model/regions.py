from sqlalchemy.orm import Mapped, mapped_column

from app.model.base import Base


class Regions(Base):
    __tablename__ = 'regions'

    sigunguno: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]