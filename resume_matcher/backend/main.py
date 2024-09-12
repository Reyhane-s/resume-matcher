from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Resume(BaseModel):
    skills: List[str]
    age: Optional[int]
    degree: str

class MatchRequest(BaseModel):
    required_skills: List[str]
    required_age_range: tuple
    required_degree: str
    resumes: List[Resume]

@app.post("/match/")
def match_resumes(request: MatchRequest):
    # کد محاسبه نمرات و تطابق رزومه‌ها
    # برای ساده‌سازی، کد محاسبه نمرات را مستقیماً در اینجا کپی کن
    # یا آن را به توابع جداگانه تقسیم کن
    return {"matches": "result data"}
