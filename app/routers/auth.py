from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.auth.schemas import UserLogin, Token
from app.models.user import User
from app.auth.utils import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.email, "user_id": user.id})
    user_data_for_response = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "photo": user.photo
    }
    return {"access_token": token, "token_type": "bearer", "user": user_data_for_response}