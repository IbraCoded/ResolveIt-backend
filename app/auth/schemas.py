from pydantic import BaseModel, EmailStr

# models.py or similar file

from pydantic import BaseModel

class UserPublic(BaseModel):
    id: int
    name: str | None = None
    email: str
    photo: str | None = None
    class Config:
        from_atrributes = True # This tells Pydantic to read data from a SQLAlchemy model

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic