from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.model.rental import Rental

# HTML 템플릿 렌더링 라우터
reservation_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@reservation_router.get('/{spaceno}', response_class=HTMLResponse)
async def get_reservation(req: Request, spaceno: int, db: Session = Depends(get_db)):
    try:
        rental = db.query(Rental).filter(Rental.spaceno == spaceno).first()
        if not rental:
            raise HTTPException(status_code=404, detail="Rental not found")
        return templates.TemplateResponse('reservation/reservation.html', {'request': req, 'rent': rental})
    except Exception as ex:
        print(f'Error fetching reservation for spaceno {spaceno}: {str(ex)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

@reservation_router.post('/{spaceno}/confirm', response_class=HTMLResponse)
async def confirm_reservation(
        req: Request,
        spaceno: int,
        date: str = Form(...),
        time: str = Form(...),
        people: int = Form(...),
        db: Session = Depends(get_db)
):
    try:
        rental = db.query(Rental).filter(Rental.spaceno == spaceno).first()
        if not rental:
            raise HTTPException(status_code=404, detail="Rental not found")

        # time 파라미터를 받아서 selectedTimes로 변환
        selected_times = time.split(',') if time else []

        # 예약 정보를 결제 페이지로 전달
        return templates.TemplateResponse('payment/payment.html', {
            'request': req,
            'rent': rental,
            'date': date,
            'time': time,  # 서버에서 수신한 time 문자열 그대로 전달
            'people': people,
            'selectedTimes': selected_times  # 선택한 시간을 리스트로 전달
        })
    except Exception as ex:
        print(f'Error confirming reservation for spaceno {spaceno}: {str(ex)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")





