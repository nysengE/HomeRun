from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.model.rental import Rental
from app.model.reservation import Reservation
from app.schema.reservation import ReservationCreate
from datetime import datetime

reservation_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@reservation_router.get('/{spaceno}', response_class=HTMLResponse)
async def get_reservation(req: Request, spaceno: int, db: Session = Depends(get_db)):
    try:
        rental = db.query(Rental).filter(Rental.spaceno == spaceno).first()
        if not rental:
            print(f"No rental found for spaceno: {spaceno}")
            raise HTTPException(status_code=404, detail="Rental not found")

        print(f"Fetched rental data: {rental}")
        return templates.TemplateResponse('reservation/reservation.html', {'request': req, 'rent': rental})
    except Exception as ex:
        print(f'Error fetching reservation for spaceno {spaceno}: {str(ex)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")


# 달력 이용가능한 날짜 가져오기
@reservation_router.get('/api/rental/{spaceno}/avail_dates')
async def get_available_dates(spaceno: int, db: Session = Depends(get_db)):
    try:
        rental = db.query(Rental).filter(Rental.spaceno == spaceno).first()
        if not rental:
            raise HTTPException(status_code=404, detail="Rental not found")

        avail_dates = [date.availdate.isoformat() for date in rental.avail_dates]
        return JSONResponse(content=avail_dates)
    except Exception as ex:
        print(f'Error fetching available dates: {str(ex)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

# 결제로 post
@reservation_router.post('/api/reservation', response_model=ReservationCreate)
async def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    try:

        new_reservation = Reservation(
            spaceno=reservation.spaceno,
            resdate=datetime.strptime(reservation.resdate, "%Y-%m-%d"),
            restime=reservation.restime,
            people=reservation.people,
            price=reservation.price,
            resstatus=1  # 예약 상태 기본값
        )
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)
        return {"success": True, "resno": new_reservation.resno}
    except Exception as ex:
        print(f'Error creating reservation: {str(ex)}')
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

