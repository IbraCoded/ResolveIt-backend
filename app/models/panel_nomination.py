from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.utils.enums import PanelRole


class PanelNomination(Base):
    __tablename__ = "panel_nominations"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    nominated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(PanelRole), nullable=False)
    contact_info = Column(String, nullable=False)

    case = relationship("Case", back_populates="panel_nominations")
    user = relationship("User")