from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from models import  schemas, auth
from database import get_db
from typing import List

router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("/", response_model=schemas.RequestOut)
def create_request(request: schemas.RequestCreate, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    user_id = current["user"].id if current["role"] == "user" else None
    hospital_id = current["hospital"].id if current["role"] == "hospital" and current["hospital"].verified else None
    if not user_id and not hospital_id:
        raise HTTPException(status_code=403, detail="Authorized user or verified hospital required")
    return crud.create_request(db, request, user_id=user_id, hospital_id=hospital_id)

@router.get("/", response_model=List[schemas.RequestOut])
def read_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_requests(db, skip=skip, limit=limit)

@router.get("/{request_id}", response_model=schemas.RequestOut)
def read_request(request_id: int, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_request = crud.get_request(db, request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    if current["role"] == "user" and db_request.user_id != current["user"].id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if current["role"] == "hospital" and db_request.hospital_id != current["hospital"].id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db_request

@router.put("/{request_id}", response_model=schemas.RequestOut)
def update_request(request_id: int, request: schemas.RequestUpdate, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_request = crud.get_request(db, request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    if current["role"] == "user" and db_request.user_id != current["user"].id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if current["role"] == "hospital" and db_request.hospital_id != current["hospital"].id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.update_request(db, request_id, request)

@router.delete("/{request_id}")
def delete_request(request_id: int, current: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_request = crud.get_request(db, request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    if current["role"] == "user" and db_request.user_id != current["user"].id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if current["role"] == "hospital" and db_request.hospital_id != current["hospital"].id:
        raise HTTPException(status_code=403, detail="Not authorized")
    crud.delete_request(db, request_id)
    return {"detail": "Request deleted"}