from pydantic import BaseModel, EmailStr
from app.utils.enums import CaseType, CaseStatus
from typing import Optional, List
from datetime import datetime
from fastapi import Form
from app.utils.enums import CaseType


class CaseBase(BaseModel):
    type: CaseType
    description: str
    opposite_party_name: str
    opposite_party_phone: str
    opposite_party_address: str
    opposite_party_user_id: Optional[int] = None
    opposite_party_email: Optional[EmailStr] = None
    is_pending_in_court: bool = False
    court_or_police_name: Optional[str] = None
    case_or_fir_number: Optional[str] = None
    # witness_list: Optional[str] = None
    creator_user: str

class CaseWitnesses():
    witness_list: Optional[str] = None

class CaseCreate(CaseBase):
    proof_upload: Optional[str] = None
    

# I created this schema because we are using a multipart form
# and because of that fastapi needs us to use form
class CaseForm(CaseCreate):
    @classmethod
    def as_form(
        cls,
        type: CaseType = Form(...),
        description: str = Form(...),
        opposite_party_name: str = Form(...),
        opposite_party_phone: str = Form(...),
        opposite_party_address: str = Form(...),
        opposite_party_user_id: Optional[int] = Form(...),
        opposite_party_email: Optional[EmailStr] = Form(...),
        is_pending_in_court: bool = False,
        court_or_police_name: Optional[str] = Form(...),
        case_or_fir_number: Optional[str] = Form(...),
    ):
        return cls(
            type=type,
            description=description,
            opposite_party_name=opposite_party_name,
            opposite_party_phone=opposite_party_phone,
            opposite_party_address=opposite_party_address,
            opposite_party_user_id=opposite_party_user_id,
            opposite_party_email=opposite_party_email,
            is_pending_in_court=is_pending_in_court,
            court_or_police_name=court_or_police_name,
            case_or_fir_number=case_or_fir_number,
        )

class CaseUpdateStatus(BaseModel):
    status: CaseStatus

class CaseResponse(CaseBase, CaseWitnesses):
    id: int
    user_id: int
    proof_upload: Optional[str] = None
    status: CaseStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class CaseList(BaseModel):
    cases: List[CaseResponse]
        
