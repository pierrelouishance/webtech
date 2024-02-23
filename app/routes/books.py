from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas.schemas import Book
import app.services.services as service


router = APIRouter(prefix="/books", tags=["First"])
 
@router.get('/')
def get_books():
    books=service.get_all_books()
    return JSONResponse(
        content=[book.model_dump() for book in books],
        status_code=200,
    )