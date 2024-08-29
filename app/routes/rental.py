from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from app.dbfactory import SessionLocal
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.schema.rental import RentalCreate
from app.service.rental import RentalServices

rental_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@rental_router.get('/', response_class=HTMLResponse)
async def rental(req: Request):
    return templates.TemplateResponse('rental/rental.html', {'request': req})

# 렌탈 항목 추가 폼 페이지
@rental_router.get("/add")
async def read_add(request: Request):
    return templates.TemplateResponse("rental/add.html", {"request": request})

# 렌탈 항목 추가 처리
@rental_router.post("/add")
async def add_rental(request: Request, title: str = Form(...), contents: str = Form(...),
                     people: int = Form(...), price: int = Form(...), zipcode: str = Form(...),
                     businessno: int = Form(...), sportsno: int = Form(...), sigunguno: int = Form(...),
                     db: Session = Depends(get_db)
                     ):
    try:
        rental_data = RentalCreate(
            title=title, contents=contents, people=people,
            price=price, zipcode=zipcode, businessno=businessno,
            sportsno=sportsno, sigunguno=sigunguno
        )
        new_rental = RentalServices.create_rental(db, rental_data)
        return RedirectResponse(url="/add", status_code=303)
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}


# 상세 페이지 라우터 추가
@rental_router.get('/details/mj_college', response_class=HTMLResponse)
async def mj_college_detail(req: Request):
    return templates.TemplateResponse('rental/details/mj_college.html', {'request': req})

@rental_router.get('/details/foreign_university', response_class=HTMLResponse)
async def hufs_detail(req: Request):
    return templates.TemplateResponse('rental/details/foreign_university.html', {'request': req})

@rental_router.get('/details/hansung_university', response_class=HTMLResponse)
async def hansung_university_detail(req: Request):
    return templates.TemplateResponse('rental/details/hansung_university.html', {'request': req})

@rental_router.get('/details/urban_basketball', response_class=HTMLResponse)
async def urban_basketball_detail(req: Request):
    return templates.TemplateResponse('rental/details/urban_basketball.html', {'request': req})

