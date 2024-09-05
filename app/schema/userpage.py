from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class RequestClubno(BaseModel):
    clubno: int

class ModifyClub(BaseModel):
    title: str
    contents: str
    people: int
    sportsno: int
    sigunguno: int
    clubno: int

class ModifyUser(BaseModel):
    name: str
    passwd: Optional[str] = None
    email: str
    phone: str
    birth: Optional[date] = None

class CheckUser(BaseModel):
    passwd: str
