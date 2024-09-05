from pydantic import BaseModel

# SuspendUserRequest 모델 정의
class SuspendUserRequest(BaseModel):
    userid: str
    reason: str
    duration: int

# UnsuspendUserRequest 모델 정의
class UnsuspendUserRequest(BaseModel):
    userid: str
