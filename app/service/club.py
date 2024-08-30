import os
from datetime import datetime

from fastapi import Form, HTTPException
from sqlalchemy import insert, select, func, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.model.club import Club, ClubAttach, Apply, Reply
from app.model.regions import Regions
from app.model.sports import Sports
from app.schema.club.club import NewClub

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


    @staticmethod
    def selectone_club(clubno, db):
        try:
            # 조회수
            stmt = update(Club).where(Club.clubno == clubno) \
                .values(views=Club.views + 1)
            db.execute(stmt)

# select c.clubno, c.title, c.registdate, ca.fname, s.name, r.name from club c
# join clubattach ca on c.clubno = ca.clubno
# join sports s on c.sportsno = s.sportsno
# join regions r on c.sigunguno = r.sigunguno
# order by c.registdate desc;

            stmt = select(Club.clubno,
                          Club.title,
                          Club.contents,
                          Club.people,
                          Club.registdate,
                          Club.modifydate,
                          func.strftime('%Y-%m-%d', Club.registdate).label('registdate'),
                          Club.modifydate,
                          Club.views,
                          Club.userid,
                          ClubAttach.fname.label('fname'),
                          Sports.name.label('sportname'),
                          Regions.name.label('regionname')
                          ).select_from(Club) \
                .join(ClubAttach, Club.clubno == ClubAttach.clubno) \
                .join(Sports, Club.sportsno == Sports.sportsno) \
                .join(Regions, Club.sigunguno == Regions.sigunguno) \
                .where(Club.clubno == clubno)


            # stmt = select(Club).options(joinedload(Club.attachs))\
            #         .where(Club.clubno == clubno)

            # stmt = (select(Club, ClubAttach, Sports, Regions)
            #         .join(ClubAttach, Club.clubno == ClubAttach.clubno)
            #         .join(Sports, Club.sportsno == Sports.sportsno)
            #         .join(Regions, Club.sigunguno == Regions.sigunguno)
            #         .where(Club.clubno == clubno))

            result = db.execute(stmt).fetchall()

            db.commit()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ selectone_club 오류 발생: {str(ex)}')
            db.rollback()

    @staticmethod
    def select_reply(clubno, db):
        try:
            stmt = select(Reply).options(joinedload(Reply.club))\
                    .where(Reply.clubno == clubno)\
                    .order_by(Reply.rpno)

            result = db.execute(stmt).fetchall()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_reply 오류 발생: {str(ex)}')
            db.rollback()

    @staticmethod
    def select_sports(db):
        try:
            stmt = select(Sports)

            return db.execute(stmt).fetchall()

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_sports 오류 발생: {str(ex)}')
            db.rollback()

    @staticmethod
    def select_regions(db):
        try:
            stmt = select(Regions)

            return db.execute(stmt).fetchall()

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_sports 오류 발생: {str(ex)}')
            db.rollback()


    @staticmethod
    def insert_apply(clubno, userid, db):
        try:
            stmt = insert(Apply).values(clubno=clubno, userid=userid)
            result = db.execute(stmt)
            db.commit()
            return result
        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_apply 에서 오류 발생: {str(ex)}')
            db.rollback()

    @staticmethod
    def insert_reply(db, reply):
        try:
             # rpno 부모 번호 임시 생성
            stmt = select(func.coalesce(func.max(Reply.rno), 0) + 1)
            next_rno = db.execute(stmt).scalar_one()

            stmt = insert(Reply).values(userid=reply.userid,
                                         reply=reply.reply, clubno=reply.clubno, rpno=next_rno)
            result = db.execute(stmt)

            db.commit()
            return result
        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_reply에서 오류 발생 : {str(ex)}')
            db.rollback()

    @staticmethod
    def insert_rreply(db, reply):
        try:
            stmt = insert(Reply).values(userid=reply.userid,
                                        reply=reply.reply, clubno=reply.clubno, rpno=reply.rpno)
            result = db.execute(stmt)

            db.commit()
            return result
        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_reply에서 오류 발생 : {str(ex)}')
            db.rollback()



