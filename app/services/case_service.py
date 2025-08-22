import json
from sqlalchemy.orm import Session
from app.models.case import Case
from app.models.notification import Notification
from app.utils.enums import CaseStatus
from datetime import datetime, timezone
import logging
from app.websocket_manager import manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_case_status(db: Session, case: Case, new_status: CaseStatus) -> Case:
    # Simulate opposite party response and panel creation
    if new_status == CaseStatus.AWAITING_RESPONSE:
        logger.info(f"Case {case.id} awaiting response from opposite party")
    elif new_status == CaseStatus.PANEL_CREATED:
        logger.info(f"Case {case.id} panel created")
    
    case.creator_status = new_status
    case.opposite_party_status = new_status
    case.updated_at = datetime.now(timezone.utc)
    logger.info(f"Case {case.id} status updated to {new_status}")
    return case


async def notify_case_status_change(db, case, new_status, actor_user):
    """
    Notify the relevant parties when a case status changes.
    
    db: Session
    case: Case object
    new_status: CaseStatus
    actor_user: User who triggered the change
    """
    messages = []

    if new_status == CaseStatus.PANEL_SELECTION:
        messages.append({
            "recipient_id": case.user_id,  # creator
            "message": f"Your case was accepted by {actor_user.name}. Proceed to panel selection."
        })
    elif new_status == CaseStatus.PANEL_CREATED:
        for uid in [case.user_id, case.opposite_party_user_id]:
            messages.append({
                "recipient_id": uid,
                "message": f"Panel has been created for Case #{case.id}. Mediation will start soon."
            })
    elif new_status == CaseStatus.MEDIATION_IN_PROGRESS:
        for uid in [case.user_id, case.opposite_party_user_id]:
            messages.append({
                "recipient_id": uid,
                "message": f"Mediation has started for Case #{case.id}. Please await instructions."
            })
    elif new_status in [CaseStatus.RESOLVED, CaseStatus.UNRESOLVED]:
        for uid in [case.user_id, case.opposite_party_user_id]:
            messages.append({
                "recipient_id": uid,
                "message": f"Case #{case.id} has been marked as {new_status.value.upper()}."
            })

    # Store and push notifications
    for msg in messages:
        db_notification = Notification(user_id=msg["recipient_id"], message=msg["message"])
        db.add(db_notification)
        await manager.send_personal_message(
            json.dumps({"type": "case_update", "case_id": case.id, "message": msg["message"]}),
            user_id=msg["recipient_id"]
        )

    db.commit()
