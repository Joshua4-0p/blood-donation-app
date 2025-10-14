from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from models import schemas, ai_model, auth
from database import get_db
from typing import List, Optional

router = APIRouter(prefix="/donations", tags=["donations"])


@router.post("/", response_model=schemas.DonationOut)
def create_donation(donation: schemas.DonationCreate, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass



@router.get("/", response_model=List[schemas.DonationOut])
def search_donations(blood_type: Optional[schemas.BloodType] = None, location: Optional[str] = None, skip: int = 0, limit: int = 100, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass



@router.get("/{donation_id}", response_model=schemas.DonationOut)
def read_donation(donation_id: int, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass



@router.patch("/{donation_id}", response_model=schemas.DonationOut)
def update_donation(donation_id: int, update: schemas.DonationUpdate, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass