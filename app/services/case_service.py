from sqlalchemy.orm import Session
from app.models.case import Case
from app.utils.enums import CaseStatus
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_case_status(db: Session, case: Case, new_status: CaseStatus) -> Case:
    # Simulate opposite party response and panel creation
    if new_status == CaseStatus.AWAITING_RESPONSE:
        logger.info(f"Case {case.id} awaiting response from opposite party")
    elif new_status == CaseStatus.PANEL_CREATED:
        logger.info(f"Case {case.id} panel created")
    
    case.status = new_status
    case.updated_at = datetime.now(timezone.utc)
    logger.info(f"Case {case.id} status updated to {new_status}")
    return case