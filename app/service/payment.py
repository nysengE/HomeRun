from datetime import datetime
from sqlalchemy.orm import Session
from app.model.payment import Payments

# class PaymentService:
#     @staticmethod
#     # def insert_reservation( db: Session) -> int:
#     #     try:
#     #          payment = Payments(
#     #
#     #         )
#     #         db.add(payment)
#     #         db.commit()
#     #         db.refresh(payment)  # 예약 ID를 가져오기 위해 refresh 호출
#     #
#     #     except Exception as e:
#     #         db.rollback()
#     #         print(f'예약 추가 중 오류 발생: {e}')
#     #         raise
