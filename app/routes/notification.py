from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.service.notification import NotificationService

notification_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')


@notification_router.get('/notification/{cpg}', response_class=HTMLResponse)
async def list(req: Request, cpg: int, db: Session = Depends(get_db)):
    try:
        stpgb = int((cpg - 1) / 10) * 10 + 1
        bdlist = NotificationService.select_board(db, cpg)
        return templates.TemplateResponse('notification/index.html',
                                          {'request': req, 'bdlist': bdlist, 'cpg': cpg, 'stpgb': stpgb})
    except Exception as ex:
        print(f'▷▷▷ joinok 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/notification/error', status_code=303)


@notification_router.get('/notification/register', response_class=HTMLResponse)
async def write_notification(req: Request):
    return templates.TemplateResponse('notification/register_post.html', {'request': req})


@notification_router.get('/notification/edit/{notino}', response_class=HTMLResponse)
async def edit_notification(req: Request, notino: int, db: Session = Depends(get_db)):
    notification = NotificationService.get_notification_by_id(db, notino)
    return templates.TemplateResponse('notification/edit_post.html', {
        'request': req, 'notification': notification
    })


@notification_router.get('/error', response_class=HTMLResponse)
async def error(req: Request):
    return templates.TemplateResponse('notification/error.html', {'request': req})


@notification_router.get('/notification/detail/{notino}', response_class=HTMLResponse)
async def notification_detail(req: Request, notino: int, db: Session = Depends(get_db)):
    try:
        notification = NotificationService.get_notification_by_id(db, notino)  # 공지사항 조회
        if not notification:
            return RedirectResponse(url='/notification/error', status_code=303)  # 공지사항이 없을 경우 오류 페이지로 리다이렉트
        return templates.TemplateResponse('notification/detail.html', {
            'request': req, 'notification': notification
        })
    except Exception as ex:
        print(f'▷▷▷ notification_detail 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/notification/error', status_code=303)


@notification_router.route('/notification/delete/<int:notino>', methods=['POST'])
def delete_notification(notino):
    # 데이터베이스에서 해당 notino에 맞는 게시글 삭제
    db.delete_notification(notino)

    # 삭제 후 공지사항 목록 페이지로 리디렉션
    return redirect('/notification')
