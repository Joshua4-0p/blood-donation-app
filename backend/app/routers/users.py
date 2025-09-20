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
    



    # Json example for testing   
#     {
#   "date_of_birth": "1990-01-20",
#   "weight": 80.0,
#   "feels_well_today": true,
#   "serious_medical_conditions": false,
#   "taking_medications_or_recent_procedure": false,
#   "malaria_in_past_6_months": false,
#   "blood_exposure_risk": false,
#   "high_risk_behaviors": true,
#   "pregnancy_breastfeeding": null,
#   "recent_travel_high_risk": false,
#   "last_donation_date": null,
#   "alcohol_or_drugs_recent": false,
#   "previous_health_issues": false
# }