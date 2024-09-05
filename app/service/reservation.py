from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from datetime import datetime
from app.model.rental import Rental

#  선택해서 결제할려고 하는 정보들  정의한 함수
async def process_reservation(req: Request, spaceno: int, date: str, time: str, people: int, db: Session):
    rental = db.query(Rental).filter(Rental.spaceno == spaceno).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")

    userid = req.session.get('logined_uid', None)

    selected_times = time.split(',') if time else []

    formatted_times = []
    for t in selected_times:
        try:
            formatted_time = datetime.strptime(t.strip(), "%H:%M:%S").strftime("%H:%M")
            formatted_times.append(formatted_time)
        except ValueError as e:
            print(f"Time conversion error: {e}, time: {t}")
            raise HTTPException(status_code=400, detail="Invalid time format")

    return {
        'request': req,
        'rent': rental,
        'date': date,
        'time': ', '.join(formatted_times),
        'people': people,
        'selectedTimes': selected_times,
        'userid': userid
    }
