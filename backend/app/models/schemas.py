from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class BloodType(str, Enum):
    A_PLUS = 'A+'
    A_MINUS = 'A-'
    B_PLUS = 'B+'
    B_MINUS = 'B-'
    AB_PLUS = 'AB+'
    AB_MINUS = 'AB-'
    O_PLUS = 'O+'
    O_MINUS = 'O-'
    UNKNOWN = 'Unknown'

class Urgency(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class DonationStatus(str, Enum):
    AVAILABLE = 'available'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    DEFERRED = 'deferred'

class UserBase(BaseModel):
    name: str
    email: str
    age: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    blood_type: BloodType = BloodType.UNKNOWN
    contact_info: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    blood_type: Optional[BloodType] = None
    contact_info: Optional[str] = None

class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class HospitalBase(BaseModel):
    name: str
    location: str
    license: str
    email: str
    contact_info: Optional[str] = None

class HospitalCreate(HospitalBase):
    password: str

class HospitalUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    contact_info: Optional[str] = None

class HospitalOut(HospitalBase):
    id: int
    verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RequestBase(BaseModel):
    blood_type: BloodType
    quantity: int = 1
    urgency: Urgency = Urgency.MEDIUM
    location: str
    medical_reason: Optional[str] = None

class RequestCreate(RequestBase):
    pass

class RequestUpdate(BaseModel):
    blood_type: Optional[BloodType] = None
    quantity: Optional[int] = None
    urgency: Optional[Urgency] = None
    location: Optional[str] = None
    medical_reason: Optional[str] = None

class RequestOut(RequestBase):
    id: int
    user_id: Optional[int] = None
    hospital_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DonationBase(BaseModel):
    location: Optional[str] = None
    health_questionnaire: Dict

class DonationCreate(DonationBase):
    pass

class DonationUpdate(BaseModel):
    status: Optional[DonationStatus] = None
    request_id: Optional[int] = None
    recipient_user_id: Optional[int] = None

class DonationOut(DonationBase):
    id: int
    user_id: int
    hospital_id: Optional[int] = None
    request_id: Optional[int] = None
    recipient_user_id: Optional[int] = None
    status: DonationStatus
    eligibility_reason: Optional[str] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    email: str
    password: str

class ForgotPassword(BaseModel):
    email: str

class ResetPassword(BaseModel):
    token: str
    new_password: str