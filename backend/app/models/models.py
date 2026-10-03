from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Text, TIMESTAMP, func, JSON, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.event import listens_for
import enum

Base = declarative_base()

class BloodType(enum.Enum):
    A_POSITIVE = 'A+'
    A_NEGATIVE = 'A-'
    B_POSITIVE = 'B+'
    B_NEGATIVE = 'B-'
    AB_POSITIVE = 'AB+'
    AB_NEGATIVE = 'AB-'
    O_POSITIVE = 'O+'
    O_NEGATIVE = 'O-'
    UNKNOWN = 'Unknown'

class Urgency(enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class DonationStatus(enum.Enum):
    AVAILABLE = 'available'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    DEFERRED = 'deferred'

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    age = Column(Integer)
    gender = Column(String(50))
    location = Column(String(255))
    blood_type = Column(Enum(BloodType, values_callable=lambda x: [e.value for e in x], native_enum=False), default=BloodType.UNKNOWN)
    contact_info = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    donations = relationship('Donation', foreign_keys='Donation.user_id', back_populates='user')
    requests = relationship('Request', foreign_keys='Request.user_id', back_populates='user')
    received_donations = relationship('Donation', foreign_keys='Donation.recipient_user_id', back_populates='recipient_user')
    password_resets = relationship('PasswordReset', foreign_keys='PasswordReset.user_id', back_populates='user')

class Hospital(Base):
    __tablename__ = 'hospitals'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    license = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    verified = Column(Boolean, default=False)
    contact_info = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    requests = relationship('Request', foreign_keys='Request.hospital_id', back_populates='hospital')
    donations = relationship('Donation', back_populates='hospital')
    password_resets = relationship('PasswordReset', foreign_keys='PasswordReset.hospital_id', back_populates='hospital')

class Request(Base):
    __tablename__ = 'requests'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    hospital_id = Column(Integer, ForeignKey('hospitals.id', ondelete='CASCADE'))
    blood_type = Column(Enum(BloodType, values_callable=lambda x: [e.value for e in x], native_enum=False), nullable=False)
    quantity = Column(Integer, default=1)
    urgency = Column(Enum(Urgency, values_callable=lambda x: [e.value for e in x], native_enum=False), default=Urgency.MEDIUM)
    location = Column(String(255), nullable=False)
    medical_reason = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    user = relationship('User', back_populates='requests')
    hospital = relationship('Hospital', back_populates='requests')
    fulfilled_donations = relationship('Donation', back_populates='request')

class Donation(Base):
    __tablename__ = 'donations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    hospital_id = Column(Integer, ForeignKey('hospitals.id', ondelete='SET NULL'))
    request_id = Column(Integer, ForeignKey('requests.id', ondelete='SET NULL'))
    recipient_user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    status = Column(Enum(DonationStatus, values_callable=lambda x: [e.value for e in x], native_enum=False), default=DonationStatus.AVAILABLE)
    health_questionnaire = Column(JSON)
    eligibility_reason = Column(Text)
    location = Column(String(255))
    completed_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    user = relationship('User', foreign_keys=[user_id], back_populates='donations')
    hospital = relationship('Hospital', back_populates='donations')
    request = relationship('Request', back_populates='fulfilled_donations')
    recipient_user = relationship('User', foreign_keys=[recipient_user_id], back_populates='received_donations')

class PasswordReset(Base):
    __tablename__ = 'password_resets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    hospital_id = Column(Integer, ForeignKey('hospitals.id', ondelete='CASCADE'))
    token = Column(String(255), nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    user = relationship('User', back_populates='password_resets')
    hospital = relationship('Hospital', back_populates='password_resets')
    __table_args__ = (
        CheckConstraint('user_id IS NOT NULL AND hospital_id IS NULL OR user_id IS NULL AND hospital_id IS NOT NULL', name='chk_reset_owner'),
        {'extend_existing': True}
    )

def update_timestamps(mapper, connection, target):
    target.updated_at = func.current_timestamp()

for model in [User, Hospital, Request, Donation]:
    listens_for(model, 'before_update')(update_timestamps)