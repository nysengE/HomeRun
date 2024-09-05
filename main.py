import os
from contextlib import asynccontextmanager
from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Depends, Query, Form, UploadFile, File
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

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
from app.routes.usermanage import usermanage_router
from app.service.management import ManagementService
from app.service.usermanage import UserService
from app.service.rental import RentalService, process_upload
from app.utils import format_time


scheduler = AsyncIOScheduler()

async def release_suspension_task():
    # 데이터베이스 세션을 사용하여 작업 실행
    db = next(get_db())
    UserService.check_and_release_suspension(db)

async def delete_old_private_posts_task():
    # 데이터베이스 세션을 사용하여 작업 실행
    db = next(get_db())
    ManagementService.delete_old_private_posts(db)


# Lifespan 관리 함수 정의
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_startup()  # 서버 시작 시 실행될 코드
    yield
    await db_shutdown()  # 서버 종료 시 실행될 코드

# FastAPI 앱 인스턴스 생성 시 lifespan 함수 전달
app = FastAPI(lifespan=lifespan)

SECRET_KEY = "20240822110005"
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


templates = Jinja2Templates(directory='views/templates')
app.mount('/static', StaticFiles(directory='views/static'), name='static')
# Static files 설정
app.mount("/cdn/img", StaticFiles(directory="C:/java/nginx-1.26.2/html/homerun/img"), name="cdn")


app.include_router(club_router, prefix='/club')
app.include_router(management_router, prefix='/management')
app.include_router(mypage_router, prefix='/mypage')
app.include_router(notification_router, prefix='/notification')
app.include_router(payment_router, prefix='/payment')
app.include_router(rental_router, prefix='/rental')
app.include_router(reservation_router, prefix="/reservation")
app.include_router(user_router, prefix='/user')
app.include_router(usermanage_router, prefix='/usermanage')


@app.get("/", response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse('index.html', {'request': req})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

templates.env.filters['format_time'] = format_time


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)