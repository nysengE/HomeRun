from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

mypage_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')


@mypage_router.get('/userinfo', response_class=HTMLResponse)
async def userinfo(req: Request):
    return templates.TemplateResponse('mypage/user/userinfo.html', {'request': req})

@mypage_router.get('/clubwrite', response_class=HTMLResponse)
async def clubwrite(req: Request):
    return templates.TemplateResponse('mypage/user/clubwrite.html', {'request': req})

@mypage_router.get('/clubapply', response_class=HTMLResponse)
async def clubapply(req: Request):
    return templates.TemplateResponse('mypage/user/clubapply.html', {'request': req})

@mypage_router.get('/rentalapply', response_class=HTMLResponse)
async def rentalapply(req: Request):
    return templates.TemplateResponse('mypage/user/rentalapply.html', {'request': req})