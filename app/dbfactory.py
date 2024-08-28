from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import rental
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

async def db_shutdown():
    pass
