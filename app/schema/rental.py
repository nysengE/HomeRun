from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class RentalBase(BaseModel):
    title: str = Field(..., description="공간 대여의 제목")
    contents: str = Field(..., description="공간 대여의 내용")
    people: int = Field(..., gt=0, description="대여 가능한 최대 인원수")
    price: int = Field(..., gt=0, description="대여 가격")
    zipcode: str = Field(..., max_length=10, description="우편번호")
    businessno: int = Field(..., description="사업자 회원 번호")
    sportsno: int = Field(..., description="운동 종목 번호")
    sigunguno: int = Field(..., description="지역 번호")

class RentalCreate(RentalBase):
    """데이터베이스에 새로운 공간 대여 정보를 추가하기 위한 스키마"""
    pass

class Rental(RentalBase):
    spaceno: int = Field(..., description="공간 번호")
    regisdate: Optional[date] = Field(None, description="등록 일자")
    modifydate: Optional[date] = Field(None, description="수정 일자")

    class Config:
        from_attributes = True  # orm_mode 대신 사용
