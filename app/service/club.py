import os
from datetime import datetime

from fastapi import Form, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.model.club import Club, ClubAttach
from app.model.regions import Regions
from app.model.sports import Sports
from app.schema.club import NewClub

UPLOAD_PATH = 'C:/Java/nginx-1.26.2/nginx-1.26.2/html/homerun/img'

async def get_club_data(title: str = Form(...),
                  contents: str = Form(...),
                  people: str = Form(...),
                  sportsno:str = Form(...),
                  sigunguno: str = Form(...),
                  userid: str = Form(...)) -> NewClub:
    try:
        return NewClub(title=title,
                       contents=contents,
                       people=int(people),
                       sportsno=int(sportsno),
                       sigunguno=int(sigunguno),
                       userid=userid)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"get_club_data 오류: {e}")

async def process_upload(files):
    # attachs = []
    today = datetime.today().strftime('%Y%m%d%H%M%S')
    # for file in files:
    if files.filename != '' and files.size > 0:
        nfname = f'{today}{files.filename}'
        fname = os.path.join(UPLOAD_PATH, nfname)
        content = await files.read()
        with open(fname, 'wb') as f:
            f.write(content)
        attach = [nfname, files.size]
        # attachs.append(attach)
    return attach

class ClubService:
    @staticmethod
    def insert_club(club, attach, db):
        try:
            # sportsno = club.sportsno
            # sigunguno = club.sigunguno
            # people = club.people
            stmt = insert(Club).values(title=club.title, contents=club.contents, people=club.people,
                                       sportsno=club.sportsno, sigunguno=club.sigunguno, userid=club.userid)
            result = db.execute(stmt)

            inserted_clubno = result.inserted_primary_key[0]
            # for attach in attachs:
            data = {'fname': attach[0], 'fsize': attach[1], 'clubno': inserted_clubno}
            # print(data)
            stmt2 = insert(ClubAttach).values(data)
            result = db.execute(stmt2)

            db.commit()

            return result


        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_club 에서 오류 발생: {str(ex)}')
            db.rollback()

    @staticmethod
    def select_club(db):
    # select c.clubno, c.title, c.registdate, ca.fname, s.name, r.name from club c
    # join clubattach ca on c.clubno = ca.clubno
    # join sports s on c.sportsno = s.sportsno
    # join regions r on c.sigunguno = r.sigunguno
    # order by c.registdate desc;
        try:
            from sqlalchemy import func
            stmt3 = select(Club.clubno,
                          Club.title,
                          func.strftime('%Y-%m-%d', Club.registdate).label('registdate'),
                          ClubAttach.fname,
                          Sports.name.label('sportname'),
                          Regions.name.label('regionname')
                    ).select_from(Club)\
                    .join(ClubAttach, Club.clubno == ClubAttach.clubno)\
                    .join(Sports, Club.sportsno == Sports.sportsno)\
                    .join(Regions, Club.sigunguno == Regions.sigunguno)\
                    .order_by(Club.registdate.desc())
            result = db.execute(stmt3).fetchall()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ service select_club에서 오류 발생: {str(ex)}')
            db.rollback()
