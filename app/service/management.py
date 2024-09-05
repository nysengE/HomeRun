from sqlalchemy import select, update, delete, func, case, extract
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from datetime import datetime, timedelta
from app.model.club import Club  # Club 모델 임포트
from app.model.rental import Rental
from app.model.sports import Sports
from app.model.users import Users
from app.model.regions import Regions

class ManagementService:
    @staticmethod
    def get_posts(db: Session, cpg: int, search: str):
        try:
            # 검색 조건이 있는 경우 필터 추가
            query = select(Club, Sports.name).join(Sports, Club.sportsno == Sports.sportsno)
            if search:
                query = query.where(Club.title.ilike(f'%{search}%'))

            # 총 게시글 수 계산
            total_count = db.execute(select(func.count()).select_from(query.subquery())).scalar()

            # 페이지네이션 적용하여 게시글 조회
            query = query.order_by(Club.registdate.desc()).limit(10).offset((cpg - 1) * 10)
            results = db.execute(query).all()

            # 결과 매핑
            post_list = [{"clubno": club.clubno, "title": club.title, "contents": club.contents,
                          "registdate": club.registdate, "name": name, "status": club.status,
                          "closed_date": club.closed_date} for club, name in results]

            total_pages = (total_count + 9) // 10
            return post_list, total_pages
        except SQLAlchemyError as ex:
            print(f'▶▶▶ get_posts에서 오류발생 : {str(ex)}')
            db.rollback()
            return [], 0

    @staticmethod
    def get_rentals(db: Session, cpg: int, search: str):
        try:
            # 검색 조건이 있는 경우 필터 추가
            query = select(Rental, Sports.name).join(Sports, Rental.sportsno == Sports.sportsno)
            if search:
                query = query.where(Rental.title.ilike(f'%{search}%'))

            # 총 게시글 수 계산
            total_count = db.execute(select(func.count()).select_from(query.subquery())).scalar()

            # 페이지네이션 적용하여 게시글 조회
            query = query.order_by(Rental.regisdate.desc()).limit(10).offset((cpg - 1) * 10)
            results = db.execute(query).all()

            # 결과 매핑
            rental_list = [{"spaceno": rental.spaceno, "title": rental.title, "contents": rental.contents,
                            "regisdate": rental.regisdate, "name": name, "status": rental.status,
                            "closed_date": rental.closed_date} for rental, name in results]

            total_pages = (total_count + 9) // 10
            return rental_list, total_pages
        except SQLAlchemyError as ex:
            print(f'▶▶▶ get_rentals에서 오류발생 : {str(ex)}')
            db.rollback()
            return [], 0


    @staticmethod
    def update_status(post_id: int, status: str, db: Session, table: str):
        try:
            current_date = datetime.now().date()

            if table == 'club':
                # 클럽 상태 업데이트 로직
                club_to_update = db.query(Club).filter(Club.clubno == post_id).first()
                if club_to_update:
                    club_to_update.status = status
                    club_to_update.closed_date = current_date if status == 'close' else None
                    db.add(club_to_update)  # 변경 내용을 세션에 반영

            elif table == 'rental':
                # 렌탈 상태 업데이트 로직
                rental_to_update = db.query(Rental).filter(Rental.spaceno == post_id).first()
                if rental_to_update:
                    rental_to_update.status = status
                    rental_to_update.closed_date = current_date if status == 'close' else None
                    db.add(rental_to_update)  # 변경 내용을 세션에 반영

            db.commit()
            print("상태가 성공적으로 업데이트되었습니다.")
        except SQLAlchemyError as ex:
            print(f'▷▷▷ update_status에서 SQLAlchemy 오류 발생: {str(ex)}')
            db.rollback()
        except Exception as e:
            print(f'▷▷▷ 일반 오류 발생: {str(e)}')
            db.rollback()

    def delete_old_private_posts(db: Session):
        try:
            # 현재 날짜에서 1년 전 날짜 계산
            one_year_ago = datetime.now().date() - timedelta(days=365)

            # 'closed_date'가 1년 이상 지난 Club 게시글 삭제
            stmt_club = delete(Club).where(Club.status == 'close', Club.closed_date < one_year_ago)
            db.execute(stmt_club)

            # 'closed_date'가 1년 이상 지난 Rental 게시글 삭제
            stmt_rental = delete(Rental).where(Rental.status == 'close', Rental.closed_date < one_year_ago)
            db.execute(stmt_rental)

            db.commit()
        except SQLAlchemyError as ex:
            print(f'▶▶▶ delete_old_private_posts에서 오류발생 : {str(ex)}')
            db.rollback()

    @staticmethod
    def get_statistics(db: Session):
        try:
            current_year = datetime.now().year

            # 조건1: 동호회 카테고리별 게시글 수
            club_count_by_sport = db.query(
                Sports.name,
                func.count(Club.clubno).label('club_count')
            ).join(Club, Sports.sportsno == Club.sportsno).group_by(Sports.name).all()
            club_count_by_sport = [{"name": row[0], "club_count": row[1]} for row in club_count_by_sport]

            # 조건2: 대여 카테고리별 게시글 수
            rental_count_by_sport = db.query(
                Sports.name,
                func.count(Rental.spaceno).label('rental_count')
            ).join(Rental, Sports.sportsno == Rental.sportsno).group_by(Sports.name).all()
            rental_count_by_sport = [{"name": row[0], "rental_count": row[1]} for row in rental_count_by_sport]

            # 조건3: 카테고리별 사용자 연령대 수
            age_group_count_by_sport = db.query(
                Sports.name,
                case(
                    (current_year - func.strftime('%Y', Users.birth) < 20, '10대'),
                    (current_year - func.strftime('%Y', Users.birth) < 30, '20대'),
                    (current_year - func.strftime('%Y', Users.birth) < 40, '30대'),
                    (current_year - func.strftime('%Y', Users.birth) < 50, '40대'),
                    (current_year - func.strftime('%Y', Users.birth) < 60, '50대'),
                    else_='60대 이상'
                ).label('age_group'),
                func.count(Users.userno).label('user_count')
            ).join(Club, Users.userid == Club.userid).join(Sports, Club.sportsno == Sports.sportsno).group_by(Sports.name, 'age_group').all()
            age_group_count_by_sport = [{"name": row[0], "age_group": row[1], "user_count": row[2]} for row in age_group_count_by_sport]

            # 조건4: 지역별 스포츠 종류 수 (Rental 테이블 기준으로 모든 데이터 집계)
            sports_count_by_region = db.query(
                Regions.name,
                Sports.name,
                func.count(Rental.spaceno).label('sport_count')
            ).join(Rental, Regions.sigunguno == Rental.sigunguno).join(Sports, Rental.sportsno == Sports.sportsno).group_by(Regions.name, Sports.name).all()

            # 데이터를 지역별로 그룹화하여 스포츠 종류 수를 딕셔너리 형태로 변환
            sports_by_region = {}
            for row in sports_count_by_region:
                region_name = row[0]
                sport_name = row[1]
                count = row[2]
                if region_name not in sports_by_region:
                    sports_by_region[region_name] = {}
                sports_by_region[region_name][sport_name] = count

            return {
                "club_count_by_sport": club_count_by_sport,
                "rental_count_by_sport": rental_count_by_sport,
                "age_group_count_by_sport": age_group_count_by_sport,
                "sports_count_by_region": sports_by_region
            }

        except Exception as ex:
            print(f'▶▶▶ get_statistics에서 오류 발생: {str(ex)}')
            db.rollback()
            return {}
