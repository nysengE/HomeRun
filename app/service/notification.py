import os
from datetime import datetime
from fastapi import Form, UploadFile, Request
from sqlalchemy import insert, select, update, delete, func, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List
from app.model.notification import Notification, NotiAttach
from app.schema.notification import NewNotification

UPLOAD_PATH = '/usr/share/nginx/html/cdn/img/'  # 파일 업로드 경로 설정

# 공지사항 데이터 생성 함수
def get_notification_data(req: Request, title: str = Form(...), contents: str = Form(...)):
    # 세션에서 사용자 ID를 가져오고, 기본값은 '운영자'로 설정
    userid = req.session.get('userid', '운영자')
    # 입력받은 제목과 내용을 포함한 새 공지사항 객체를 반환
    return NewNotification(userid=userid, title=title, contents=contents)

# 파일 업로드를 처리하는 비동기 함수
async def process_upload(files: List[UploadFile]) -> List[dict]:
    attachs = []  # 업로드된 파일 정보를 저장하기 위한 리스트
    today = datetime.today().strftime('%Y%m%d%H%M%S')  # 파일명에 사용할 시간 정보 생성

    # 업로드된 파일이 없는 경우 빈 리스트 반환
    if not files:
        return attachs

    # 업로드된 각 파일을 처리
    for file in files:
        if file.filename and file.size > 0:  # 파일이 존재하고 크기가 0보다 큰 경우만 처리
            nfname = f'{today}_{file.filename}'  # 새 파일명 생성
            fname = os.path.join(UPLOAD_PATH, nfname)  # 파일 전체 경로 생성
            try:
                content = await file.read()  # 파일 내용을 비동기적으로 읽기
                with open(fname, 'wb') as f:  # 파일을 바이너리 쓰기 모드로 열기
                    f.write(content)  # 파일 내용을 저장
                attachs.append({'fname': nfname, 'fsize': file.size})  # 파일 정보를 리스트에 추가
                print(f"파일 저장 성공: {fname}")  # 파일 저장 성공 메시지 출력
            except Exception as e:
                print(f'파일 저장 중 오류 발생: {e}')  # 파일 저장 실패 메시지 출력

    return attachs  # 저장된 파일 정보 리스트 반환


class NotificationService:
    @staticmethod
    def select_notification(cpg, search, db):
        """
        공지사항 목록을 가져오는 메서드
        :param cpg: 현재 페이지 번호
        :param search: 검색어 (제목 기준 검색)
        :param db: 데이터베이스 세션
        :return: 공지사항 목록과 총 페이지 수
        """
        try:
            # 공지사항 총 개수 계산 (검색어가 있는 경우 필터 추가)
            if search:
                total_stmt = select(func.count(Notification.notino)).where(Notification.title.ilike(f'%{search}%'))
            else:
                total_stmt = select(func.count(Notification.notino))
            total_count = db.execute(total_stmt).scalar()

            # 페이지당 공지사항 10개 가져오기 (검색어가 있는 경우 필터 추가)
            if search:
                stmt = select(Notification.notino, Notification.title, Notification.userid,
                              Notification.registdate, func.first_value(NotiAttach.fname)
                              .over(partition_by=Notification.notino).label('fname')) \
                    .outerjoin(NotiAttach, Notification.notino == NotiAttach.notino) \
                    .where(Notification.title.ilike(f'%{search}%')) \
                    .order_by(Notification.notino.desc()).limit(10).offset((cpg - 1) * 10)
            else:
                stmt = select(Notification.notino, Notification.title, Notification.userid,
                              Notification.registdate, func.first_value(NotiAttach.fname)
                              .over(partition_by=Notification.notino).label('fname')) \
                    .outerjoin(NotiAttach, Notification.notino == NotiAttach.notino) \
                    .order_by(Notification.notino.desc()).limit(10).offset((cpg - 1) * 10)

            notilist = db.execute(stmt).fetchall()  # 쿼리 실행 결과를 리스트로 저장

            # 총 페이지 수 계산
            total_pages = (total_count + 9) // 10  # 페이지당 10개 공지사항을 보여줌
            return notilist, total_pages
        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_notification에서 오류발생 : {str(ex)} ')
            db.rollback()  # 오류 발생 시 트랜잭션 롤백
            return [], 0

    @staticmethod
    def selectone_notification(notino, db):
        """
        특정 공지사항을 조회하는 메서드
        :param notino: 공지사항 ID
        :param db: 데이터베이스 세션
        :return: 공지사항 객체
        """
        try:
            stmt = select(Notification).where(Notification.notino == notino)  # 특정 공지사항 조회 쿼리 생성
            return db.execute(stmt).scalars().first()  # 첫 번째 결과 반환
        except SQLAlchemyError as ex:
            print(f'▶▶▶ selectone_notification에서 오류발생 : {str(ex)} ')
            db.rollback()  # 오류 발생 시 트랜잭션 롤백

    @staticmethod
    async def update_notification(notino, title, contents, db, attachs=None):
        """
        공지사항을 업데이트하는 메서드
        :param notino: 공지사항 ID
        :param title: 공지사항 제목
        :param contents: 공지사항 내용
        :param db: 데이터베이스 세션
        :param attachs: 첨부파일 리스트
        """
        try:
            # 공지사항 내용 업데이트 쿼리 생성
            stmt = update(Notification).where(Notification.notino == notino) \
                .values(title=title, contents=contents, modifydate=datetime.now())
            db.execute(stmt)  # 쿼리 실행

            # 기존 첨부 파일 삭제 및 새로운 파일 추가
            if attachs:
                # 기존 첨부 파일 조회
                stmt = select(NotiAttach.fname).where(NotiAttach.notino == notino)
                file_list = db.execute(stmt).scalars().all()

                # 파일 삭제 함수 호출
                NotificationService.delete_files(file_list)

                # 기존 첨부 파일 DB 데이터 삭제
                stmt = delete(NotiAttach).where(NotiAttach.notino == notino)
                db.execute(stmt)

                # 새 첨부 파일 저장
                for attach in attachs:
                    data = {'fname': attach['fname'], 'fsize': attach['fsize'], 'notino': notino}
                    stmt = insert(NotiAttach).values(data)
                    db.execute(stmt)

            db.commit()  # 변경 사항 커밋
        except SQLAlchemyError as ex:
            print(f'▶▶▶ update_notification에서 오류발생: {str(ex)}')
            db.rollback()  # 오류 발생 시 트랜잭션 롤백

    @staticmethod
    def insert_notification(noti, attachs, db):
        """
        공지사항을 추가하는 메서드
        :param noti: 새로운 공지사항 객체
        :param attachs: 첨부파일 리스트
        :param db: 데이터베이스 세션
        :return: 성공 여부 (True/False)
        """
        try:
            # 공지사항 데이터 삽입 쿼리 생성
            stmt = insert(Notification).values(userid=noti.userid, title=noti.title, contents=noti.contents)
            result = db.execute(stmt)
            inserted_notino = result.inserted_primary_key[0]  # 새로 삽입된 공지사항 ID 가져오기

            # 첨부파일 정보 삽입
            for attach in attachs:
                data = {'fname': attach['fname'], 'fsize': attach['fsize'], 'notino': inserted_notino}
                stmt = insert(NotiAttach).values(data)
                db.execute(stmt)

            db.commit()  # 트랜잭션 커밋
            return True
        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_notification에서 오류발생: {str(ex)}')
            db.rollback()  # 트랜잭션 롤백
            return False

    @staticmethod
    def delete_files(file_list):
        """
        파일을 삭제하는 메서드
        :param file_list: 삭제할 파일 목록
        """
        for file in file_list:
            try:
                file_path = os.path.join(UPLOAD_PATH, file)  # 파일 경로 생성
                if os.path.exists(file_path):
                    os.remove(file_path)  # 파일 삭제
                    print(f"파일 삭제 성공: {file_path}")
                else:
                    print(f"파일이 존재하지 않습니다: {file_path}")
            except OSError as e:
                print(f"파일 삭제 오류: {e}")

    @staticmethod
    def delete_notification(notino, db):
        """
        공지사항을 삭제하는 메서드
        :param notino: 공지사항 ID
        :param db: 데이터베이스 세션
        """
        try:
            # 첨부파일 조회 후 삭제
            stmt = select(NotiAttach.fname).where(NotiAttach.notino == notino)
            file_list = db.execute(stmt).scalars().all()
            NotificationService.delete_files(file_list)

            # 첨부파일 DB 삭제
            stmt = delete(NotiAttach).where(NotiAttach.notino == notino)
            db.execute(stmt)

            # 공지사항 삭제
            stmt = delete(Notification).where(Notification.notino == notino)
            db.execute(stmt)

            db.commit()  # 트랜잭션 커밋
        except SQLAlchemyError as ex:
            print(f'▶▶▶ delete_notification에서 오류발생: {str(ex)}')
            db.rollback()  # 트랜잭션 롤백

    @staticmethod
    def delete_notiattach(notino, fname, db):
        """
        특정 첨부파일을 삭제하는 메서드
        :param notino: 공지사항 ID
        :param fname: 파일 이름
        :param db: 데이터베이스 세션
        """
        try:
            # 파일 삭제
            NotificationService.delete_files([fname])

            # 첨부파일 DB 삭제
            stmt = delete(NotiAttach).where(and_(NotiAttach.notino == notino, NotiAttach.fname == fname))
            db.execute(stmt)

            db.commit()  # 트랜잭션 커밋
        except SQLAlchemyError as ex:
            print(f'▶▶▶ delete_notiattach에서 오류발생: {str(ex)}')
            db.rollback()  # 트랜잭션 롤백

