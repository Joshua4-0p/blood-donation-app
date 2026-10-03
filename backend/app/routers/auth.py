from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud
from models import schemas, auth
from database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register/user", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    pass

@router.post("/register/hospital", response_model=schemas.HospitalOut)
def register_hospital(hospital: schemas.HospitalCreate, db: Session = Depends(get_db)):
    pass

@router.post("/login", response_model=schemas.Token)
def login(login: schemas.Login, db: Session = Depends(get_db)):
    pass

@router.post("/forgot-password")
def forgot_password(forgot: schemas.ForgotPassword, db: Session = Depends(get_db)):
    pass

@router.post("/reset-password")
def reset_password(reset: schemas.ResetPassword, db: Session = Depends(get_db)):
    pass