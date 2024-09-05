from sqlalchemy.orm import Session
from app.model.users import Users
from app.model.usermanage import UserManage  # usermanage 모델 임포트
from datetime import datetime
from sqlalchemy import select, func

class UserService:
    @staticmethod
    def get_all_users(db: Session, cpg: int, search: str):
        try:
            # 서브쿼리 작성: usermanage 테이블에서 umno가 가장 높은 레코드를 가져옴
            latest_usermanage_subquery = db.query(
                UserManage.userid,
                func.max(UserManage.umno).label('max_umno')
            ).group_by(UserManage.userid).subquery()

            # 메인 쿼리 작성: User와 UserManage를 조인하고 최신의 UserManage만 가져오도록 함
            query = db.query(Users, UserManage).select_from(Users). \
                outerjoin(
                latest_usermanage_subquery,
                (Users.userid == latest_usermanage_subquery.c.userid)
            ).outerjoin(
                UserManage,
                (UserManage.userid == latest_usermanage_subquery.c.userid) &
                (UserManage.umno == latest_usermanage_subquery.c.max_umno)
            )

            # 검색 조건이 있는 경우 필터 추가
            if search:
                query = query.filter(Users.userid.ilike(f'%{search}%'))

            # 총 사용자 수 계산
            total_count = query.count()

            # 페이지네이션 적용하여 사용자 조회
            results = query.order_by(Users.registdate.desc()) \
                .limit(10).offset((cpg - 1) * 10).all()

            # 결과를 (User, UserManage) 튜플 형태로 반환
            total_pages = (total_count + 9) // 10
            return results, total_pages
        except Exception as e:
            print(f"사용자 목록 조회 오류 발생: {e}")
            return [], 0

    @staticmethod
    def suspend_user(db: Session, userid: str, reason: str, duration: int):
        user = db.query(Users).filter(Users.userid == userid).first()
        if not user:
            raise ValueError("해당 사용자가 존재하지 않습니다.")

        # 사용자 관리 테이블에 정지 사유, 기간 및 등록 시간 추가
        user_manage_entry = UserManage(userid=userid, reason=reason, duration=duration, regdate=datetime.now())
        db.add(user_manage_entry)
        db.commit()

        # 사용자 테이블에 정지 기간 설정
        user.status = duration
        user.suspension = datetime.now()
        db.commit()

    @staticmethod
    def unsuspend_user(db: Session, userid: str):
        user = db.query(Users).filter(Users.userid == userid).first()
        if not user:
            raise ValueError("해당 사용자가 존재하지 않습니다.")

        # 활동 정지 취소
        user.status = None
        user.suspension = None
        db.commit()
        print(f"사용자 {user.userid}의 활동 정지가 취소되었습니다.")

    @staticmethod
    def check_and_release_suspension(db: Session):
        users = db.query(Users).filter(Users.status.in_([7, 30]), Users.suspension.isnot(None)).all()
        current_date = datetime.now()

        for user in users:
            suspension_duration = (current_date - user.suspension).days

            # status에 설정된 기간이 지났는지 확인
            if suspension_duration >= user.status:
                user.status = None
                user.suspension = None
                db.commit()
                print(f"사용자 {user.userid}의 활동 정지가 자동으로 해제되었습니다.")
