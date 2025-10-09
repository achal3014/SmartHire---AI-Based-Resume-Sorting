from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import shutil
import os

from app.pipeline import ResumePipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

pipeline = ResumePipeline()

@app.post("/rank_resumes/")
async def rank_resumes(
    job_description: str = Form(...),
    jd_skills: str = Form(...),
    files: List[UploadFile] = None
):
    saved_files = []
    for file in files:
        path = os.path.join(UPLOAD_DIR, file.filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(path)

    jd_skills_list = [s.strip() for s in jd_skills.split(",")]
    ranked_results = pipeline.rank_resumes_hybrid(saved_files, job_description, jd_skills_list)
    
    # Format for frontend
    response = [
        {"name": name, "score": round(score, 3)} for name, score in ranked_results
    ]
    return {"results": response}
