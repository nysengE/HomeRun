from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session, session
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.service.userpage import UserpageService

mypage_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')


@mypage_router.get('/userinfo', response_class=HTMLResponse)
async def userinfo(req: Request):
    return templates.TemplateResponse('mypage/user/userinfo.html', {'request': req})

@mypage_router.get('/clubwrite', response_class=HTMLResponse)
async def clubwrite(req: Request, db: Session = Depends(get_db)):
    try:
        # userid = session['userid']
        userid = 'dangdang'
        clublist = UserpageService.select_club(userid, db)

        if clublist is None:
            clublist = []

        clubno = clublist.clubno
        print('clubno: ', clubno)

        return templates.TemplateResponse('mypage/user/clubwrite.html',
                                          {'request': req, 'clublist': clublist})


    except Exception as ex:
        print(f'▷▷▷ mypage clubapply 오류 발생 : {str(ex)}')

# @mypage_router.get('/clubwrite/apply/{clubno}', response_class=HTMLResponse)
# async def clubwrite(req: Request, clubno: int, db: Session = Depends(get_db)):
#     try:
#
#         clublist = UserpageService.select_applylist(clubno, db)
#
#         if clublist is None:
#             clublist = []
#
#         return templates.TemplateResponse('mypage/user/clubwrite.html',
#                                           {'request': req, 'clublist': clublist})
#
#
#     except Exception as ex:
#         print(f'▷▷▷ mypage clubapply 오류 발생 : {str(ex)}')


@mypage_router.get('/clubapply', response_class=HTMLResponse)
async def clubapply(req: Request, db: Session = Depends(get_db)):
    try:
        # userid = session['userid']
        userid = 'dangdang'
        applylist = UserpageService.select_apply(userid, db)

        if applylist is None:
            applylist = []

        return templates.TemplateResponse('mypage/user/clubapply.html',
                                          {'request': req, 'applylist': applylist})


    except Exception as ex:
        print(f'▷▷▷ mypage clubapply 오류 발생 : {str(ex)}')


    return templates.TemplateResponse('mypage/user/clubapply.html', {'request': req})

@mypage_router.get('/rentalapply', response_class=HTMLResponse)
async def rentalapply(req: Request):
    return templates.TemplateResponse('mypage/user/rentalapply.html', {'request': req})