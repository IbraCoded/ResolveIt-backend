from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, case, admin
from app.db.session import engine
from app.db.base import Base
from app.routers.auth import router as auth_router
from app.routers.web_socket import router as websocket_routes
from app.routers.notification import router as notification_routes 

import app.models 

app = FastAPI(title="ResolveIt Backend")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(websocket_routes)
app.include_router(notification_routes, prefix="/notifications", tags=["notifications"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(case.router, prefix="/cases", tags=["cases"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Welcome to ResolveIt Backend"}