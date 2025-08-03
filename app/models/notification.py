# app/models/notification.py

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
from app.utils.enums import NotificationType

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # recipient
    message = Column(String, nullable=False)
    title = Column(String, nullable=True, default="info")  # Optional title for the notification
    type = Column(Enum(NotificationType), default=NotificationType.INFO)  # Type of notification (e.g., "case_invitation", "case_notification", "info")
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=True)  # Optional case ID if related to a case
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="notifications")
    
