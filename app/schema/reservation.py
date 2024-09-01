from pydantic import BaseModel
from datetime import date

class ReservationCreate(BaseModel):
    spaceno: int
    resdate: str  # 날짜 문자열
    restime: str
    people: int
    price: int

class ReservationResponse(BaseModel):
    resno: int
    spaceno: int
    resdate: date
    restime: str
    resstatus: int
