import os
import httpx
from fastapi import APIRouter, FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.model.payment import Payment

app = FastAPI()

payment_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

# 아임포트 API 설정
IMP_REST_API_KEY = os.getenv("IMP_REST_API_KEY", "3330350811307223")
IMP_REST_API_SECRET = os.getenv("IMP_REST_API_SECRET", "wlMWRVhEkwkYjY5B1mfBA356GRRSpFTSrULnWFUM5oiUn7DxZt8LfjAUBIEYqtzZqrUQT2EE9S8UawlL")
IMP_BASE_URL = "https://api.iamport.kr"

@payment_router.get('/{spaceno}', response_class=HTMLResponse)
async def club(req: Request):
    return templates.TemplateResponse('payment/payment.html', {'request': req})

# 아임포트 액세스 토큰 가져오기
async def get_access_token():
    url = f"{IMP_BASE_URL}/users/getToken"
    headers = {"Content-Type": "application/json"}
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
            raise HTTPException(status_code=500, detail="액세스 토큰 발급 실패")

@app.post("/pay/complete")
async def pay_complete(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    imp_uid = data.get("imp_uid")
    if not imp_uid:
        raise HTTPException(status_code=400, detail="잘못된 결제 식별자")

    # 프론트엔드에서 전송된 데이터 사용
    payment_info = {
        "amount": data.get("amount", 10000),  # 전송된 금액 또는 기본값
        "custom_data": {
            "date": data.get("date", "2024-09-01"),  # 전송된 예약 날짜 또는 기본값
            "time": data.get("time", "12:00:00"),    # 전송된 예약 시간 또는 기본값
            "people": data.get("people", 2),         # 전송된 인원수 또는 기본값
            "spaceno": data.get("spaceno", 1)        # 전송된 공간 번호 또는 기본값
        }
    }

    from datetime import datetime
    new_payment = Payment(
        paydate=datetime.now().date(),
        totalprice=payment_info["amount"],
        resdate=payment_info["custom_data"]["date"],
        restime=payment_info["custom_data"]["time"],
        resprice=payment_info["amount"],
        respeople=payment_info["custom_data"]["people"],
        spaceno=payment_info["custom_data"]["spaceno"]
    )
    db.add(new_payment)
    db.commit()
    return JSONResponse(content={"message": "결제가 완료되었습니다."})
