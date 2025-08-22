import json
from sqlalchemy.orm import Session
from app.models.case import Case
from app.models.notification import Notification
from app.utils.enums import CaseStatus
from datetime import datetime, timezone
import logging
from app.websocket_manager import manager
from app.utils.enums import NotificationType

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
    """
    notifications = []

    if new_status == CaseStatus.PANEL_SELECTION:
        notifications.append({
            "recipient_id": case.user_id,  # creator
            "title": "Case Update",
            "type": NotificationType.INFO,
            "message": f"Your case was accepted by {actor_user.name}. Proceed to panel selection."
        })

    elif new_status == CaseStatus.PANEL_CREATED:
        for uid in [case.user_id, case.opposite_party_user_id]:
            notifications.append({
                "recipient_id": uid,
                "title": "Case Update",
                "type": NotificationType.SUCCESS,
                "message": f"Panel has been created for Case #{case.id}. Mediation will start soon."
            })

    elif new_status == CaseStatus.MEDIATION_IN_PROGRESS:
        for uid in [case.user_id, case.opposite_party_user_id]:
            notifications.append({
                "recipient_id": uid,
                "title": "Case Update",
                "type": NotificationType.INFO,
                "message": f"Mediation has started for Case #{case.id}. Please await instructions."
            })

    elif new_status in [CaseStatus.RESOLVED, CaseStatus.UNRESOLVED]:
        notif_type = NotificationType.SUCCESS if new_status == CaseStatus.RESOLVED else NotificationType.WARNING
        for uid in [case.user_id, case.opposite_party_user_id]:
            notifications.append({
                "recipient_id": uid,
                "title": "Case Update",
                "type": notif_type,
                "message": f"Case #{case.id} has been marked as {new_status.value.upper()}."
            })

    # Save and send
    for notif in notifications:
        db_notification = Notification(
            user_id=notif["recipient_id"],
            title=notif["title"],
            type=notif["type"],
            message=notif["message"],
            case_id=case.id,
            is_read=False
        )
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)

        await manager.send_personal_message(
            json.dumps({
                "id": db_notification.id,
                "title": db_notification.title,
                "type": db_notification.type,
                "message": db_notification.message,
                "created_at": db_notification.created_at.isoformat(),
                "is_read": db_notification.is_read,
                "case_id": case.id,
                "from_user": actor_user.name
            }),
            user_id=notif["recipient_id"]
        )