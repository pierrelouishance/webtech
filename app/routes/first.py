from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError


router = APIRouter(prefix="/first", tags=["First"])

@router.get('/')
def get_first():
    print("alright here we go")
