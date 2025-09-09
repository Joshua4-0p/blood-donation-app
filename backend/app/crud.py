from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import models, schemas
from datetime import datetime, timedelta
import bcrypt
import uuid
from typing import Optional

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    user_data = user.model_dump(exclude={'password'})
    db_user = models.User(**user_data, password_hash=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        # Use model_dump() and handle enum conversion properly
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == 'blood_type' and value is not None:
                # Convert string back to SQLAlchemy enum
                if isinstance(value, str):
                    # Find the corresponding SQLAlchemy enum member
                    for enum_member in models.BloodType:
                        if enum_member.value == value:
                            value = enum_member
                            break
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def get_user_donation_history(db: Session, user_id: int):
    return db.query(models.Donation).filter(
        and_(models.Donation.user_id == user_id, models.Donation.status == models.DonationStatus.COMPLETED)
    ).order_by(models.Donation.completed_at.desc()).all()

def get_user_received_history(db: Session, user_id: int):
    return db.query(models.Donation).filter(
        models.Donation.recipient_user_id == user_id
    ).order_by(models.Donation.completed_at.desc()).all()

def create_hospital(db: Session, hospital: schemas.HospitalCreate):
    hashed_pw = hash_password(hospital.password)
    hospital_data = hospital.model_dump(exclude={'password'})
    db_hospital = models.Hospital(**hospital_data, password_hash=hashed_pw)
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

def get_hospital(db: Session, hospital_id: int):
    return db.query(models.Hospital).filter(models.Hospital.id == hospital_id).first()

def get_hospital_by_email(db: Session, email: str):
    return db.query(models.Hospital).filter(models.Hospital.email == email).first()

def update_hospital(db: Session, hospital_id: int, hospital_update: schemas.HospitalUpdate):
    db_hospital = get_hospital(db, hospital_id)
    if db_hospital:
        update_data = hospital_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_hospital, key, value)
        db.commit()
        db.refresh(db_hospital)
    return db_hospital

def verify_hospital(db: Session, hospital_id: int):
    db_hospital = get_hospital(db, hospital_id)
    if db_hospital:
        db_hospital.verified = True
        db.commit()
        db.refresh(db_hospital)
    return db_hospital

def get_hospital_requests(db: Session, hospital_id: int):
    return db.query(models.Request).filter(models.Request.hospital_id == hospital_id).all()

def get_hospital_donation_history(db: Session, hospital_id: int):
    return db.query(models.Donation).filter(
        models.Donation.hospital_id == hospital_id
    ).order_by(models.Donation.completed_at.desc()).all()

def create_request(db: Session, request: schemas.RequestCreate, user_id: Optional[int] = None, hospital_id: Optional[int] = None):
    request_data = request.model_dump()
    # Convert blood_type and urgency enums if needed
    if 'blood_type' in request_data and isinstance(request_data['blood_type'], str):
        for enum_member in models.BloodType:
            if enum_member.value == request_data['blood_type']:
                request_data['blood_type'] = enum_member
                break
    if 'urgency' in request_data and isinstance(request_data['urgency'], str):
        for enum_member in models.Urgency:
            if enum_member.value == request_data['urgency']:
                request_data['urgency'] = enum_member
                break
    
    db_request = models.Request(**request_data, user_id=user_id, hospital_id=hospital_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Request).offset(skip).limit(limit).all()

def get_request(db: Session, request_id: int):
    return db.query(models.Request).filter(models.Request.id == request_id).first()

def update_request(db: Session, request_id: int, request_update: schemas.RequestUpdate):
    db_request = get_request(db, request_id)
    if db_request:
        update_data = request_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == 'blood_type' and value is not None and isinstance(value, str):
                for enum_member in models.BloodType:
                    if enum_member.value == value:
                        value = enum_member
                        break
            elif key == 'urgency' and value is not None and isinstance(value, str):
                for enum_member in models.Urgency:
                    if enum_member.value == value:
                        value = enum_member
                        break
            setattr(db_request, key, value)
        db.commit()
        db.refresh(db_request)
    return db_request

def delete_request(db: Session, request_id: int):
    db_request = get_request(db, request_id)
    if db_request:
        db.delete(db_request)
        db.commit()
    return db_request

def get_last_donation_date(db: Session, user_id: int):
    last_donation = db.query(models.Donation).filter(
        and_(models.Donation.user_id == user_id, models.Donation.status == models.DonationStatus.COMPLETED)
    ).order_by(models.Donation.completed_at.desc()).first()
    return last_donation.completed_at if last_donation else None

def create_donation(db: Session, donation: schemas.DonationCreate, user_id: int, eligibility_result: dict):
    donation_data = donation.model_dump()
    db_donation = models.Donation(
        **donation_data,
        user_id=user_id,
        status=models.DonationStatus.AVAILABLE if eligibility_result['eligible'] else models.DonationStatus.DEFERRED,
        eligibility_reason=eligibility_result['reason']
    )
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)
    return db_donation

def search_donations(db: Session, blood_type: Optional[schemas.BloodType] = None, location: Optional[str] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Donation).join(models.User).filter(models.Donation.status == models.DonationStatus.AVAILABLE)
    if blood_type:
        # Convert Pydantic enum to SQLAlchemy enum for filtering
        sqlalchemy_blood_type = None
        if isinstance(blood_type, str):
            blood_type_value = blood_type
        else:
            blood_type_value = blood_type.value
        
        for enum_member in models.BloodType:
            if enum_member.value == blood_type_value:
                sqlalchemy_blood_type = enum_member
                break
        
        if sqlalchemy_blood_type:
            query = query.filter(models.User.blood_type == sqlalchemy_blood_type)
    if location:
        query = query.filter(models.User.location.ilike(f"%{location}%"))
    query = query.order_by(
        models.User.blood_type.desc().nullslast(),
        models.Donation.created_at.desc()
    )
    return query.offset(skip).limit(limit).all()

def get_donation(db: Session, donation_id: int):
    return db.query(models.Donation).filter(models.Donation.id == donation_id).first()

def update_donation(db: Session, donation_id: int, donation_update: schemas.DonationUpdate, hospital_id: Optional[int] = None):
    db_donation = get_donation(db, donation_id)
    if db_donation:
        update_data = donation_update.model_dump(exclude_unset=True)
        if 'status' in update_data and isinstance(update_data['status'], str):
            # Convert status string to SQLAlchemy enum
            for enum_member in models.DonationStatus:
                if enum_member.value == update_data['status']:
                    update_data['status'] = enum_member
                    break
        
        if 'status' in update_data and update_data['status'] == models.DonationStatus.COMPLETED:
            db_donation.completed_at = datetime.utcnow()
            db_donation.hospital_id = hospital_id or db_donation.hospital_id
            
        for key, value in update_data.items():
            setattr(db_donation, key, value)
            
        if db_donation.request_id:
            request = get_request(db, db_donation.request_id)
            if request.user_id:
                db_donation.recipient_user_id = request.user_id
        db.commit()
        db.refresh(db_donation)
    return db_donation

def create_password_reset(db: Session, email: str, entity_type: str):
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=1)
    user_id = None
    hospital_id = None
    if entity_type == "user":
        user = get_user_by_email(db, email)
        if user:
            user_id = user.id
    elif entity_type == "hospital":
        hospital = get_hospital_by_email(db, email)
        if hospital:
            hospital_id = hospital.id
    if not user_id and not hospital_id:
        return None
    db_reset = models.PasswordReset(user_id=user_id, hospital_id=hospital_id, token=token, expires_at=expires_at)
    db.add(db_reset)
    db.commit()
    db.refresh(db_reset)
    return db_reset

def get_password_reset(db: Session, token: str):
    return db.query(models.PasswordReset).filter(models.PasswordReset.token == token).first()

def update_password(db: Session, token: str, new_password: str):
    db_reset = get_password_reset(db, token)
    if not db_reset or db_reset.expires_at < datetime.utcnow():
        return None
    if db_reset.user_id:
        user = get_user(db, db_reset.user_id)
        if user:
            user.password_hash = hash_password(new_password)
            db.commit()
            db.refresh(user)
            db.delete(db_reset)
            db.commit()
            return user
    elif db_reset.hospital_id:
        hospital = get_hospital(db, db_reset.hospital_id)
        if hospital:
            hospital.password_hash = hash_password(new_password)
            db.commit()
            db.refresh(hospital)
            db.delete(db_reset)
            db.commit()
            return hospital
    return None