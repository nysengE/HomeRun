from pydantic import BaseModel


class NewClub(BaseModel):
    title: str
    contents: str
    people: int
    sportsno: int
    sigunguno: int
    userid: str