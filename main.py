from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.routes.club import club_router
from app.routes.management import management_router
from app.routes.mypage import mypage_router
from app.routes.notification import notification_router
from app.routes.payment import payment_router
from app.routes.rental import rental_router
from app.routes.reservation import reservation_router
from app.routes.user import user_router

app = FastAPI()

templates = Jinja2Templates(directory='views/templates')
app.mount('/static', StaticFiles(directory='views/static'), name='static')

app.include_router(club_router, prefix='/club')
app.include_router(management_router, prefix='/management')
app.include_router(mypage_router, prefix='/mypage')
app.include_router(notification_router, prefix='/notification')
app.include_router(payment_router, prefix='/payment')
app.include_router(rental_router, prefix='/rental')
app.include_router(reservation_router, prefix='/reservation')
app.include_router(user_router, prefix='/user')


@app.get("/", response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse('index.html', {'request': req})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)