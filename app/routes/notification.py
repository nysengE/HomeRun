from typing import List
from fastapi import APIRouter, Request, UploadFile, File
from fastapi.params import Depends, Form
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.schema.notification import NewNotification
from app.service.notification import NotificationService
from app.service.notification import get_notification_data, process_upload

notification_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')


@notification_router.get('/list/{cpg}', response_class=HTMLResponse)
async def list(req: Request, cpg: int, db: Session = Depends(get_db)):
    try:
        notilist = NotificationService.select_notification(cpg, db)
        print(f'DEBUG: notilist = {notilist}')  # 디버깅을 위한 출력

        return templates.TemplateResponse('notification/list.html',
                                          {'request': req, 'notilist': notilist})

    except Exception as ex:
        print(f'▷▷▷ list 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/error.html', status_code=303)


@notification_router.get('/write', response_class=HTMLResponse)
async def write(req: Request):
    return templates.TemplateResponse('notification/write.html', {'request': req})


@notification_router.post('/write', response_class=HTMLResponse)
async def writeok(req: Request, notification: NewNotification = Depends(get_notification_data),
                  files: List[UploadFile] = File(None), db: Session = Depends(get_db)):
    try:
        if files is None:
            files = []  # files가 None일 때 빈 리스트로 초기화

        attachs = await process_upload(files)  # 필요한 인자 전달
        if NotificationService.insert_notification(notification, attachs, db):
            return RedirectResponse('/notification/list/1', 303)
        else:
            # 등록 실패 시 에러 처리
            return RedirectResponse('/include/error.html', 303)

    except Exception as ex:
        print(f'▷▷▷ writeok 오류발생 {str(ex)}')
        return RedirectResponse('/include/error.html', 303)


@notification_router.get('/view/{notino}', response_class=HTMLResponse)
async def view(req: Request, notino: int, db: Session = Depends(get_db)):
    try:
        notification = NotificationService.selectone_notification(notino, db)

        return templates.TemplateResponse('notification/view.html',
                                          {'request': req, 'notification': notification})

    except Exception as ex:
        print(f'▷▷▷ view 오류발생 {str(ex)}')
        return RedirectResponse('/error.html', 303)


@notification_router.get('/edit/{notino}', response_class=HTMLResponse)
async def edit(req: Request, notino: int, db: Session = Depends(get_db)):
    try:
        notification = NotificationService.selectone_notification(notino, db)
        return templates.TemplateResponse('notification/edit.html', {'request': req, 'notification': notification})
    except Exception as ex:
        print(f'▷▷▷ edit 오류발생 {str(ex)}')
        return RedirectResponse('/error.html', 303)


@notification_router.post('/edit/{notino}', response_class=HTMLResponse)
async def edit_post(req: Request, notino: int, title: str = Form(...), contents: str = Form(...),
                    db: Session = Depends(get_db)):
    try:
        notification = NotificationService.selectone_notification(notino, db)
        if notification:
            NotificationService.update_notification(notino, title, contents, db)
            return RedirectResponse(f'/notification/view/{notino}', 303)
        else:
            return RedirectResponse('/error.html', 303)
    except Exception as ex:
        print(f'▷▷▷ edit_post 오류발생 {str(ex)}')
        return RedirectResponse('/error.html', 303)


@notification_router.post('/delete/{notino}', response_class=HTMLResponse)
async def delete(notino: int, db: Session = Depends(get_db)):
    try:
        NotificationService.delete_notification(notino, db)
        return RedirectResponse('/notification/list/1', 303)
    except Exception as ex:
        print(f'▷▷▷ delete 오류발생 {str(ex)}')
        return RedirectResponse('/error.html', 303)