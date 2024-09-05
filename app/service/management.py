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
            # Sports 테이블에 별칭을 사용하여 중복 참조 문제 해결
            sports_alias_1 = aliased(Sports)
            sports_alias_2 = aliased(Sports)
            sports_alias_3 = aliased(Sports)
            sports_alias_4 = aliased(Sports)

            # regions 테이블에 대한 별칭 설정
            regions_alias = aliased(Regions)  # 'Region' 클래스는 'regions' 테이블을 참조합니다.

            # 카테고리별 게시글 수 조회 (Club과 Sports 조인)
            stmt_posts_count = select(
                sports_alias_1.name.label('name'),
                func.count(Club.clubno).label('count')
            ).join(sports_alias_1, Club.sportsno == sports_alias_1.sportsno).group_by(sports_alias_1.name)
            posts_count = db.execute(stmt_posts_count).fetchall()

            # 현재 연도 계산
            current_year = datetime.now().year

            # 사용자의 나이 계산 (현재 연도에서 출생 연도를 빼기)
            user_age = current_year - extract('year', Users.birth)

            # 카테고리별 연령대 수 조회 (Club, User, Sports 조인)
            stmt_age_group = select(
                sports_alias_2.name.label('name'),
                func.sum(case(
                    (user_age.between(10, 19), 1),
                    else_=0
                )).label('10대'),
                func.sum(case(
                    (user_age.between(20, 29), 1),
                    else_=0
                )).label('20대'),
                func.sum(case(
                    (user_age.between(30, 39), 1),
                    else_=0
                )).label('30대'),
                func.sum(case(
                    (user_age.between(40, 49), 1),
                    else_=0
                )).label('40대'),
                func.sum(case(
                    (user_age >= 50, 1),
                    else_=0
                )).label('50대 이상')
            ).join(Club, Club.userid == Users.userno).join(sports_alias_2, Club.sportsno == sports_alias_2.sportsno).group_by(sports_alias_2.name)
            age_group_count = db.execute(stmt_age_group).fetchall()

            # 운동 이름별 Rental 게시글 수 조회 (Rental과 Sports 조인)
            stmt_rental_count_by_sport = select(
                sports_alias_3.name.label('name'),
                func.count(Rental.spaceno).label('count')
            ).join(sports_alias_3, Rental.sportsno == sports_alias_3.sportsno).group_by(sports_alias_3.name)
            rental_count_by_sport = db.execute(stmt_rental_count_by_sport).fetchall()

            # 지역별 운동 이름 수 조회 (regions, Rental, Sports 조인)
            stmt_sport_count_by_region = select(
                regions_alias.name.label('region_name'),
                sports_alias_4.name.label('name'),
                func.count(Rental.spaceno).label('count')
            ).join(Rental, Rental.sigunguno == regions_alias.sigunguno).join(sports_alias_4, Rental.sportsno == sports_alias_4.sportsno).group_by(regions_alias.name, sports_alias_4.name)

            sport_count_by_region = db.execute(stmt_sport_count_by_region).fetchall()

            # 결과를 딕셔너리로 변환하여 반환
            stats = {
                'posts_count': [{'name': row.name, 'count': row.count} for row in posts_count],
                'age_group_count': [
                    {'name': row.name, '10대': row[1], '20대': row[2], '30대': row[3], '40대': row[4], '50대 이상': row[5]}
                    for row in age_group_count
                ],
                'rental_count_by_sport': [{'name': row.name, 'count': row.count} for row in rental_count_by_sport],
                'sport_count_by_region': []
            }

            # 지역별 운동 이름 수를 딕셔너리 형태로 변환하여 추가
            region_dict = {}
            for row in sport_count_by_region:
                region_name = row.region_name
                sport_name = row.name
                count = row.count

                if region_name not in region_dict:
                    region_dict[region_name] = {'region_name': region_name, 'sports': []}

                region_dict[region_name]['sports'].append({'name': sport_name, 'count': count})

            # 딕셔너리 값을 리스트로 변환하여 stats에 추가
            stats['sport_count_by_region'] = list(region_dict.values())

            return stats

        except SQLAlchemyError as ex:
            print(f'▶▶▶ get_statistics에서 오류 발생 : {str(ex)}')
            db.rollback()
            return {}
