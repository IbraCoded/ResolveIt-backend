from pydantic import BaseModel
from app.utils.enums import NotificationType
from typing import Optional, List
from datetime import datetime
from fastapi import Form
from app.utils.enums import CaseType


class NotificationBase(BaseModel):
    id: int = None
    user_id: int
    message: str
    title: Optional[str] = "info"  # Optional title for the notification
    type: NotificationType  # Type of notification (e.g., "case_invitation", "case_notification", "info")
    case_id: Optional[int] = None  # Optional case ID if related to a case
    is_read: bool = False
    created_at: datetime = datetime.now()
    
class NotificationResponse(NotificationBase):
    class Config:
        from_attributes = True