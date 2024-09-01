from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.model import rental, sports, regions, reservation, payment
from app.model.regions import Region
from app.model.sports import Sports
from app.setting import config

engine = create_engine(config.dbconn, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def db_startup():
    rental.Base.metadata.create_all(engine)
    sports.Base.metadata.create_all(engine)
    regions.Base.metadata.create_all(engine)
    reservation.Base.metadata.create_all(engine)
    payment.Base.metadata.create_all(engine)


    # 세션 생성
    db: Session = SessionLocal()
    try:
        # 기존에 데이터가 있는지 확인
        if db.query(Region).count() == 0:  # 테이블에 데이터가 없는 경우에만 삽입
            # 지역 목록
            region_names = [
                "종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구",
                "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구",
                "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구",
                "서초구", "강남구", "송파구", "강동구"
            ]

            # 지역 데이터 삽입
            for index, name in enumerate(region_names, start=1):
                region = Region(sigunguno=index, name=name)
                db.add(region)
            db.commit()

        # Sports 테이블 데이터 삽입
        if db.query(Sports).count() == 0:  # 테이블에 데이터가 없는 경우에만 삽입
            sports_data = [
                (1, '축구'),
                (2, '야구'),
                (3, '농구'),
                (4, '테니스'),
                (5, '기타')
            ]
            for sportsno, name in sports_data:
                sport = Sports(sportsno=sportsno, name=name)
                db.add(sport)
            db.commit()


    finally:
        db.close()


async def db_shutdown():
    pass
