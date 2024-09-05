from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.dbfactory import get_db
from app.service.usermanage import UserService
from app.schema.usermanage import SuspendUserRequest, UnsuspendUserRequest  # 수정된 임포트 경로

usermanage_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')


@usermanage_router.get('/list', response_class=HTMLResponse)
async def list_users(req: Request, cpg: int = Query(1), search: str = '', db: Session = Depends(get_db)):
    try:
        user_list, total_pages = UserService.get_all_users(db, cpg, search)
        return templates.TemplateResponse('usermanage/users_list.html', {'request': req, 'user_list': user_list, 'cpg': cpg, 'total_pages': total_pages, 'search': search})
    except Exception as ex:
        print(f'▷▷▷ 사용자 목록 조회 오류 발생 : {str(ex)}')
        return templates.TemplateResponse('error.html', {'request': req})


@usermanage_router.post('/suspend_user')
async def suspend_user(request: SuspendUserRequest, db: Session = Depends(get_db)):
    try:
        UserService.suspend_user(db, request.userid, request.reason, request.duration)
        return {'message': '사용자가 성공적으로 활동 정지되었습니다.'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"오류 발생: {str(e)}")


# 활동 정지 취소 엔드포인트 수정
@usermanage_router.post('/unsuspend_user')
async def unsuspend_user(request: UnsuspendUserRequest, db: Session = Depends(get_db)):
    try:
        UserService.unsuspend_user(db, request.userid)
        return {'message': '사용자의 활동 정지가 취소되었습니다.'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"오류 발생: {str(e)}")


@usermanage_router.post('/release_suspension')
async def release_suspension(db: Session = Depends(get_db)):
    try:
        UserService.check_and_release_suspension(db)
        return {'message': '활동 정지 해제 작업이 완료되었습니다.'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"오류 발생: {str(e)}")
