from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_mock import MockLLMProvider
import uvicorn

app = FastAPI(title="EduPath AI Service")
llm = MockLLMProvider()

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
