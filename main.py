from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.dbfactory import db_startup, db_shutdown, get_db
from app.model.rental import Rental
from app.routes.club import club_router
from app.routes.management import management_router
from app.routes.mypage import mypage_router
from app.routes.notification import notification_router
from app.routes.payment import payment_router
from app.routes.rental import rental_router
from app.routes.reservation import reservation_router
from app.routes.user import user_router



# Lifespan 관리 함수 정의
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_startup()  # 서버 시작 시 실행될 코드
    yield
    await db_shutdown()  # 서버 종료 시 실행될 코드

# FastAPI 앱 인스턴스 생성 시 lifespan 함수 전달
app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory='views/templates')
app.mount('/static', StaticFiles(directory='views/static'), name='static')
# Static files 설정
app.mount("/cdn/img", StaticFiles(directory="C:/java/nginx-1.26.2/html/cdn/img"), name="cdn")

app.include_router(club_router, prefix='/club')
app.include_router(management_router, prefix='/management')
app.include_router(mypage_router, prefix='/mypage')
app.include_router(notification_router, prefix='/notification')
app.include_router(payment_router, prefix='/payment')
app.include_router(rental_router, prefix='/rental')
app.include_router(reservation_router, prefix='/reservation')
app.include_router(user_router, prefix='/user')


@app.get("/", response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse('index.html', {'request': req})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# 네이버 클라이언트 ID와 Secret
NAVER_CLIENT_ID = "m9pur6frrc"
NAVER_CLIENT_SECRET = "KHVJQZJZeuOLkn3tr3u0mamTjfNVgQZlelhc0tcf"

@app.get("/geocode/{spaceno}")
async def geocode(spaceno: int, db: Session = Depends(get_db)):
    # 데이터베이스에서 해당 공간의 주소 가져오기
    rental = db.query(Rental).filter(Rental.spaceno == spaceno).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")

    # 네이버 지도 API 엔드포인트
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"

    # 요청 헤더 설정
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVER_CLIENT_SECRET,
    }

    # 요청 파라미터 설정
    params = {
        "query": rental.district,  # 등록된 도로명 주소 사용
    }

    # 네이버 지도 API로 비동기 요청
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

    # 응답 상태 확인
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Geocoding failed")

    # 응답 데이터를 JSON 형식으로 반환
    return response.json()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)