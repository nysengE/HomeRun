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

@club_router.get('/', response_class=HTMLResponse)
async def club(req: Request, db: Session = Depends(get_db)):
    try:
        clublist = ClubService.select_club(db)
        sports = ClubService.select_sports(db)
        regions = ClubService.select_regions(db)

        return templates.TemplateResponse('club/club.html',
                                          {'request': req, 'clublist': clublist,
                                           'sports': sports, 'regions': regions})
    except Exception as ex:
        print(f'▷▷▷ /club router 오류 발생 : {str(ex)}')



@club_router.get('/add', response_class=HTMLResponse)
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
            return RedirectResponse('/club', 303)

    except Exception as ex:
        print(f'▷▷▷ addok 오류발생 {str(ex)}')
        raise HTTPException(status_code=500, detail=f"Server error: {str(ex)}")

@club_router.get('/view/{clubno}', response_class=HTMLResponse)
async def view(req: Request, clubno: int, db: Session = Depends(get_db)):
    try:
        club = ClubService.selectone_club(clubno, db)

        return templates.TemplateResponse('club/view.html',
                                          {'request': req, 'club': club, 'clubno': clubno})
    except Exception as ex:
        print(f'▷▷▷ view 오류발생 {str(ex)}')


@club_router.get('/apply/{clubno}/{userid}', response_class=HTMLResponse)
async def apply(req: Request, clubno: int, userid:str, db: Session = Depends(get_db)):
    try:
        if ClubService.insert_apply(clubno, userid, db):
            return RedirectResponse('/club', 303)
    except Exception as ex:
        print(f'▷▷▷ apply 오류발생 {str(ex)}')

@club_router.post('/reply', response_class=HTMLResponse)
async def reply(req: Request, reply: NewReply, db: Session = Depends(get_db)):
    try:
        if ClubService.insert_reply(db, reply):
            return RedirectResponse(f'/club/view/{reply.clubno}',303)
    except Exception as ex:
        print(f'▷▷▷ reply 오류 발생 : {str(ex)}')




