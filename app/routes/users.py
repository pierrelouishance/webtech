from fastapi import APIRouter, Query, status, Request, Form, Depends
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from app.authentif.login_manager import login_manager
from app.services.users import *
from app.schemas.users import UserSchema
from uuid import uuid4
from fastapi.templating import Jinja2Templates
from werkzeug.security import check_password_hash

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/users")
