from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

mypage_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@mypage_router.get('/user', response_class=HTMLResponse)
async def user(req: Request):
    return templates.TemplateResponse('mypage/user.html', {'request': req})

@mypage_router.get('/userinfo', response_class=HTMLResponse)
async def userinfo(req: Request):
    return templates.TemplateResponse('mypage/user/userinfo.html', {'request': req})