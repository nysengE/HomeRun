from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

rental_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@rental_router.get('/', response_class=HTMLResponse)
async def rental(req: Request):
    return templates.TemplateResponse('rental/rental.html', {'request': req})

# 상세 페이지 라우터 추가
@rental_router.get('/details/mj_college', response_class=HTMLResponse)
async def mj_college_detail(req: Request):
    return templates.TemplateResponse('rental/details/mj_college.html', {'request': req})

@rental_router.get('/details/Foreign_university', response_class=HTMLResponse)
async def hufs_detail(req: Request):
    return templates.TemplateResponse('rental/details/Foreign_university.html', {'request': req})

@rental_router.get('/details/hansung_university', response_class=HTMLResponse)
async def hansung_university_detail(req: Request):
    return templates.TemplateResponse('rental/details/hansung_university.html', {'request': req})

@rental_router.get('/details/urban_basketball', response_class=HTMLResponse)
async def urban_basketball_detail(req: Request):
    return templates.TemplateResponse('rental/details/urban_basketball.html', {'request': req})

