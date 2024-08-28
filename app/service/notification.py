import os
from datetime import datetime

from fastapi import Form
from sqlalchemy import insert, select, distinct, func, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.model.notification import Notification, NotiAttach
from app.schema.notification import NewNotification

UPLOAD_PATH = 'C:/Java/nginx-1.26.2/html/prj/img/ntf/'

def get_notification_data(title: str = Form(...), userid: str = Form(...),
                          contents: str = Form(...)):
    return NewNotification(userid=userid, title=title,
                           contents=contents)

async def process_upload(files):
    attachs = []  # 업로드된 파일 정보를 저장하기 위한 리스트
    today = datetime.today().strftime('%Y%m%d%H%M%S')  # UUID 생성

    if files is None:
        return attachs  # files가 None인 경우 빈 리스트 반환

    for file in files:
        if file.filename != '' and file.size > 0:
            nfname = f'{today}{file.filename}'
            fname = os.path.join(UPLOAD_PATH, nfname)  # 업로드할 파일 경로 생성
            content = await file.read()  # 업로드할 파일의 내용을 비동기로 읽음
            with open(fname, 'wb') as f:
                f.write(content)
            attach = [nfname, file.size]  # 업로드된 파일 정보를 리스트에 저장
            attachs.append(attach)

    return attachs


class NotificationService:
    @staticmethod
    def insert_notification(noti, attachs, db):
        try:
            stmt = insert(Notification).values(userid=noti.userid,
                                               title=noti.title, contents=noti.contents)
            result = db.execute(stmt)

            inserted_notino = result.inserted_primary_key[0]
            for attach in attachs:
                data = {'fname': attach[0], 'fsize': attach[1],
                        'notino': inserted_notino}
                stmt = insert(NotiAttach).values(data)
                result = db.execute(stmt)

            db.commit()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_notification에서 오류발생 : {str(ex)} ')
            db.rollback()


    @staticmethod
    def select_notification(cpg, db):
        try:
            stmt = select(Notification.notino, Notification.title, Notification.userid,
                          Notification.regdate, func.first_value(NotiAttach.fname)
                          .over(partition_by=Notification.notino).label('fname')) \
                .outerjoin(NotiAttach, Notification.notino == NotiAttach.notino) \
                .order_by(Notification.notino.desc()).limit(10).offset((cpg - 1) * 10)
            result = db.execute(stmt).fetchall()  # fetchall()로 모든 결과를 가져옵니다.

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_notification에서 오류발생 : {str(ex)} ')
            db.rollback()
            return []



    @staticmethod
    def selectone_notification(notino, db):

        try:
            stmt = select(Notification).where(Notification.notino == notino)
            result = db.execute(stmt).scalars().first()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ selectone_notification에서 오류발생 : {str(ex)} ')
            db.rollback()


    @staticmethod
    def update_notification(notino, title, contents, db):
        try:
            stmt = update(Notification).where(Notification.notino == notino) \
                .values(title=title, contents=contents, last_modified=datetime.now())
            db.execute(stmt)
            db.commit()
        except SQLAlchemyError as ex:
            print(f'▶▶▶ update_notification에서 오류발생 : {str(ex)} ')
            db.rollback()


    @staticmethod
    def delete_notification(notino, db):
        try:
            stmt = delete(Notification).where(Notification.notino == notino)
            db.execute(stmt)
            db.commit()
        except SQLAlchemyError as ex:
            print(f'▶▶▶ delete_notification에서 오류발생 : {str(ex)} ')
            db.rollback()