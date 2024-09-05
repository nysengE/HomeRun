from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.model.rental import Rental
from datetime import datetime

from app.service.reservation import process_reservation

# HTML 템플릿 렌더링 라우터
reservation_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@reservation_router.get('/{spaceno}', response_class=HTMLResponse)
async def get_reservation(req: Request, spaceno: int, db: Session = Depends(get_db)):
    try:
        rental = db.query(Rental).filter(Rental.spaceno == spaceno).first()
        if not rental:
            raise HTTPException(status_code=404, detail="Rental not found")

        # 세션에서 사용자 ID와 번호를 가져옵니다.
        userid = req.session.get('logined_uid', None)
        userno = req.session.get('logined_userno', None)

        # 템플릿에 세션 정보와 렌탈 정보 전달
        return templates.TemplateResponse('reservation/reservation.html', {
            'request': req,
            'rent': rental,
            'userid': userid,
        })
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
        context = await process_reservation(req, spaceno, date, time, people, db)
        return templates.TemplateResponse('payment/payment.html', context)
    except Exception as ex:
        print(f'Error confirming reservation for spaceno {spaceno}: {str(ex)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")









# @reservation_router.post('/{spaceno}/confirm', response_class=HTMLResponse)
# async def confirm_reservation(
#         req: Request,
#         spaceno: int,
#         date: str = Form(...),
#         time: str = Form(...),
#         people: int = Form(...),
#         db: Session = Depends(get_db)
# ):
#     try:
#         rental = db.query(Rental).filter(Rental.spaceno == spaceno).first()
#         if not rental:
#             raise HTTPException(status_code=404, detail="Rental not found")
#
#         # 세션에서 사용자 ID와 사용자 번호 가져오기
#         userid = req.session.get('logined_uid', None)
#
#         # time 파라미터를 받아서 selectedTimes로 변환
#         selected_times = time.split(',') if time else []
#
#         # 시/분 형식으로 변환
#         formatted_times = []
#         for t in selected_times:
#             try:
#                 formatted_time = datetime.strptime(t.strip(), "%H:%M:%S").strftime("%H:%M")
#                 formatted_times.append(formatted_time)
#             except ValueError as e:
#                 print(f"Time conversion error: {e}, time: {t}")
#                 raise HTTPException(status_code=400, detail="Invalid time format")
#
#         # 예약 정보를 결제 페이지로 전달
#         return templates.TemplateResponse('payment/payment.html', {
#             'request': req,
#             'rent': rental,
#             'date': date,
#             'time': ', '.join(formatted_times),  # 시/분 형식의 시간 문자열
#             'people': people,
#             'selectedTimes': selected_times,  # 선택한 시간을 리스트로 전달
#             'userid': userid,  # 세션에서 가져온 사용자 ID 전달
#         })
#     except Exception as ex:
#         print(f'Error confirming reservation for spaceno {spaceno}: {str(ex)}')
#         raise HTTPException(status_code=500, detail="Internal Server Error")






