from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.schema.management import StatusUpdate
from app.service.management import ManagementService

management_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')


@management_router.get('/club_list', response_class=HTMLResponse)
async def list_posts(req: Request, cpg: int = Query(1), search: str = '', db: Session = Depends(get_db)):
    try:
        post_list, total_pages = ManagementService.get_posts(db, cpg, search)
        return templates.TemplateResponse('management/club_list.html',
                                          {'request': req, 'post_list': post_list, 'cpg': cpg,
                                           'total_pages': total_pages, 'search': search,
                                           'max': max, 'min': min})
    except Exception as ex:
        print(f'▷▷▷ 게시글 목록 조회 오류 발생 : {str(ex)}')
        return templates.TemplateResponse('error.html', {'request': req})

@management_router.get('/rental_list', response_class=HTMLResponse)
async def list_rentals(req: Request, cpg: int = Query(1), search: str = '', db: Session = Depends(get_db)):
    try:
        rental_list, total_pages = ManagementService.get_rentals(db, cpg, search)
        return templates.TemplateResponse('management/rental_list.html', {'request': req, 'rental_list': rental_list, 'cpg': cpg, 'total_pages': total_pages, 'search': search})
    except Exception as ex:
        print(f'▷▷▷ 대여 목록 조회 오류 발생 : {str(ex)}')
        return templates.TemplateResponse('error.html', {'request': req})

@management_router.post('/update_status/{post_id}')
async def update_post_status(post_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    try:
        print(f"수신된 JSON 데이터: {status_update.dict()}")
        ManagementService.update_status(post_id, status_update.status, db, status_update.table)
        return {'message': '상태가 변경되었습니다.'}
    except Exception as ex:
        print(f'▷▷▷ 상태 변경 오류 발생 : {str(ex)}')
        return {'message': '상태 변경에 실패했습니다.'}


@management_router.post('/update_rental_status/{rental_id}')
async def update_rental_status(rental_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    try:
        print(f"수신된 JSON 데이터: {status_update.dict()}")
        ManagementService.update_status(rental_id, status_update.status, db, status_update.table)
        return {'message': '상태가 변경되었습니다.'}
    except Exception as ex:
        print(f'▷▷▷ 상태 변경 오류 발생 : {str(ex)}')
        return {'message': '상태 변경에 실패했습니다.'}


@management_router.get('/statistics', response_class=HTMLResponse)
async def get_statistics(req: Request, db: Session = Depends(get_db)):
    try:
        stats = ManagementService.get_statistics(db)
        return templates.TemplateResponse('management/statistics.html', {'request': req, 'stats': stats})
    except Exception as ex:
        print(f'▷▷▷ 통계 조회 오류 발생 : {str(ex)}')
        return templates.TemplateResponse('error.html', {'request': req})
