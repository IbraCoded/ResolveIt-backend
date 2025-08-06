from fastapi import Depends, HTTPException, status, Query
from fastapi import WebSocket
from jose import JWTError, jwt
from app.config import settings
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.auth.utils import decode_access_token, ALGORITHM, SECRET_KEY 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# This function is used to get the current user from a WebSocket connection
# It assumes the token is passed as a query parameter
# Later we can improve this by using a more secure method of passing the token
async def get_current_user_from_ws(websocket: WebSocket, db: Session) -> User:
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        raise ValueError("Missing token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)
        user_id = payload.get("user_id")
        if user_id is None:
            raise ValueError("Invalid payload")
    except JWTError:
        await websocket.close(code=1008)
        raise ValueError("Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        await websocket.close(code=1008)
        raise ValueError("User not found")

    return user