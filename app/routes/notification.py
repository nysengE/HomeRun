from fastapi import APIRouter
from starlette.templating import Jinja2Templates

notification_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')