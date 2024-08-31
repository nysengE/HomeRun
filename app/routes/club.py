from math import ceil
from urllib.parse import quote

from fastapi import APIRouter, File, UploadFile
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.schema.club.club import NewClub, NewReply
from app.service.club import get_club_data, process_upload, ClubService

club_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@club_router.get('/{cpg}', response_class=HTMLResponse)
async def club(req: Request, cpg: int, db: Session = Depends(get_db)):
    try:
        # 페이지
        stpgb = int((cpg - 1) / 5) * 5 + 1
        clublist, cnt = ClubService.select_club(db, cpg)
        sports = ClubService.select_sports(db)
        regions = ClubService.select_regions(db)

        # 총 페이지 수
        allpage = ceil(cnt / 8)

        return templates.TemplateResponse('club/club.html',
                                          {'request': req, 'clublist': clublist,
                                           'sports': sports, 'regions': regions,
                                           'cpg': cpg, 'allpage': allpage, 'stpgb': stpgb,
                                           'baseurl': '/club/'})

    except Exception as ex:
        print(f'▷▷▷ /club router 오류 발생 : {str(ex)}')

# 검색 club list
@club_router.get('/{sport}/{region}/{people}/{title}/{cpg}', response_class=HTMLResponse)
async def findclub(req: Request, cpg: int, sport: int = 99, region: int = 99, people: int = 9999,  title: str = '#', db: Session = Depends(get_db)):
    try:
        # 페이지 없을 경우
        if cpg < 1:
            raise HTTPException(status_code=400, detail="Invalid page number")

        # 페이지
        stpgb = int((cpg - 1) / 5) * 5 + 1

        clublist, cnt = ClubService.find_select_club(db, cpg, sport, region, people, title)

        # 데이터가 없을 경우
        if clublist is None:
            clublist = []

        sports = ClubService.select_sports(db)
        regions = ClubService.select_regions(db)

        # 총 페이지 수
        allpage = ceil(cnt / 8)

        # title을 URL 인코딩
        encoded_title = quote(title)

        # baseurl 설정
        baseurl = f'/club/{sport}/{region}/{people}/{encoded_title}/'

        return templates.TemplateResponse('club/club.html',
                                          {'request': req, 'clublist': clublist,
                                           'sports': sports, 'regions': regions,
                                           'cpg': cpg, 'allpage': allpage, 'stpgb': stpgb,
                                           'baseurl': baseurl})

    except Exception as ex:
        print(f'▷▷▷ /club router 오류 발생 : {str(ex)}')



@club_router.get('/club/add', response_class=HTMLResponse)
async def add(req: Request):
    return templates.TemplateResponse('club/add.html', {'request': req})

@club_router.post('/add', response_class=HTMLResponse)
async def addok(req: Request, club: NewClub = Depends(get_club_data),
                files: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # print('hello')
        attachs = await process_upload(files)
        # print(attachs)
        if ClubService.insert_club(club, attachs, db):
            return RedirectResponse('/club/1', 303)

    except Exception as ex:
        print(f'▷▷▷ addok 오류발생 {str(ex)}')
        raise HTTPException(status_code=500, detail=f"Server error: {str(ex)}")

@club_router.get('/view/{clubno}', response_class=HTMLResponse)
async def view(req: Request, clubno: int, db: Session = Depends(get_db)):
    try:
        club = ClubService.selectone_club(clubno, db)
        reply = ClubService.select_reply(clubno, db)

        # 신청목록에서 신청한 아이디 가져오기
        applyuid = ClubService.select_apply_userid(clubno, db)
        print('applyuid: ',applyuid)

        return templates.TemplateResponse('club/view.html',
                                          {'request': req, 'club': club,
                                           'clubno': clubno, 'reply': reply, 'applyuid': applyuid})
    except Exception as ex:
        print(f'▷▷▷ view 오류발생 {str(ex)}')


@club_router.get('/apply/{clubno}/{userid}', response_class=HTMLResponse)
async def apply(req: Request, clubno: int, userid:str, db: Session = Depends(get_db)):
    try:
        if ClubService.insert_apply(clubno, userid, db):
            return RedirectResponse('/club/1', 303)
    except Exception as ex:
        print(f'▷▷▷ apply 오류발생 {str(ex)}')

@club_router.post('/reply', response_class=HTMLResponse)
async def reply(req: Request, reply: NewReply, db: Session = Depends(get_db)):
    try:
        if ClubService.insert_reply(db, reply):
            return RedirectResponse(f'/club/view/{reply.clubno}',303)
    except Exception as ex:
        print(f'▷▷▷ reply 오류 발생 : {str(ex)}')

@club_router.post('/rreply', response_class=HTMLResponse)
async def reply(req: Request, reply: NewReply, db: Session = Depends(get_db)):
    try:
        if ClubService.insert_rreply(db, reply):
            return RedirectResponse(f'/club/view/{reply.clubno}',303)
    except Exception as ex:
        print(f'▷▷▷ reply 오류 발생 : {str(ex)}')




