from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.utils.enums import CaseType, CaseStatus
from datetime import datetime, timezone

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(CaseType), nullable=False)
    description = Column(String, nullable=False)
    opposite_party_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    opposite_party_email = Column(String, nullable=True)
    opposite_party_name = Column(String, nullable=False)
    opposite_party_phone = Column(String, nullable=False)
    opposite_party_address = Column(String, nullable=False)
    is_pending_in_court = Column(Boolean, default=False)
    court_or_police_name = Column(String, nullable=True)
    case_or_fir_number = Column(String, nullable=True)
    proof_upload = Column(String, nullable=True)  # Path to uploaded proof
    # status = Column(Enum(CaseStatus), default=CaseStatus.REGISTERED)
    witness_list = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # Relationships
    creator_user = relationship("User", back_populates="created_cases", foreign_keys=[user_id])
    opposite_party_user = relationship("User", back_populates="accused_cases", foreign_keys=[opposite_party_user_id])    
    
    
    # case status tracking for each party
    creator_status = Column(Enum(CaseStatus), default=CaseStatus.AWAITING_RESPONSE)
    opposite_party_status = Column(Enum(CaseStatus), default=CaseStatus.REQUESTED)
    
    # once the opposite party status is accepted, 
    # then we can proceed with using creator_status for both