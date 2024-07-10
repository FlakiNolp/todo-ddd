from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
import sys


router = APIRouter(tags=["app"])


@router.get("/")
async def root():
    return FileResponse(path=r"app/files/index.html")


@router.get("/{file}")
async def file_get(file: str):
    try:
        return FileResponse(path=rf"app/files/{file}")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
