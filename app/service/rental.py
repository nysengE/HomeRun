import os
from datetime import datetime

from fastapi import Form
from sqlalchemy import insert, select, distinct, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, Session

from app.model.rental import Rental, RentalAttach, RentalAvail
from app.schema.rental import NewRental

UPLOAD_PATH = 'C:/java/nginx-1.26.2/html/cdn/img/'

def get_rental_data(title: str = Form(...), contents: str = Form(...),
                    people: int = Form(...), price: int = Form(...),
                    address: str = Form(...), latitude: float = Form(...),
                    longitude: float = Form(...), sportsno: int = Form(...),
                    sigunguno: int = Form(...), available_dates: str = Form(...)):
    return NewRental(
        title=title,
        contents=contents,
        people=people,
        price=price,
        address=address,
        latitude=latitude,
        longitude=longitude,
        sportsno=sportsno,
        sigunguno=sigunguno,
        available_dates=available_dates  # 추가된 부분
    )

async def process_upload(files):
    attachs = []  # 업로드된 파일 정보를 저장하기 위한 리스트 생성
    today = datetime.today().strftime('%Y%m%d%H%M%S')  # 파일 이름에 사용할 UUID 생성
    for file in files:
        if file.filename != '' and file.size > 0:
            nfname = f'{today}_{file.filename}'
            fname = os.path.join(UPLOAD_PATH, nfname)  # 업로드할 파일 경로 생성
            content = await file.read()  # 비동기로 파일 내용 읽기
            with open(fname, 'wb') as f:
                f.write(content)
            attach = [nfname, file.size]  # 업로드된 파일 정보를 리스트에 저장
            attachs.append(attach)

    return attachs

class RentalService:
    @staticmethod
    def insert_rental(rent, attachs, db: Session):
        try:
            stmt = insert(Rental).values(
                title=rent.title,  # 점 표기법으로 수정
                contents=rent.contents,
                people=rent.people,
                price=rent.price,
                address=rent.address,
                latitude=rent.latitude,
                longitude=rent.longitude,
                sportsno=rent.sportsno,
                sigunguno=rent.sigunguno,
                regisdate=datetime.now()
            )
            result = db.execute(stmt)
            inserted_spaceno = result.inserted_primary_key[0]

            # 사용 가능 날짜 처리
            if rent.available_dates:  # available_dates가 있는 경우에만 처리
                dates = rent.available_dates.split(', ')
                for date_str in dates:
                    try:
                        avail_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        new_avail = RentalAvail(availdate=avail_date, availstatus=1, spaceno=inserted_spaceno)
                        db.add(new_avail)
                    except ValueError as ve:
                        print(f'Invalid date format for {date_str}: {ve}')

            for attach in attachs:
                data = {
                    'fname': attach[0],
                    'fsize': attach[1],
                    'spaceno': inserted_spaceno
                }
                stmt = insert(RentalAttach).values(data)
                db.execute(stmt)

            db.commit()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_rental에서 오류 발생: {str(ex)}')
            db.rollback()
            raise

    @staticmethod
    def insert_avail_dates(spaceno: int, dates: list, db: Session):
        """
        사용 가능 날짜를 RentalAvail 테이블에 저장하는 메서드
        """
        try:
            for date_str in dates:
                try:
                    avail_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    new_avail = RentalAvail(availdate=avail_date, availstatus=1, spaceno=spaceno)
                    db.add(new_avail)
                except ValueError as ve:
                    print(f'Invalid date format for {date_str}: {ve}')
            db.commit()
        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_avail_dates에서 오류 발생: {str(ex)}')
            db.rollback()
            raise
    @staticmethod
    def select_rentals(db: Session, limit=25):
        try:
            rentals = db.query(Rental).options(joinedload(Rental.attachs)) \
                .order_by(Rental.spaceno.desc()).limit(limit).all()
            return rentals

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_rentals에서 오류 발생: {str(ex)}')
            db.rollback()
            return []  # 예외 발생 시 빈 리스트 반환

    @staticmethod
    def select_one_rental(spaceno, db: Session):
        try:
            stmt = select(Rental).options(joinedload(Rental.attachs)) \
                .where(Rental.spaceno == spaceno)
            result = db.execute(stmt).scalars().first()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_one_rental에서 오류 발생: {str(ex)}')
            db.rollback()
            return None  # 예외 발생 시 None 반환