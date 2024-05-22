from fastapi import APIRouter, HTTPException, status, Request, Form, Depends
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from pydantic import ValidationError
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from app.models.users import User
from app.models.notes import Notes
from app.schemas.notes import NoteSchema
from app.schemas.users import UserSchema
from app.services import notes as note
from app.authentif.login_manager import login_manager

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/notes", tags=["Notes"])
