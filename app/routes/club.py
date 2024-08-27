from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

club_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@club_router.get('/', response_class=HTMLResponse)
async def club(req: Request):
    return templates.TemplateResponse('club/club.html', {'request': req})

@club_router.get('/add', response_class=HTMLResponse)
async def club(req: Request):
    return templates.TemplateResponse('club/add.html', {'request': req})


