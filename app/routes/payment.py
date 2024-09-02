import httpx
from fastapi import APIRouter, FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from app.dbfactory import get_db
from app.model.payment import Payment
from app.model.rental import Rental

app = FastAPI()

payment_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')



@payment_router.get('/{spaceno}', response_class=HTMLResponse)
async def club(req: Request):
    return templates.TemplateResponse('payment/payment.html', {'request': req})





# 아임포트 API 설정
IMP_REST_API_KEY = "3330350811307223"
IMP_REST_API_SECRET = "wlMWRVhEkwkYjY5B1mfBA356GRRSpFTSrULnWFUM5oiUn7DxZt8LfjAUBIEYqtzZqrUQT2EE9S8UawlL"
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
async def pay_complete(request: Request, db: Session = Depends(get_db)):
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
        # 결제 성공: 결제 정보 저장
        payment_info = response_data["response"]
        from datetime import datetime
        new_payment = Payment(
            paydate=datetime.now().date(),
            totalprice=payment_info["amount"],
            resdate=payment_info["custom_data"]["date"],
            restime=payment_info["custom_data"]["time"],
            resprice=payment_info["amount"],  # 여기서 가격은 예시입니다.
            respeople=payment_info["custom_data"]["people"],
            spaceno=payment_info["custom_data"]["spaceno"]
        )
        db.add(new_payment)
        db.commit()
        return JSONResponse(content={"message": "결제가 완료되었습니다."})
    else:
        return JSONResponse(content={"message": "결제 검증에 실패했습니다."}, status_code=400)








