from typing import List
from fastapi import APIRouter, Request, UploadFile, File, Depends, Form
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.schema.notification import NewNotification
from app.service.notification import NotificationService, get_notification_data, process_upload

notification_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

# 공지사항 목록 페이지
@notification_router.get('/list/{cpg}', response_class=HTMLResponse)
async def list(req: Request, cpg: int, search: str = '', db: Session = Depends(get_db)):
    try:
        # 공지사항 목록과 총 페이지 수를 조회
        notilist, total_pages = NotificationService.select_notification(cpg, search, db)
        return templates.TemplateResponse('notification/list.html',
                                          {'request': req, 'notilist': notilist, 'cpg': cpg,
                                           'total_pages': total_pages, 'search': search,
                                           'max': max, 'min': min})  # 템플릿에 데이터 전달
    except Exception as ex:
        print(f'▷▷▷ list 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/error.html', status_code=303)

# 공지사항 작성 페이지
@notification_router.get('/write', response_class=HTMLResponse)
async def write(req: Request):
    # 로그인 세션 처리
    # if req.session.get('userid') != 'manager':
    #     return RedirectResponse(url='/error.html', status_code=303)
    # 공지사항 작성 페이지를 반환
    return templates.TemplateResponse('notification/write.html', {'request': req})

# 공지사항 작성 처리
@notification_router.post('/write', response_class=HTMLResponse)
async def writeok(req: Request, notification: NewNotification = Depends(get_notification_data),
                  files: List[UploadFile] = File(None), db: Session = Depends(get_db)):
    try:
        # 업로드된 파일 처리
        attachs = await process_upload(files) if files else []
        if NotificationService.insert_notification(notification, attachs, db):
            return RedirectResponse('/notification/list/1', 303)
        else:
            return RedirectResponse('/include/error.html', 303)
    except Exception as ex:
        print(f'▷▷▷ writeok 오류발생: {str(ex)}')
        return RedirectResponse('/include/error.html', 303)

# 공지사항 보기 페이지
@notification_router.get('/view/{notino}', response_class=HTMLResponse)
async def view(req: Request, notino: int, db: Session = Depends(get_db)):
    try:
        # 공지사항 정보 조회
        notification = NotificationService.selectone_notification(notino, db)
        return templates.TemplateResponse('notification/view.html',
                                          {'request': req, 'notification': notification})
    except Exception as ex:
        print(f'▷▷▷ view 오류발생 {str(ex)}')
        return RedirectResponse('/error.html', 303)

# 공지사항 수정 페이지
@notification_router.get('/edit/{notino}', response_class=HTMLResponse)
async def edit(req: Request, notino: int, db: Session = Depends(get_db)):
    # 로그인 세션 처리
    # if req.session.get('userid') != 'manager':
    #     return RedirectResponse(url='/error.html', status_code=303)
    try:
        # 공지사항 정보 조회
        notification = NotificationService.selectone_notification(notino, db)
        return templates.TemplateResponse('notification/edit.html', {'request': req, 'notification': notification})
    except Exception as ex:
        print(f'▷▷▷ edit 오류발생 {str(ex)}')
        return RedirectResponse('/error.html', 303)

# 공지사항 수정 처리
@notification_router.post('/edit/{notino}', response_class=HTMLResponse)
async def edit_post(req: Request, notino: int, title: str = Form(...), contents: str = Form(...),
                    files: List[UploadFile] = File(None), db: Session = Depends(get_db)):
    try:
        # 공지사항 정보 조회
        notification = NotificationService.selectone_notification(notino, db)
        if notification:
            attachs = await process_upload(files) if files else []  # 업로드된 파일 처리
            await NotificationService.update_notification(notino, title, contents, db, attachs)
            return RedirectResponse(f'/notification/view/{notino}', status_code=303)
        else:
            return RedirectResponse('/error.html', status_code=303)
    except Exception as ex:
        print(f'▷▷▷ edit_post 오류발생: {str(ex)}')
        return RedirectResponse('/error.html', status_code=303)

# 공지사항 삭제 처리
@notification_router.post('/delete/{notino}', response_class=HTMLResponse)
async def delete(notino: int, db: Session = Depends(get_db)):
    try:
        NotificationService.delete_notification(notino, db)
        return RedirectResponse('/notification/list/1', 303)
    except Exception as ex:
        print(f'▷▷▷ delete 오류발생 {str(ex)}')
        return RedirectResponse('/error.html', 303)

# 첨부 이미지 삭제 처리
@notification_router.post('/delete_image/{notino}')
def delete_image(notino: int, fname: str = Form(...), db: Session = Depends(get_db)):
    try:
        NotificationService.delete_notiattach(notino, fname, db)
        return JSONResponse(content={"message": "파일 삭제 성공"}, status_code=200)
    except Exception as ex:
        print(f'▷▷▷ delete_image 오류발생: {str(ex)}')
        return JSONResponse(content={"message": "파일 삭제 실패"}, status_code=500)

