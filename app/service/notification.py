from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model.notification import Notification

class NotificationService:
    @staticmethod
    def select_board(db, cpg):
        try:
            stbno = (cpg - 1) * 10
            from sqlalchemy import select
            stmt = (select(Notification.notino, Notification.title, Notification.contents,
                           Notification.regdate, Notification.userid)\
                           .order_by(Notification.notino.desc())\
                           .offset(stbno).limit(10))
            result = db.execute(stmt)
            return result

        except SQLAlchemyError as ex:
            print(f'▷▷▷select_board 오류발생: {str:(ex)}')


    @staticmethod
    def get_notification_by_id(db, notino):
        try:
            return db.query(Notification).filter_by(notino=notino).first()
        except SQLAlchemyError as e:
            print(f'▷▷▷select_board 오류발생: {str:(ex)}')
            return None


    @staticmethod
    def delete_notification(db: Session, notino: int) -> bool:
        notification = db.query(Notification).filter_by(id=notino).first()
        if notification:
            db.delete(notification)
            db.commit()
            return True
        return False
