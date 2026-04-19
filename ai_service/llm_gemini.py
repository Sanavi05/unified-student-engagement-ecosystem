import google.generativeai as genai
import json
import os
import re
from typing import List, Dict

class GeminiProvider:
    def __init__(self, api_key: str = None):
        """Initialize Gemini provider with API key"""
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        # Using gemini-2.5-flash - latest model with 1M token support
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.provider_name = "Gemini_AI"

    def _extract_json(self, text: str):
        """Extract JSON from text, handling markdown code blocks and extra formatting"""
        try:
            # Remove markdown code blocks if present
            text = text.strip()
            if text.startswith('```'):
                text = re.sub(r'^```(?:json)?\n', '', text)
                text = re.sub(r'\n```$', '', text)
            
            # Try to parse as is
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON array or object
            try:
                match = re.search(r'\[.*\]|\{.*\}', text, re.DOTALL)
                if match:
                    return json.loads(match.group())
            except:
                pass
        
        return None

    def generate_timeline(self, user_profile: dict) -> List[Dict]:
        """Generate personalized timeline using Gemini"""
        try:
            prompt = f"""Based on this student profile:
- GPA: {user_profile.get('gpa', 'N/A')}
- Preferred Country: {user_profile.get('country', 'N/A')}
- Test Score: {user_profile.get('testScore', 'N/A')}

Generate a 5-month timeline for preparing for higher education applications.
For each month, provide a task to complete.
Format your response as a JSON array with objects containing "month" and "task" fields.
Example: [{"month": "Month 1", "task": "..."}, {"month": "Month 2", "task": "..."}]
Return ONLY the JSON array, no other text."""

            response = self.model.generate_content(prompt)
            timeline_text = response.text.strip() if response.text else ""
            
            # Parse JSON response
            timeline = self._extract_json(timeline_text)
            if timeline and isinstance(timeline, list):
                return timeline
            
            return self._get_fallback_timeline()
        except Exception as e:
            print(f"Error generating timeline: {e}")
            return self._get_fallback_timeline()

    def recommend_universities(self, gpa: float, country: str) -> List[str]:
        """Recommend universities using Gemini based on GPA and country"""
        try:
            prompt = f"""Recommend 3-5 universities for a student with:
- GPA: {gpa}
- Preferred Country: {country}

Provide practical, realistic recommendations based on the GPA level.
Format your response as a JSON array with university names only.
Example: ["University A", "University B", "University C"]
Return ONLY the JSON array, no other text."""

            response = self.model.generate_content(prompt)
            universities_text = response.text.strip() if response.text else ""
            
            # Parse JSON response
            universities = self._extract_json(universities_text)
            if universities and isinstance(universities, list):
                return universities
            
            return self._get_fallback_universities(gpa, country)
        except Exception as e:
            print(f"Error recommending universities: {e}")
            return self._get_fallback_universities(gpa, country)

    def predict_admission_chance(self, target_uni: str, score: int) -> dict:
        """Predict admission chance using Gemini"""
        try:
            prompt = f"""Based on typical admission criteria, estimate the probability of admission to {target_uni} for a student with a test score of {score} out of 340.

Provide a realistic probability percentage based on common admission statistics.
Format your response as a JSON object with "university" and "probability" fields.
Example: {{"university": "University Name", "probability": "75%"}}
Return ONLY the JSON object, no other text."""

            response = self.model.generate_content(prompt)
            prediction_text = response.text.strip() if response.text else ""
            
            # Parse JSON response
            prediction = self._extract_json(prediction_text)
            if prediction and isinstance(prediction, dict):
                return prediction
            
            return self._get_fallback_prediction(target_uni, score)
        except Exception as e:
            print(f"Error predicting admission chance: {e}")
            return self._get_fallback_prediction(target_uni, score)

    def _get_fallback_timeline(self) -> List[Dict]:
        """Fallback timeline if Gemini call fails"""
        return [
            {"month": "Month 1", "task": "Shortlist Universities and prepare for GRE/GMAT."},
            {"month": "Month 2", "task": "Write first draft of Statement of Purpose (SOP)."},
            {"month": "Month 3", "task": "Finalize Letters of Recommendation (LORs) and submit applications."},
            {"month": "Month 4", "task": "Apply for Education Loans based on admits."},
            {"month": "Month 5", "task": "Visa interview preparation and mock interviews."}
        ]

    def _get_fallback_universities(self, gpa: float, country: str) -> List[str]:
        """Fallback universities if Gemini call fails"""
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

    def _get_fallback_prediction(self, target_uni: str, score: int) -> dict:
        """Fallback prediction if Gemini call fails"""
        chance = min(max(50 + (score / 340) * 40 if score else 70, 0), 99)
        return {"university": target_uni, "probability": f"{int(chance)}%"}
