from typing import Optional

from pydantic import BaseModel, Field


class NewClub(BaseModel):
    title: str
    contents: str
    people: int
    sportsno: int
    sigunguno: int
    userid: str

class NewReply(BaseModel):
    reply: str
    userid: str
    clubno: int
    rpno: Optional[int] = Field(default=None)