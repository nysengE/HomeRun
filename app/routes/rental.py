from fastapi import APIRouter, Depends, HTTPException, Request, Form, UploadFile, File
from typing import List
from datetime import datetime, time
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.model.regions import Regions
from app.schema.rental import NewRental
from app.service.rental import RentalService, get_rental_data, process_upload

rental_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@rental_router.get('/', response_class=HTMLResponse)
async def rental(req: Request, db: Session = Depends(get_db)):
    try:
        rentals = RentalService.select_rentals(db)
        regions = db.query(Regions).all()  # 지역 정보 가져오기
        # 세션에서 사용자 ID 가져오기
        userid = req.session.get('logined_uid')
        return templates.TemplateResponse('rental/rental.html', {'request': req, 'rentals': rentals, 'regions': regions, 'userid': userid})
    except Exception as ex:
        print(f'▷▷▷ rental 오류 발생 : {str(ex)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

# 렌탈 항목 추가 폼 페이지
@rental_router.get("/add", response_class=HTMLResponse)
async def read_add(request: Request, db: Session = Depends(get_db)):
    try:
        regions = db.query(Regions).all()  # 지역 정보를 데이터베이스에서 가져옴
        # 세션에서 사용자 ID 가져오기
        userid = request.session.get('logined_uid', None)

        if not userid:
            # 세션에 userid가 없는 경우 로그인 페이지로 리디렉트
            return RedirectResponse('/user/login', status_code=303)

        return templates.TemplateResponse("rental/add.html", {"request": request, "regions": regions, "userid": userid})
    except Exception as ex:
        print(f'오류 발생: {str(ex)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")



@rental_router.post("/add", response_class=RedirectResponse)
async def add_rental(
        title: str = Form(...),
        contents: str = Form(...),
        people: int = Form(...),
        price: str = Form(...),  # 문자열로 수신
        address: str = Form(...),
        latitude: float = Form(...),
        longitude: float = Form(...),
        sportsno: int = Form(...),
        sigunguno: int = Form(...),
        availdate: str = Form(...),
        availtime: str = Form(...),
        userid: str = Form(...),  # userid 받기
        files: List[UploadFile] = File([]),
        db: Session = Depends(get_db)
):
    # 쉼표 제거 및 정수로 변환
    try:
        price = int(price.replace(',', ''))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid price format. Please provide a valid integer.")

    # 날짜와 시간 변환
    try:

        availdate = datetime.strptime(availdate, '%Y-%m-%d').date()  # 날짜 변환
        availtime = datetime.strptime(availtime, '%H:%M').time()  # 시간 변환
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date or time format. Please use correct format.")

    # 나머지 코드 진행...
    attachs = await process_upload(files)
    rental_data = {
        "title": title,
        "contents": contents,
        "people": people,
        "price": price,
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
        "sportsno": sportsno,
        "sigunguno": sigunguno,
        "availdate": availdate,
        "availtime": availtime,
        "userid": userid  # 여기서도 userno 대신 userid로 사용
    }


    try:
        RentalService.insert_rental(rental_data, attachs, db)
        return RedirectResponse('/rental/', status_code=303)
    except SQLAlchemyError as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database Error")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@rental_router.get('/details/{spaceno}', response_class=HTMLResponse)
async def detail_rental(req: Request, spaceno: int, db: Session = Depends(get_db)):
    try:
        rent = RentalService.select_one_rental(spaceno, db)
        if not rent:
            raise HTTPException(status_code=404, detail="Rental not found")  # 스페이스 번호에 해당하는 항목이 없을 때

        userid = req.session.get('logined_uid', None)
        userno = req.session.get('logined_userno', None)

        # 템플릿에 userid와 userno를 전달
        return templates.TemplateResponse('rental/details.html', {
            'request': req,
            'rent': rent,
            'userid': userid,
            'userno': userno
        })
    except Exception as ex:
        print(f'▷▷▷ detail_rental 오류 발생 : {str(ex)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
