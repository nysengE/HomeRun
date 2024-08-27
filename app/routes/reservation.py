from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

reservation_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@reservation_router.get('/', response_class=HTMLResponse)
async def club(req: Request):
    return templates.TemplateResponse('reservation/reservation.html', {'request': req})


