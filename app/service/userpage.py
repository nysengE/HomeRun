import os
from datetime import datetime

from fastapi import Form, HTTPException
from sqlalchemy import select, func, delete, update
from sqlalchemy.exc import SQLAlchemyError

from app.model.club import Apply, Club, ClubAttach
from app.model.regions import Regions
from app.model.sports import Sports
from app.model.users import Users
from app.schema.mypage.userpage import ModifyClub

UPLOAD_PATH = 'C:/Java/nginx-1.26.2/nginx-1.26.2/html/homerun/img'

async def get_club_data(title: str = Form(...),
                        contents: str = Form(...),
                        people: str = Form(...),
                        sportsno:str = Form(...),
                        sigunguno: str = Form(...),
                        clubno: str =Form(...)) -> ModifyClub:
    try:
        return ModifyClub(title=title,
                       contents=contents,
                       people=int(people),
                       sportsno=int(sportsno),
                       sigunguno=int(sigunguno),
                       clubno = int(clubno))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"get_club_data 오류: {e}")


async def process_upload(files):
    attach = None
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

class UserpageService:
    @staticmethod
    def select_apply(userid, db):
        try:
            stmt = select(Apply.ano,
                          Apply.regdate.label('applyregdate'),
                          Apply.status,
                          Apply.userid.label('applyuserid'),
                          Apply.clubno,
                          Club.title,
                          Sports.name.label('sportsname')
                          ).select_from(Apply)\
                    .join(Club, Club.clubno == Apply.clubno)\
                    .join(Sports, Sports.sportsno == Club.sportsno)\
                    .where(Apply.userid == userid)

            result = db.execute(stmt).fetchall()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_apply 에서 오류 발생: {str(ex)}')
            db.rollback()

    @staticmethod
    def select_club(userid, db):
        try:
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
                          Sports.name.label('sportname'),
                          Regions.name.label('regionname')
                          ).select_from(Club) \
                .join(Sports, Club.sportsno == Sports.sportsno) \
                .join(Regions, Club.sigunguno == Regions.sigunguno) \
                .where(Club.userid == userid)

            result = db.execute(stmt).fetchall()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_club 에서 오류 발생: {str(ex)}')
            db.rollback()


    @staticmethod
    def select_applylist(clubno, db):
        try:
            stmt = select(Apply.ano,
                          Apply.userid,
                          Apply.regdate,
                          Apply.status
                          ).where(Apply.clubno == clubno)
            result = db.execute(stmt).fetchall()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_applylist 에서 오류 발생: {str(ex)}')
            db.rollback()
            return []


    @staticmethod
    def delete_club(clubno, db):
        try:

            stmt = delete(Club).where(Club.clubno == clubno)
            result = db.execute(stmt)

            db.commit()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ delete_club 에서 오류 발생: {str(ex)}')
            db.rollback()

    @staticmethod
    def update_apply(ano, db):
        try:

            stmt = update(Apply).values(status='승인')\
                .where(Apply.ano == ano)

            result = db.execute(stmt)

            db.commit()
            return result.rowcount > 0

        except SQLAlchemyError as ex:
            print(f'▶▶▶ update_apply 에서 오류 발생: {str(ex)}')
            db.rollback()

    @staticmethod
    def update_club(club, db, attachs):
        try:
            # Club 테이블 수정
            stmt_update = update(Club).where(Club.clubno == club.clubno).values(
                title=club.title,
                contents=club.contents,
                people=club.people,
                sportsno=club.sportsno,
                sigunguno=club.sigunguno,
                modifydate=datetime.now().replace(microsecond=0)
            )
            result = db.execute(stmt_update)

            # ClubAttach 테이블 수정
            if attachs:
                stmt_attach = update(ClubAttach).where(ClubAttach.clubno == club.clubno).values(
                    fname=attachs[0],
                    fsize=attachs[1]
                )
                result = db.execute(stmt_attach)

            db.commit()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ update_club 에서 오류 발생: {str(ex)}')
            db.rollback()

    @staticmethod
    def selectone_club(clubno, db):
        try:

            # select c.clubno, c.title, c.registdate, ca.fname, s.name, r.name from club c
            # join clubattach ca on c.clubno = ca.clubno
            # join sports s on c.sportsno = s.sportsno
            # join regions r on c.sigunguno = r.sigunguno
            # order by c.registdate desc;

            stmt = select(Club.clubno,
                          Club.title,
                          Club.contents,
                          Club.people,
                          Club.sportsno,
                          Club.sigunguno,
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


            result = db.execute(stmt).fetchall()

            db.commit()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ selectone_club 오류 발생: {str(ex)}')
            db.rollback()

    @staticmethod
    def select_users(userid, db):
        try:

            stmt = select(Users.userno,
                          Users.userid,
                          Users.passwd,
                          Users.name,
                          Users.email,
                          Users.phone,
                          Users.birth
                          ).where(Users.userid == userid)

            result = db.execute(stmt).fetchall()


            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_users 오류 발생: {str(ex)}')
            db.rollback()

    def select_pwd(userid, db):
        try:

            stmt = select(Users.passwd).where(Users.userid == userid)

            result = db.execute(stmt).scalar_one_or_none()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_pwd 오류 발생: {str(ex)}')
            db.rollback()
