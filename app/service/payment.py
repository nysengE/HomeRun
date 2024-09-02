from datetime import datetime
from sqlalchemy.orm import Session
from app.model.payment import Payments

# class PaymentService:
#     @staticmethod
#     # def insert_reservation(spaceno: int, resdate: str, restime: str, db: Session) -> int:
#     #     try:
#     #          payment = Payments(
#     #             spaceno=spaceno,
#     #             resdate=datetime.strptime(resdate, '%Y-%m-%d'),
#     #             restime=restime,
#     #         )
#     #         db.add(payment)
#     #         db.commit()
#     #         db.refresh(payment)  # 예약 ID를 가져오기 위해 refresh 호출
#     #         return payment.resno
#     #     except Exception as e:
#     #         db.rollback()
#     #         print(f'예약 추가 중 오류 발생: {e}')
#     #         raise
