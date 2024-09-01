from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from app.dbfactory import get_db
from app.model.rental import Rental
from app.model.reservation import Reservation
from app.schema.reservation import ReservationCreate, ReservationResponse
from datetime import datetime

# API 라우터
reservation_api_router = APIRouter()

@reservation_api_router.get('/rental/{spaceno}/avail_dates')
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

@reservation_api_router.post("/reservation", response_model=ReservationResponse)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    try:
        new_reservation = Reservation(
            spaceno=reservation.spaceno,
            resdate=reservation.resdate,
            resstart=reservation.resstart,
            resend=reservation.resend,
            people=reservation.people,
            price=reservation.price,
        )
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)
        return new_reservation
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))