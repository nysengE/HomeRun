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
    available_dates: List[str]  # 문자열 리스트로 변경

    class Config:
        from_attributes = True


