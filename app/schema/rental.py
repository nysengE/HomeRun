from datetime import date, time
from typing import List

from pydantic import BaseModel

class NewRental(BaseModel):
    title: str
    contents: str
    people: int
    price: int
    address: str
    latitude: float  # 추가된 필드
    longitude: float  # 추가된 필드
    sportsno: int
    sigunguno: int
    availdate: date
    availtime: time

    class Config:
        from_attributes = True


