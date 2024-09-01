from datetime import datetime, time, date

from pydantic import BaseModel

class ReservationCreate(BaseModel):
    spaceno: int
    resdate: date  # 날짜 타입으로 변경
    resstart: time  # 시작 시간
    resend: time  # 종료 시간
    people: int
    price: int

class ReservationResponse(BaseModel):
    resno: int
    spaceno: int
    resdate: date
    resstart: time
    resend: time
    resstatus: int
