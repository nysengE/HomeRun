from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from app.model.club import Apply, Club
from app.model.regions import Regions
from app.model.sports import Sports


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
            print(f'▶▶▶ select_apply 에서 오류 발생: {str(ex)}')
            db.rollback()