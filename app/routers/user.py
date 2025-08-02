from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserForm, OppositeParty
from app.utils.file_upload import save_file
from app.auth.dependencies import get_current_user
from app.auth.utils import hash_password
from typing import List, Optional
import os

router = APIRouter()

# create route doesn't work
@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserForm = Depends(UserForm.as_form),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
    ):
    print("hello")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="User with this email already exists")
    if file:
        if file.size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File size exceeds 10MB")
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid file type")
        # this will save the photo in the file system and set the path to be the photo property
        user.photo = await save_file(file, "photos")
    
    hashed_pw = hash_password(user.password)
    user.password = hashed_pw
    
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



# update route for user
@router.patch("/{user_id}", response_model=UserResponse)
# i am using Form because its a multipart json input cause of the file
async def update_user(
    user_id: int,
    name: Optional[str] = Form(None),
    age: Optional[int] = Form(None),
    gender: Optional[str] = Form(None),
    street: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    zip_code: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None),
    phone: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # verify if the current user is the one trying to update their own profile
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if age is not None and age < 18:
        raise HTTPException(status_code=400, detail="Age must be at least 18")

    # Handle file update
    if file:
        if file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB")
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid file type")

        if user.photo and os.path.exists(user.photo):
            os.remove(user.photo)

        user.photo = await save_file(file, "photos")

    # Update fields
    user.name = name or user.name
    user.age = age or user.age
    user.gender = gender or user.gender
    user.street = street or user.street
    user.city = city or user.city
    user.zip_code = zip_code or user.zip_code
    user.email = email or user.email
    user.phone = phone or user.phone

    db.commit()
    db.refresh(user)
    return user


# This route is used to search for users by name when selecting an opposite party for a case
@router.get("/search", response_model=List[OppositeParty])
def search_users(name: str = Query(..., min_length=1),
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)
                ):
    return (
        db.query(User)
        .filter(User.name.ilike(f"%{name}%"),
                User.id != current_user.id)  # Exclude the current user from search results
        .limit(10)
        .all()
    )
