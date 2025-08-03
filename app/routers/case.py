import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.case import Case
from app.models.user import User
from app.models.notification import Notification
from app.schemas.case import CaseList, CaseResponse, CaseUpdateStatus, CaseForm
from app.services.case_service import update_case_status
from app.utils.file_upload import save_file
from app.auth.dependencies import get_current_user
from typing import List, Optional
from app.websocket_manager import manager

router = APIRouter()

# create case route
# @router.post("/", response_model=CaseResponse)
# async def create_case(
#     case: CaseCreate,
#     file: UploadFile = File(None),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
#     ):
#     if file:
#         if file.size > 10 * 1024 * 1024:  # 10MB limit
#             raise HTTPException(status_code=400, detail="Invalid file type or size")
#         case.proof_upload = await save_file(file, "proofs")
    
#     db_case = Case(**case.model_dump(), user_id=current_user.id)
#     db.add(db_case)
#     db.commit()
#     db.refresh(db_case)
#     return db_case


@router.post("/", response_model=CaseResponse)
async def create_case(
    case: CaseForm = Depends(CaseForm.as_form),
    proof: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    if proof:
        if proof.size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="Invalid file type or size")
        case.proof_upload = await save_file(proof, "proofs")
    
    if not case.opposite_party_user_id and not case.opposite_party_email:
        print("No opposing party provided")
        raise HTTPException(status_code=400, detail="You must provide either an existing user as an opposing party of an email to invite the party")
    
    if case.is_pending_in_court and (not case.court_or_police_name or not case.case_or_fir_number):
        raise HTTPException(status_code=400, detail="Court or police name and case number is required if case is pending in court")
    db_case = Case(**case.model_dump(), user_id=current_user.id)
    db.add(db_case)
    db.commit()
    db.refresh(db_case)

    if case.opposite_party_user_id:
        message = f"You've been added as the opposite party to a new case by {current_user.name}"
        db_notification = Notification(user_id=case.opposite_party_user_id, message=message)
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        await manager.send_personal_message(
            json.dumps({
                "type": "info",
                "title": "New Case assigned",
                "case_id": db_case.id,
                "message": message,
                "from_user": current_user.name
            }),
            user_id=case.opposite_party_user_id
        )
    elif case.opposite_party_email:
        # send an invitation mail to the user
        print("Send an email to the email service")
        pass
    return db_case


# update case route
@router.patch("/{id}/status", response_model=CaseResponse)
async def update_case(
    id: int, status_update: CaseUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    db_case = db.query(Case).filter(Case.id == id).first()
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")
    if db_case.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this case")
    
    db_case = update_case_status(db, db_case, status_update.status)
    db.commit()
    db.refresh(db_case)
    return db_case

# get all a user's cases
@router.get("/user", response_model=CaseList)
async def get_cases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    db_cases = db.query(Case).filter(Case.user_id == current_user.id).all()
    if not db_cases:
        return {"cases": []}
    return {"cases": db_cases}


# get a specific case
@router.get("/{id}", response_model=CaseResponse)
async def get_case(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    db_case = db.query(Case).filter(Case.id == id).first()
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")    
    return db_case
