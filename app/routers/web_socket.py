# app/routers/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.websocket_manager import manager
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            # To keep the connection alive
            await websocket.receive_text()  
    except WebSocketDisconnect:
        manager.disconnect(user_id)
