from pydantic import BaseModel


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
    email: str
    phone: str
    birth: str

