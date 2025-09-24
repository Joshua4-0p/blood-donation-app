from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import schemas, models, auth
import crud
from database import get_db
from typing import List
from models.ai_model import *


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

@router.post("/assess-eligibility", response_model=EligibilityResult)
async def assess_donor_eligibility(questionnaire: CameroonDonorQuestionnaire):
    """Assess blood donation eligibility for Cameroon context"""
    if not eligibility_agent:
        raise HTTPException(status_code=500, detail="Eligibility agent not initialized")
    
    try:
        result = eligibility_agent.assess_eligibility(questionnaire)
        
    
        today = date.today()
        age = today.year - questionnaire.date_of_birth.year - (
            (today.month, today.day) < (questionnaire.date_of_birth.month, questionnaire.date_of_birth.day)
        )
        logger.info(f"Assessment completed: {result.status} for donor age {age}")
        
        return result
    except Exception as e:
        logger.error(f"Assessment failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Assessment error: {str(e)}")
    


