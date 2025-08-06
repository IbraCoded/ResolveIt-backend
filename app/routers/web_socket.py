from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.db.session import get_db
from app.websocket_manager import manager
from app.config import settings
from app.auth.dependencies import get_current_user_from_ws
from app.models.user import User
from sqlalchemy.orm import Session

router = APIRouter()

# @router.websocket("/ws/{user_id}")
# async def websocket_endpoint(
#     websocket: WebSocket,
#     user_id: int,
#     current_user: User = Depends(get_current_user)
#     ):
#     await manager.connect(user_id, websocket)
#     try:
#         while True:
#             # To keep the connection alive
#             await websocket.receive_text()  
#     except WebSocketDisconnect:
#         manager.disconnect(user_id)

# The endpoint is now secure, using the authenticated user's ID
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    try:
        user = await get_current_user_from_ws(websocket, db)
        await manager.connect(user.id, websocket)

        while True:
            data = await websocket.receive_text()
            # Handle messages if needed
    except WebSocketDisconnect:
        manager.disconnect(user.id)
    except Exception as e:
        print("WebSocket error:", e)
        await websocket.close()