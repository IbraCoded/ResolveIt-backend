from sqlalchemy import Column, Integer, String, Enum, Boolean
from app.db.base import Base
from app.utils.enums import Gender
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    photo = Column(String, nullable=True)  # Path to uploaded photo
    password = Column(String, nullable=False)
    # cases = relationship("Case", back_populates="user")
    
    role = Column(String, default='user')
    
    # Relationships
    created_cases = relationship("Case", back_populates="creator_user", foreign_keys="Case.user_id")
    accused_cases = relationship("Case", back_populates="opposite_party_user", foreign_keys="Case.opposite_party_user_id")
    
    # notifications to the user
    notifications = relationship("Notification", back_populates="user")
