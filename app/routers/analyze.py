from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import uuid

from app.services.parser_service import parse_file
from app.services.rag_service import analyze_artifact

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    file_id = uuid.uuid4().hex
    saved_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_artifact(saved_path)

    return JSONResponse(content={
        "filename": file.filename,
        "llm_analysis": result
    })