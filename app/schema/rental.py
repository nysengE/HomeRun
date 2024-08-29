from pydantic import BaseModel

class NewRental(BaseModel):
    title: str
    contents: str
    people: int
    price: int
    zipcode: str
    sportsno: int
    sigunguno: int

    class Config:
        from_attributes = True
