from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import schemas, models, auth
import crud
from database import get_db
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass


@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserUpdate, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass


@router.get("/{user_id}/donations", response_model=List[schemas.DonationOut])
def get_user_donations(user_id: int, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass


@router.get("/{user_id}/received-donations", response_model=List[schemas.DonationOut])
def get_user_received_donations(user_id: int, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass


@router.get("/{user_id}/requests", response_model=List[schemas.RequestOut])
def get_user_requests(user_id: int, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass