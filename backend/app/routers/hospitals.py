from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from models import schemas, auth
from database import get_db
from typing import List

router = APIRouter(prefix="/hospitals", tags=["hospitals"])

@router.get("/{hospital_id}", response_model=schemas.HospitalOut)
def read_hospital(hospital_id: int, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass

@router.put("/{hospital_id}", response_model=schemas.HospitalOut)
def update_hospital(hospital_id: int, hospital: schemas.HospitalUpdate, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass


@router.patch("/{hospital_id}/verify", response_model=schemas.HospitalOut)
def verify_hospital(hospital_id: int, db: Session = Depends(get_db)):
    pass


@router.get("/{hospital_id}/requests", response_model=List[schemas.RequestOut])
def get_hospital_requests(hospital_id: int, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass

@router.get("/{hospital_id}/donations", response_model=List[schemas.DonationOut])
def get_hospital_donations(hospital_id: int, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pass