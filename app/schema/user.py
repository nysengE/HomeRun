from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class NewUser(BaseModel):
    userid: str
    passwd: str
    name: str
    email: str
    birth: date
    phone: str
    captcha: str
    business_id: Optional[str] = Field(None, description="Business ID")
    businessno: Optional[str] = Field(None, description="Business upload number")

class FindIdRequest(BaseModel):
    name: str
    email: str

class FindPasswordRequest(BaseModel):
    userid: str
    name: str