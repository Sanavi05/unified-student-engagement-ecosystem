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

class LoanEligibilityRequest(BaseModel):
    income: float
    coApplicant: str
    universityTier: str

class LoanOfferRequest(BaseModel):
    bankName: str
    income: float
    universityTier: str

class ChatRequest(BaseModel):
    message: str
    history: list = []

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

@app.post("/finance/eligibility")
def check_loan_eligibility(data: LoanEligibilityRequest):
    try:
        result = llm.analyze_loan_eligibility(data.income, data.coApplicant, data.universityTier)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/finance/loan-advice")
def get_loan_advice(data: LoanOfferRequest):
    try:
        result = llm.recommend_loan_offer(data.bankName, data.income, data.universityTier)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat(data: ChatRequest):
    try:
        reply = llm.chat(data.message, data.history)
        return {"reply": reply}
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
