from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.case import Case
from app.schemas.case import CaseResponse
from app.utils.enums import CaseType, CaseStatus
from typing import List, Optional

router = APIRouter()

def verify_admin_token(x_api_key: str = Header(...)):
    if x_api_key != "dummy-admin-token":  # Replace with proper auth in production
        raise HTTPException(status_code=401, detail="Invalid admin token")

@router.get("/cases/", response_model=List[CaseResponse])
async def get_cases(
    status: Optional[CaseStatus] = None,
    type: Optional[CaseType] = None,
    db: Session = Depends(get_db),
    _ = Depends(verify_admin_token)
):
    query = db.query(Case)
    if status:
        query = query.filter(Case.status == status)
    if type:
        query = query.filter(Case.type == type)
    return query.all()

@router.get("/cases/stats")
async def get_case_stats(db: Session = Depends(get_db), _ = Depends(verify_admin_token)):
    stats = {
        "active": db.query(Case).filter(Case.status.in_([
            CaseStatus.REGISTERED, CaseStatus.AWAITING_RESPONSE,
            CaseStatus.ACCEPTED, CaseStatus.PANEL_CREATED,
            CaseStatus.MEDIATION_IN_PROGRESS])).count(),
        "resolved": db.query(Case).filter(Case.status == CaseStatus.RESOLVED).count(),
        "unresolved": db.query(Case).filter(Case.status == CaseStatus.UNRESOLVED).count()
    }
    return stats