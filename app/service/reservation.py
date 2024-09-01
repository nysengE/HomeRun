from datetime import datetime
from sqlalchemy.orm import Session
from app.model.reservation import Reservation

class ReservationService:
    @staticmethod
    def insert_reservation(spaceno: int, resdate: str, restime: str, db: Session) -> int:
        try:
            reservation = Reservation(
                spaceno=spaceno,
                resdate=datetime.strptime(resdate, '%Y-%m-%d'),
                restime=restime,
                resstatus=1  # 예약 상태 기본값 설정
            )
            db.add(reservation)
            db.commit()
            db.refresh(reservation)  # 예약 ID를 가져오기 위해 refresh 호출
            return reservation.resno
        except Exception as e:
            db.rollback()
            print(f'예약 추가 중 오류 발생: {e}')
            raise
