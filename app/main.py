from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, case, admin
from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.models.case import Case
from app.routers.auth import router as auth_router
from app.routers.web_socket import router as websocket_routes 

app = FastAPI(title="ResolveIt Backend")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust for frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(websocket_routes)
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(case.router, prefix="/cases", tags=["cases"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Welcome to ResolveIt Backend"}