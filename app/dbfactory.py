from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import config

from app.model import club, sports, regions, users, rental

engine = create_engine(config.dbconn, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def db_startup():
    club.Base.metadata.create_all(engine)
    sports.Base.metadata.create_all(engine)
    regions.Base.metadata.create_all(engine)
    users.Base.metadata.create_all(engine)
    rental.Base.metadata.create_all(engine)

async def db_shutdown():
    pass