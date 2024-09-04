from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.model.rental import Rental
import logging

from app.service.reservation import process_reservation

logger = logging.getLogger(__name__)

mypage_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

# POST 메서드
@mypage_router.post('/{spaceno}/confirm', response_class=HTMLResponse)
async def confirm_reservation(
        req: Request,
        spaceno: int,
        date: str = Form(...),
        time: str = Form(...),
        people: int = Form(...),
        db: Session = Depends(get_db)
):
    try:
        context = await process_reservation(req, spaceno, date, time, people, db)
        return templates.TemplateResponse('payment/payment.html', context)
    except Exception as ex:
        logger.error(f'Error confirming reservation for spaceno {spaceno}: {str(ex)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

# GET 메서드
@mypage_router.get('/{spaceno}/check', response_class=HTMLResponse)
async def check_rental(
        req: Request,
        spaceno: int,
        db: Session = Depends(get_db)
):
    try:
        rental = db.query(Rental).filter(Rental.spaceno == spaceno).first()
        if not rental:
            raise HTTPException(status_code=404, detail="Rental not found")

        # 추가 데이터를 가져오는 로직이 필요하다면 여기에 추가하세요.
        context = {
            'request': req,
            'rent': rental,  # rental 객체를 전달
            # 필요한 추가 데이터
        }
        return templates.TemplateResponse('mypage/user/rentalapply.html', context)
    except Exception as ex:
        logger.error(f'Error fetching rental details for spaceno {spaceno}: {str(ex)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
