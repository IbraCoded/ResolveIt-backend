from fastapi import UploadFile
import os
from uuid import uuid4
from pathlib import Path

async def save_file(file: UploadFile, folder: str) -> str:
    upload_dir = Path(f"../uploads/{folder}")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_extension = file.filename.split(".")[-1]
    file_path = upload_dir / f"{uuid4()}.{file_extension}"
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return str(file_path)