from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from app.dbfactory import get_db
from app.model.rental import Rental

# HTML 템플릿 렌더링 라우터
reservation_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

@reservation_router.get('/{spaceno}', response_class=HTMLResponse)
async def get_reservation(req: Request, spaceno: int, db: Session = Depends(get_db)):
    try:
        rental = db.query(Rental).filter(Rental.spaceno == spaceno).first()
        if not rental:
            raise HTTPException(status_code=404, detail="Rental not found")
        return templates.TemplateResponse('reservation/reservation.html', {'request': req, 'rent': rental})
    except Exception as ex:
        print(f'Error fetching reservation for spaceno {spaceno}: {str(ex)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
