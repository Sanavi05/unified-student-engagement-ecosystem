from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_gemini import GeminiProvider
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="EduPath AI Service")
try:
    llm = GeminiProvider()
except ValueError as e:
    print(f"⚠️ Error initializing Gemini: {e}")
    print("Make sure GEMINI_API_KEY is set in your .env file")
    raise

class RecommendationRequest(BaseModel):
    gpa: float
    country: str

class AdmissionPredictionRequest(BaseModel):
    targetUniversity: str
    testScore: int

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "FastAPI AI Engine"}

@app.post("/recommend")
def recommend(data: RecommendationRequest):
    try:
        unis = llm.recommend_universities(data.gpa, data.country)
        return {"recommendations": unis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-admission")
def predict_admission(data: AdmissionPredictionRequest):
    try:
        prediction = llm.predict_admission_chance(data.targetUniversity, data.testScore)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
