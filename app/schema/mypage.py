import os
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from app.dbfactory import get_db
from app.schema.mypage.userpage import RequestClubno, ModifyClub, CheckUser, ModifyUser
from app.service.userpage import UserpageService, get_club_data, process_upload, get_user_data

mypage_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')


@mypage_router.get('/userinfo', response_class=HTMLResponse)
async def userinfo(req: Request, db: Session = Depends(get_db)):
    try:
        # userid = session['userid']
        userid = 'dangdang'
        userdata = UserpageService.select_users(userid, db)

        if userdata is None:
            userdata = []

        passwd = userdata[0].passwd
        if passwd is None:
            passwd = ''

        return templates.TemplateResponse('mypage/user/userinfo.html',
                                          {'request': req, 'userdata': userdata, 'passwd': passwd})

    except Exception as ex:
        print(f'▷▷▷ mypage userinfo 오류 발생 : {str(ex)}')


@mypage_router.post('/checkpwd')
async def checkpwd(req: Request, passwd: CheckUser,  db: Session = Depends(get_db)):
    try:

        userid = "dangdang"

        password = UserpageService.select_pwd(userid, db)

        print('password: ', password)

        print('passwd: ', passwd.passwd)

        if password is None:
            return JSONResponse(content={'success': False})

        # 비밀번호 확인
        if passwd.passwd == password:
            return JSONResponse(content={'success': True})
        else:
            return JSONResponse(content={'success': False})


    except Exception as ex:
        print(f'▷▷▷ mypage clubwriteapply 오류 발생 : {str(ex)}')


@mypage_router.get('/clubwrite', response_class=HTMLResponse)
async def clubwrite(req: Request, db: Session = Depends(get_db)):
    try:
        # userid = session['userid']
        userid = 'dangdang'
        clublist = UserpageService.select_club(userid, db)

        if clublist is None:
            clublist = []

        return templates.TemplateResponse('mypage/user/clubwrite.html',
                                          {'request': req, 'clublist': clublist})

    except Exception as ex:
        print(f'▷▷▷ mypage clubapply 오류 발생 : {str(ex)}')

@mypage_router.delete('/clubwrite/{clubno}', response_class=HTMLResponse)
async def clubwrite(req: Request, clubno:int, db: Session = Depends(get_db)):
    try:

        UserpageService.delete_club(clubno, db)

        return JSONResponse(content={"success": True})

    except Exception as ex:
        print(f'▷▷▷ mypage clubapply 오류 발생 : {str(ex)}')


@mypage_router.post('/clubwrite/apply', response_class=HTMLResponse)
async def clubwriteapply(req: Request, NewClubno: RequestClubno,  db: Session = Depends(get_db)):
    try:
        clubno = NewClubno.clubno

        applylist = UserpageService.select_applylist(clubno, db)

        if applylist is None:
            applylist = []

        # applylist의 각 항목을 딕셔너리로 변환
        applylist_data = []
        for apply in applylist:
            # apply는 SQLAlchemy 모델 객체입니다. 이를 딕셔너리로 변환합니다.
            apply_dict = {
                "ano": apply.ano,
                "userid": apply.userid,  # 실제 필드 이름으로 수정
                "regdate": apply.regdate.strftime('%Y-%m-%d %H:%M:%S'),  # 실제 필드 이름으로 수정
                "status": apply.status,  # 실제 필드 이름으로 수정
                # 필요한 다른 필드들 추가
            }
            applylist_data.append(apply_dict)

        print(applylist_data)  # JSON 형식으로 변환된 데이터를 출력

        return JSONResponse(content={"applylist": applylist_data})


    except Exception as ex:
        print(f'▷▷▷ mypage clubwriteapply 오류 발생 : {str(ex)}')

@mypage_router.post('/clubwrite/approve')
async def clubwriteapprove(req: Request, db: Session = Depends(get_db)):
    try:
        data = await req.json()
        ano = data.get('ano')

        approve = UserpageService.update_apply(ano, db)

        if approve:
            return JSONResponse(content={'success': True})
        else:
            return JSONResponse(content={'success': False, 'message': 'Update failed'}, status_code=500)


    except Exception as ex:
        print(f'▷▷▷ mypage clubwriteapply 오류 발생 : {str(ex)}')



@mypage_router.get('/clubapply', response_class=HTMLResponse)
async def clubapply(req: Request, db: Session = Depends(get_db)):
    try:
        # userid = session['userid']
        userid = 'hehe'
        applylist = UserpageService.select_apply(userid, db)

        if applylist is None:
            applylist = []

        return templates.TemplateResponse('mypage/user/clubapply.html',
                                          {'request': req, 'applylist': applylist})


    except Exception as ex:
        print(f'▷▷▷ mypage clubapply 오류 발생 : {str(ex)}')


    return templates.TemplateResponse('mypage/user/clubapply.html', {'request': req})

@mypage_router.get('/clubwrite/modify/{clubno}', response_class=HTMLResponse)
async def clubwrite(req: Request, clubno:int, db: Session = Depends(get_db)):
    try:

        club = UserpageService.selectone_club(clubno, db)
        if club is None:
            club = []

        return templates.TemplateResponse('mypage/user/modifyclub.html',
                                          {'request': req, 'club': club})

    except Exception as ex:
        print(f'▷▷▷ mypage clubapply 오류 발생 : {str(ex)}')

@mypage_router.post("/clubwrite/deletefile")
async def deletefile(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        image_url = data.get('image_url')
        # print('image_url: ',image_url)

        # 서버에서 이미지 삭제 로직
        path = urlparse(image_url).path
        # print('path: ', path)

        filename = Path(path).name

        filepath = Path('C:/Java/nginx-1.26.2/nginx-1.26.2/html/homerun/img')/filename

        print('filepath: ',filepath)

        if filepath.exists():
            os.remove(filepath)
            return JSONResponse(content={'success': True})
        else:
            return JSONResponse(content={'success': False, 'message': '파일이 존재하지 않습니다.'}, status_code=404)

        # os.remove(os.path.join('homerun/img', os.path.basename(path)))
        #
        # return JSONResponse(content={'success': True})
    except Exception as ex:
        print(f'이미지 삭제 오류 발생: {str(ex)}')
        return JSONResponse(content={'success': False}, status_code=500)

@mypage_router.post('/modify', response_class=HTMLResponse)
async def modify(req: Request, modifyclub: ModifyClub = Depends(get_club_data),
                 files: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):

    try:
        attachs = None

        # 파일이 존재할 경우에만 처리
        if files:
            attachs = await process_upload(files)

        if UserpageService.update_club(modifyclub, db, attachs):

            return RedirectResponse('/mypage/clubwrite', 303)

    except Exception as ex:
        print(f'▷▷▷ modify 오류발생 {str(ex)}')
        raise HTTPException(status_code=500, detail=f"Server error: {str(ex)}")

@mypage_router.put('/userinfo', response_class=HTMLResponse)
async def putuserinfo(req: Request, modifyuser: ModifyUser = Depends(get_user_data), db: Session = Depends(get_db)):
    # try:
        # userid = session['userid']
        userid = 'dangdang'

        # 비밀번호가 None이면 업데이트하지 않음
        if modifyuser.passwd is None:
            modifyuser.passwd = ""

        userdata = UserpageService.select_users(userid, db)

        if userdata is None:
            userdata = []

        passwd = userdata[0].passwd

        if UserpageService.update_users(userid, modifyuser, db):
            return templates.TemplateResponse('mypage/user/userinfo.html',
                                              {'request': req, 'userdata': userdata, 'passwd':passwd, 'result': 'success'})

    # except Exception as ex:
    #     print(f'▷▷▷ mypage putuserinfo 오류 발생 : {str(ex)}')

@mypage_router.get('/rentalapply', response_class=HTMLResponse)
async def rentalapply(req: Request):
    return templates.TemplateResponse('mypage/user/rentalapply.html', {'request': req})