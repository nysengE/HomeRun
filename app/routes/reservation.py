from fastapi import APIRouter
from starlette.templating import Jinja2Templates

reservation_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')