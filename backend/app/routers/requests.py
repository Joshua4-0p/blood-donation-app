from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from models import  schemas, auth
from database import get_db
from typing import List

router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("/", response_model=schemas.RequestOut)
def create_request(request: schemas.RequestCreate, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass


@router.get("/", response_model=List[schemas.RequestOut])
def read_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pass

@router.get("/{request_id}", response_model=schemas.RequestOut)
def read_request(request_id: int, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass

@router.put("/{request_id}", response_model=schemas.RequestOut)
def update_request(request_id: int, request: schemas.RequestUpdate, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass

@router.delete("/{request_id}")
def delete_request(request_id: int, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass