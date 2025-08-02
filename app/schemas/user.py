from pydantic import BaseModel, EmailStr, field_validator
from fastapi import Form
from app.utils.enums import Gender
from typing import Optional

# base schema for user
class UserBase(BaseModel):
    name: str
    age: int
    gender: Gender
    street: str
    city: str
    zip_code: str
    email: EmailStr
    phone: str
    password: str

# schemas for user creation and response
class UserCreate(UserBase):
    photo: Optional[str] = None

    @field_validator('age')
    def validate_age(cls, v):
        if v < 18:
            raise ValueError('Age must be at least 18')
        return v
    
    

# I created this schema because we are using a multipart form
# and because of that fastapi needs us to use form
class UserForm(UserCreate):
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        age: int = Form(...),
        gender: Gender = Form(...),
        street: str = Form(...),
        city: str = Form(...),
        zip_code: str = Form(...),
        email: EmailStr = Form(...),
        phone: str = Form(...),
        password: str = Form(...)
    ):
        return cls(
            name=name,
            age=age,
            gender=gender,
            street=street,
            city=city,
            zip_code=zip_code,
            email=email,
            phone=phone,
            password=password
        )

class UserResponse(UserBase):
    id: int
    photo: Optional[str] = None
    
    class Config:
        form_attributes = True
        

# schema for user update
class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    street: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    photo: Optional[str] = None

    @field_validator('age')
    def validate_age(cls, v):
        if v is not None and v < 18:
            raise ValueError('Age must be at least 18')
        return v
    
class OppositeParty(BaseModel):
    id: int
    name: str
    phone: str
    street: str
    city: str
    zip_code: str
    
    class Config:
        from_attributes = True
    