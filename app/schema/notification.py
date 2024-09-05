from pydantic import BaseModel

class NewNotification(BaseModel):
    userid: str
    title: str
    contents: str

