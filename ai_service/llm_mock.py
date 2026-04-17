class MockLLMProvider:
    def __init__(self):
        self.provider_name = "Mock_AI"

    def generate_timeline(self, user_profile: dict) -> list:
        # Simulate AI generating a timeline
        return [
            {"month": "Month 1", "task": "Shortlist Universities and prepare for GRE/GMAT."},
            {"month": "Month 2", "task": "Write first draft of Statement of Purpose (SOP)."},
            {"month": "Month 3", "task": "Finalize Letters of Recommendation (LORs) and submit applications."},
            {"month": "Month 4", "task": "Apply for Education Loans based on admits."},
            {"month": "Month 5", "task": "Visa interview preparation and mock interviews."}
        ]

    def recommend_universities(self, gpa: float, country: str) -> list:
        # Simulate AI recommendation engine
        universities = []
        if country.lower() == 'us':
            if gpa >= 8.5:
                universities = ["Stanford University", "MIT", "UC Berkeley"]
            else:
                universities = ["Arizona State Univ", "Northeastern Univ"]
        elif country.lower() == 'uk':
            if gpa >= 8.5:
                universities = ["Oxford", "Cambridge", "Imperial College"]
            else:
                universities = ["University of Manchester", "King's College London"]
        else:
            universities = ["University of Toronto", "University of Melbourne"]
        
        return universities

    def predict_admission_chance(self, target_uni: str, score: int) -> dict:
        # Mock prediction logic
        chance = min(max(50 + (score / 340) * 40 if score else 70, 0), 99)
        return {"university": target_uni, "probability": f"{int(chance)}%"}
