## AI-blood-eligebilty-Checker/issue-6
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, date, timedelta
import json
import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
import logging
from langchain_core.pydantic_v1 import BaseModel as LangChainBaseModel, Field as LangChainField
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Cameroon Blood Donation Eligibility System", version="1.0.0")

# Enums for better type safety
class EligibilityStatus(str, Enum):
    ELIGIBLE = "eligible"
    TEMPORARILY_DEFERRED = "temporarily_deferred" 
    PERMANENTLY_DEFERRED = "permanently_deferred"
    REQUIRES_MEDICAL_CLEARANCE = "requires_medical_clearance"

class DeferralPeriod(str, Enum):
    ONE_DAY = "1_day"
    THREE_DAYS = "3_days" 
    ONE_WEEK = "1_week"
    FOUR_WEEKS = "4_weeks"
    THREE_MONTHS = "3_months"
    SIX_MONTHS = "6_months"
    ONE_YEAR = "1_year"
    PERMANENT = "permanent"

# Streamlined questionnaire with 12 essential questions for Cameroon context
class CameroonDonorQuestionnaire(BaseModel):
    # Question 1: Basic eligibility - Age and weight
    date_of_birth: date = Field(..., description="Date of birth (must be 18-60 years old)")
    weight: float = Field(..., ge=50.0, description="Weight in kg (minimum 50kg)")
    
    # Question 2: Current health status
    feels_well_today: bool = Field(..., description="Are you feeling well and healthy today?")
    
    # Question 3: Major medical conditions (Cameroon priority diseases)
    serious_medical_conditions: bool = Field(..., description="Do you have or have you ever had: HIV/AIDS, Hepatitis B/C, Tuberculosis, Sickle Cell Disease, Heart Disease, Cancer, Kidney Disease, or Diabetes requiring insulin?")
    
    # Question 4: Current medications and recent medical procedures
    taking_medications_or_recent_procedure: bool = Field(..., description="Are you currently taking any medications (antibiotics, blood thinners, antimalarials) OR have you had surgery, dental work, or vaccination in the past 4 weeks?")
    
    # Question 5: Malaria - Critical for Cameroon
    malaria_in_past_6_months: bool = Field(..., description="Have you had malaria or taken malaria treatment in the past 6 months?")
    
    # Question 6: Blood-related exposure risks
    blood_exposure_risk: bool = Field(..., description="In the past 6 months, have you: received a blood transfusion, shared needles, had a tattoo/piercing from unlicensed facility, or been exposed to someone else's blood?")
    
    # Question 7: High-risk behaviors (contextual for Cameroon)
    high_risk_behaviors: bool = Field(..., description="Have you ever: used injectable drugs not prescribed by a doctor, been paid for sex, or had multiple sexual partners with unprotected sex in the past 3 months?")
    
    # Question 8: Pregnancy and breastfeeding (for applicable donors)
    pregnancy_breastfeeding: Optional[bool] = Field(None, description="Are you currently pregnant, have you given birth in the past 6 months, or are you breastfeeding?")
    
    # Question 9: Recent travel (focus on high-risk areas)
    recent_travel_high_risk: bool = Field(..., description="In the past year, have you traveled to or lived in areas with Ebola outbreaks, or countries with different disease patterns than Cameroon?")
    
    # Question 10: Previous blood donation
    last_donation_date: Optional[date] = Field(None, description="When did you last donate blood? (Leave blank if never donated)")
    
    # Question 11: Alcohol and substance use
    alcohol_or_drugs_recent: bool = Field(..., description="Have you consumed alcohol in the past 24 hours or used any recreational drugs in the past week?")
    
    # Question 12: Previous deferral or health issues
    previous_health_issues: bool = Field(..., description="Have you ever been told not to donate blood, or do you have any other health conditions not mentioned above?")

class EligibilityResult(BaseModel):
    status: EligibilityStatus
    deferral_period: Optional[DeferralPeriod] = None
    reasons: List[str] = Field(default=[], description="Reasons for decision")
    recommendations: List[str] = Field(default=[], description="Recommendations in English and French")
    next_eligible_date: Optional[date] = None
    requires_medical_clearance: bool = False
    additional_notes: Optional[str] = None

# Cameroon-specific guidelines considering local health priorities
CAMEROON_GUIDELINES = {
    "permanent_deferrals": {
        "conditions": [
            "hiv/aids", "hepatitis b", "hepatitis c", "tuberculosis_active", 
            "sickle_cell_disease", "heart_disease", "cancer", "kidney_disease",
            "insulin_dependent_diabetes", "bleeding_disorders"
        ],
        "behaviors": [
            "intravenous_drug_use", "paid_sex", "needle_sharing"
        ]
    },
    "temporary_deferrals": {
        "malaria_treatment": {"months": 6, "reason": "Malaria endemic area - ensure complete recovery"},
        "blood_exposure": {"months": 6, "reason": "Risk of bloodborne infections"},
        "high_risk_sexual": {"months": 3, "reason": "HIV transmission risk period"},
        "pregnancy_delivery": {"months": 6, "reason": "Maternal health and iron recovery"},
        "medications_procedures": {"weeks": 4, "reason": "Drug clearance and healing"},
        "alcohol_drugs": {"days": 7, "reason": "Impaired judgment and health effects"},
        "travel_risk": {"months": 3, "reason": "Exposure to different pathogens"},
        "previous_donation": {"days": 84, "reason": "12-week interval for whole blood in tropical climate"}
    },
    "minimum_requirements": {
        "age_min": 18,  # Cameroon legal age
        "age_max": 60,  # Conservative for tropical climate
        "weight_min": 50,
        "donation_interval_days": 84  # 12 weeks for Cameroon climate
    },
    "high_risk_travel_areas": [
        "guinea", "sierra_leone", "liberia", "drc", "uganda", "sudan"  
    ]
}

# Define output schema for LLM
class LLMOutputSchema(LangChainBaseModel):
    status: EligibilityStatus
    deferral_period: Optional[DeferralPeriod] = None
    reasons: List[str] = LangChainField(..., description="Specific reasons for the decision")
    recommendations: List[str] = LangChainField(..., description="Recommendations in English and French where appropriate")
    requires_medical_clearance: bool = LangChainField(False, description="Whether medical clearance is required")
    additional_notes: Optional[str] = None

class CameroonBloodDonationAgent:
    def __init__(self, model: str = "groq/llama3-70b-8192"):
        self.llm = ChatGroq(
            model=model,
            api_key=os.environ.get('grok-api'),
            temperature=0.1,
            max_tokens=2048
        )
        
        self.output_parser = JsonOutputParser(pydantic_object=LLMOutputSchema)
        self.prompt_template = PromptTemplate(
            template="""
            You are a blood donation eligibility expert for Cameroon's healthcare system, following WHO guidelines adapted for sub-Saharan Africa's disease patterns and climate considerations.
            
            CONTEXT: Cameroon is a malaria-endemic country in Central Africa with high prevalence of hepatitis B, HIV, and sickle cell disease. The tropical climate affects donation intervals and health considerations.
            
            Based on the donor data, provide a structured JSON assessment:
            {format_instructions}
            
            DONOR DATA:
            {donor_data}
            
            CRITICAL CAMEROON-SPECIFIC CONSIDERATIONS:
            1. **Malaria**: Any recent malaria = 6-month deferral (endemic area, ensure complete recovery)
            2. **Hepatitis B**: Very high prevalence - permanent deferral if positive
            3. **Sickle Cell**: Common genetic condition - permanent deferral if disease (not trait)
            4. **Climate**: 12-week donation interval (vs 8 weeks) due to tropical climate recovery needs
            5. **Age Range**: 18-60 years (conservative for climate and healthcare infrastructure)
            6. **Travel**: Defer for Ebola-risk areas, conflict zones
            7. **Medical Clearance**: When uncertain, default to medical review for safety
            
            DECISION LOGIC:
            - **Permanent**: HIV/AIDS, Hepatitis B/C, active TB, sickle cell disease, cancer, heart disease, IV drugs, paid sex
            - **6 Months**: Malaria treatment, pregnancy/delivery, blood exposure, major surgery
            - **3 Months**: High-risk sexual behavior, risky travel, tattoo/piercing unlicensed
            - **4 Weeks**: Medications, vaccinations, dental work, minor procedures  
            - **1 Week**: Alcohol/drug use, feeling unwell
            - **Medical Review**: Complex medical history, unclear responses, multiple conditions
            
            Provide recommendations in English with key phrases in French where helpful for Cameroonian context.
            Return ONLY the JSON object.
            """,
            input_variables=["donor_data"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()},
        )
        
        self.chain = self.prompt_template | self.llm | self.output_parser

    def assess_eligibility(self, questionnaire: CameroonDonorQuestionnaire) -> EligibilityResult:
        """Main eligibility assessment method"""
        try:
            # Calculate age
            today = date.today()
            age = today.year - questionnaire.date_of_birth.year - (
                (today.month, today.day) < (questionnaire.date_of_birth.month, questionnaire.date_of_birth.day)
            )
            
            # Rule-based screening for clear cases
            rule_result = self._rule_based_screening(questionnaire, age)
            if rule_result:
                return rule_result
            
            # AI assessment for complex cases
            ai_result = self._ai_assessment(questionnaire, age)
            return ai_result
            
        except Exception as e:
            logger.error(f"Assessment error: {str(e)}")
            return EligibilityResult(
                status=EligibilityStatus.REQUIRES_MEDICAL_CLEARANCE,
                reasons=[f"System error during assessment: {str(e)}"],
                recommendations=["Please consult medical staff for manual assessment"],
                requires_medical_clearance=True
            )

    def _rule_based_screening(self, questionnaire: CameroonDonorQuestionnaire, age: int) -> Optional[EligibilityResult]:
        """Clear-cut rule-based decisions for obvious cases"""
        
        # Age requirements
        if age < CAMEROON_GUIDELINES['minimum_requirements']['age_min']:
            return EligibilityResult(
                status=EligibilityStatus.PERMANENTLY_DEFERRED,
                deferral_period=DeferralPeriod.PERMANENT,
                reasons=[f"Age below minimum: {age} years (minimum 18)"],
                recommendations=["Vous devez avoir au moins 18 ans pour donner le sang / You must be at least 18 to donate blood"]
            )
        
        if age > CAMEROON_GUIDELINES['minimum_requirements']['age_max']:
            return EligibilityResult(
                status=EligibilityStatus.PERMANENTLY_DEFERRED, 
                deferral_period=DeferralPeriod.PERMANENT,
                reasons=[f"Age above maximum: {age} years (maximum 60)"],
                recommendations=["Age limit exceeded for safety in tropical climate"]
            )
        
        # Weight requirement
        if questionnaire.weight < CAMEROON_GUIDELINES['minimum_requirements']['weight_min']:
            return EligibilityResult(
                status=EligibilityStatus.PERMANENTLY_DEFERRED,
                deferral_period=DeferralPeriod.PERMANENT,
                reasons=[f"Weight below minimum: {questionnaire.weight}kg (minimum 50kg)"],
                recommendations=["Gain weight safely to at least 50kg before attempting donation"]
            )
        
        # Not feeling well
        if not questionnaire.feels_well_today:
            return EligibilityResult(
                status=EligibilityStatus.TEMPORARILY_DEFERRED,
                deferral_period=DeferralPeriod.ONE_WEEK,
                reasons=["Not feeling well today"],
                recommendations=["Rest and return when completely healthy / Reposez-vous et revenez quand vous êtes complètement en bonne santé"],
                next_eligible_date=date.today() + timedelta(days=7)
            )
        
        # Major medical conditions - permanent deferral
        if questionnaire.serious_medical_conditions:
            return EligibilityResult(
                status=EligibilityStatus.PERMANENTLY_DEFERRED,
                deferral_period=DeferralPeriod.PERMANENT,
                reasons=["Serious medical condition (HIV/AIDS, Hepatitis, TB, Sickle Cell Disease, etc.)"],
                recommendations=["Permanent deferral for donor and recipient safety"]
            )
        
        # High-risk behaviors - permanent deferral
        if questionnaire.high_risk_behaviors:
            return EligibilityResult(
                status=EligibilityStatus.PERMANENTLY_DEFERRED,
                deferral_period=DeferralPeriod.PERMANENT,
                reasons=["High-risk behaviors (IV drug use, paid sex, multiple unprotected partners)"],
                recommendations=["Permanent deferral due to high infection risk"]
            )
        
        # Malaria in past 6 months - critical for Cameroon
        if questionnaire.malaria_in_past_6_months:
            return EligibilityResult(
                status=EligibilityStatus.TEMPORARILY_DEFERRED,
                deferral_period=DeferralPeriod.SIX_MONTHS,
                reasons=["Recent malaria or treatment in past 6 months"],
                recommendations=["Wait 6 months after complete recovery from malaria / Attendez 6 mois après guérison complète du paludisme"],
                next_eligible_date=date.today() + timedelta(days=180)
            )
        
        # Blood exposure risks
        if questionnaire.blood_exposure_risk:
            return EligibilityResult(
                status=EligibilityStatus.TEMPORARILY_DEFERRED,
                deferral_period=DeferralPeriod.SIX_MONTHS,
                reasons=["Recent blood exposure risk (transfusion, needles, unlicensed tattoo/piercing)"],
                recommendations=["Wait 6 months to ensure no infection transmission"],
                next_eligible_date=date.today() + timedelta(days=180)
            )
        
        # Pregnancy/breastfeeding
        if questionnaire.pregnancy_breastfeeding:
            return EligibilityResult(
                status=EligibilityStatus.TEMPORARILY_DEFERRED,
                deferral_period=DeferralPeriod.SIX_MONTHS,
                reasons=["Currently pregnant, recent delivery, or breastfeeding"],
                recommendations=["Wait 6 months after delivery or weaning for iron recovery / Attendez 6 mois après accouchement"],
                next_eligible_date=date.today() + timedelta(days=180)
            )
        
        # Recent alcohol/drugs
        if questionnaire.alcohol_or_drugs_recent:
            return EligibilityResult(
                status=EligibilityStatus.TEMPORARILY_DEFERRED,
                deferral_period=DeferralPeriod.ONE_WEEK,
                reasons=["Recent alcohol consumption (24h) or drug use (1 week)"],
                recommendations=["Wait 1 week after last substance use"],
                next_eligible_date=date.today() + timedelta(days=7)
            )
        
        # Previous donation interval check
        if questionnaire.last_donation_date:
            days_since = (date.today() - questionnaire.last_donation_date).days
            required_interval = CAMEROON_GUIDELINES['minimum_requirements']['donation_interval_days']
            
            if days_since < required_interval:
                days_remaining = required_interval - days_since
                return EligibilityResult(
                    status=EligibilityStatus.TEMPORARILY_DEFERRED,
                    deferral_period=DeferralPeriod.THREE_MONTHS,
                    reasons=[f"Too soon since last donation ({days_since} days ago, need {required_interval} days)"],
                    recommendations=[f"Wait {days_remaining} more days before next donation"],
                    next_eligible_date=date.today() + timedelta(days=days_remaining)
                )
        
        return None  # No clear rule-based decision, proceed to AI assessment

    def _ai_assessment(self, questionnaire: CameroonDonorQuestionnaire, age: int) -> EligibilityResult:
        """AI assessment for nuanced cases"""
        try:
            # Prepare data for AI
            data_with_age = questionnaire.dict()
            data_with_age['age'] = age
            donor_data_str = json.dumps(data_with_age, indent=2, default=str)
            
            # Get AI assessment
            ai_output = self.chain.invoke({"donor_data": donor_data_str})
            result = EligibilityResult(**ai_output)
            
            # Calculate next eligible date if deferred
            if result.status == EligibilityStatus.TEMPORARILY_DEFERRED and result.deferral_period:
                days_map = {
                    DeferralPeriod.ONE_DAY: 1,
                    DeferralPeriod.THREE_DAYS: 3,
                    DeferralPeriod.ONE_WEEK: 7,
                    DeferralPeriod.FOUR_WEEKS: 28,
                    DeferralPeriod.THREE_MONTHS: 90,
                    DeferralPeriod.SIX_MONTHS: 180,
                    DeferralPeriod.ONE_YEAR: 365
                }
                if result.deferral_period in days_map:
                    result.next_eligible_date = date.today() + timedelta(days=days_map[result.deferral_period])
            
            return result
        
        except Exception as e:
            logger.error(f"AI assessment failed: {str(e)}")
            return EligibilityResult(
                status=EligibilityStatus.REQUIRES_MEDICAL_CLEARANCE,
                reasons=[f"Complex case requiring medical review: {str(e)}"],
                recommendations=["Please consult medical staff for detailed assessment"],
                requires_medical_clearance=True
            )

# Initialize agent
try:
    eligibility_agent = CameroonBloodDonationAgent()
    logger.info("Cameroon blood donation agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize agent: {e}")
    eligibility_agent = None
