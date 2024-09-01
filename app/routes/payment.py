import httpx
from fastapi import APIRouter, FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from app.dbfactory import get_db
from app.model.rental import Rental
from app.model.reservation import Reservation

app = FastAPI()

payment_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')


@payment_router.get('/', response_class=HTMLResponse)
async def club(req: Request):
    return templates.TemplateResponse('payment/payment.html', {'request': req})

@payment_router.get('/{resno}', response_class=HTMLResponse)
async def payment(req: Request, resno: int, db: Session = Depends(get_db)):
    try:
        reservation = db.query(Reservation).filter(Reservation.resno == resno).first()
        if not reservation:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Reservation not found")

        rental = db.query(Rental).filter(Rental.spaceno == reservation.spaceno).first()
        if not rental:
            raise HTTPException(status_code=404, detail="Rental not found")

        return templates.TemplateResponse('payment/payment.html', {'request': req, 'rental': rental, 'reservation': reservation})
    except Exception as ex:
        print(f'Error fetching payment data: {str(ex)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")


# 아임포트 API 설정
IMP_REST_API_KEY = "키"
IMP_REST_API_SECRET = "키"
IMP_BASE_URL = "https://api.iamport.kr"

async def get_access_token():
    url = f"{IMP_BASE_URL}/users/getToken"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "imp_key": IMP_REST_API_KEY,
        "imp_secret": IMP_REST_API_SECRET
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        response_data = response.json()
        if response_data["code"] == 0:
            return response_data["response"]["access_token"]
        else:
            raise Exception("아임포트 액세스 토큰 발급 실패")

@app.post("/pay/complete")
async def pay_complete(request: Request):
    data = await request.json()
    imp_uid = data.get("imp_uid")

    # 아임포트 서버에서 결제 정보 조회
    access_token = await get_access_token()
    url = f"{IMP_BASE_URL}/payments/{imp_uid}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response_data = response.json()

    if response_data["code"] == 0:
        # 결제 검증 로직 추가 (예: 데이터베이스와 대조)
        return JSONResponse(content={"message": "결제가 완료되었습니다."})
    else:
        return JSONResponse(content={"message": "결제 검증에 실패했습니다."}, status_code=400)







