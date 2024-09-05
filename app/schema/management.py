from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class NotificationBase(BaseModel):
    title: str
    userid: str
    contents: str
    status: Optional[str] = 'public'  # 기본값을 '공개'로 설정

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    status: str

class NotificationResponse(NotificationBase):
    notino: int
    regdate: datetime
    last_modified: Optional[datetime]

    class Config:
        from_attributes = True  # SQLAlchemy 모델과 호환되도록 설정

class NotificationStatistics(BaseModel):
    sportsno: int
    count: int

class AgeGroupStatistics(BaseModel):
    sportsno: int
    age_10s: int
    age_20s: int
    age_30s: int
    age_40s: int
    age_50s_and_above: int

class StatisticsResponse(BaseModel):
    posts_count: List[NotificationStatistics]
    age_group_count: List[AgeGroupStatistics]

class StatusUpdate(BaseModel):
    status: str
    table: str
