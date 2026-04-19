import google.generativeai as genai
import json
import os
import re
from typing import List, Dict, Optional

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

    def analyze_loan_eligibility(self, income: float, co_applicant: str, university_tier: str) -> dict:
        """Analyze loan eligibility using Gemini"""
        try:
            prompt = f"""You are an Indian education loan advisor. Analyze the following student profile for education loan eligibility:
- Annual Family Income: ₹{income:,.0f}
- Co-applicant Status: {co_applicant}
- University Tier: {university_tier}

Provide a realistic eligibility assessment. Return ONLY a JSON object with these exact fields:
{{
  "eligible": true or false,
  "maxLoanAmount": "e.g. ₹40 Lakhs",
  "eligibilityScore": "e.g. 82%",
  "summary": "2-3 sentence summary of eligibility",
  "tips": ["tip1", "tip2", "tip3"]
}}
Return ONLY the JSON, no other text."""

            response = self.model.generate_content(prompt)
            result_text = response.text.strip() if response.text else ""
            result = self._extract_json(result_text)
            if result and isinstance(result, dict):
                return result
            return self._get_fallback_eligibility(income, co_applicant, university_tier)
        except Exception as e:
            print(f"Error analyzing loan eligibility: {e}")
            return self._get_fallback_eligibility(income, co_applicant, university_tier)

    def recommend_loan_offer(self, bank_name: str, income: float, university_tier: str) -> dict:
        """Recommend a specific bank loan offer using Gemini"""
        try:
            prompt = f"""You are an Indian education loan advisor. A student wants to apply for an education loan from {bank_name}.
Profile:
- Annual Family Income: ₹{income:,.0f}
- University Tier: {university_tier}

Provide a concise, practical loan application recommendation for {bank_name}. Return ONLY a JSON object:
{{
  "bank": "{bank_name}",
  "recommendation": "2-3 sentence actionable advice for this specific bank",
  "requiredDocuments": ["doc1", "doc2", "doc3"],
  "estimatedApprovalTime": "e.g. 7-10 working days",
  "tip": "One specific insider tip for this bank"
}}
Return ONLY the JSON, no other text."""

            response = self.model.generate_content(prompt)
            result_text = response.text.strip() if response.text else ""
            result = self._extract_json(result_text)
            if result and isinstance(result, dict):
                return result
            return self._get_fallback_loan_offer(bank_name)
        except Exception as e:
            print(f"Error recommending loan offer: {e}")
            return self._get_fallback_loan_offer(bank_name)

    def _get_fallback_eligibility(self, income: float, co_applicant: str, university_tier: str) -> dict:
        """Fallback eligibility if Gemini call fails"""
        max_loan = "₹50 Lakhs" if "Tier 1" in university_tier else "₹30 Lakhs"
        score = "78%" if income > 1000000 else "60%"
        return {
            "eligible": True,
            "maxLoanAmount": max_loan,
            "eligibilityScore": score,
            "summary": "Based on your income and university tier, you qualify for an education loan. Having a salaried co-applicant improves your chances significantly.",
            "tips": ["Maintain a clean credit history", "Keep income proof documents ready", "Apply early to avoid delays"]
        }

    def _get_fallback_loan_offer(self, bank_name: str) -> dict:
        """Fallback loan offer if Gemini call fails"""
        return {
            "bank": bank_name,
            "recommendation": f"{bank_name} offers competitive rates for education loans. Visit your nearest branch with complete documentation for the fastest processing.",
            "requiredDocuments": ["Admission letter", "Fee structure", "Income proof (co-applicant)", "Address proof", "Academic records"],
            "estimatedApprovalTime": "10-15 working days",
            "tip": "Apply online first to get a pre-approval reference number, which speeds up in-branch processing."
        }

    def chat(self, user_message: str, history: Optional[List[Dict]] = None) -> str:
        """Chat with Gemini as an education advisor"""
        system_prompt = """You are EduMentor AI, a friendly and knowledgeable higher education advisor for Indian students planning to study abroad.

You help students with:
- University selection based on GPA, test scores (GRE/GMAT), and preferred countries
- Education loan guidance (Indian banks like HDFC Credila, SBI, Axis Bank)
- Statement of Purpose (SOP) and application tips
- Admission probability assessment
- Visa process and financial planning
- Scholarship opportunities

Formatting Guidelines:
- Use **bullet points** and **numbered lists** for lists of universities, steps, or tips.
- Use **bold text** for university names or key terms.
- Use **double newlines** between paragraphs to ensure a clean, uncluttered layout.
- Keep responses concise (2-4 paragraphs max) but well-structured.
- Be warm, encouraging and practical.
- Use INR for money (₹ symbol)."""

        try:
            # Build conversation for Gemini with history
            chat_model = self.model.start_chat(history=[])

            # Send system context first if no history
            if not history:
                chat_model.send_message(f"[System: {system_prompt}]\n\nUser: {user_message}")
            else:
                # Reconstruct history
                gemini_history = []
                for msg in (history or []):
                    role = "user" if msg.get("sender") == "user" else "model"
                    gemini_history.append({"role": role, "parts": [msg.get("text", "")]})

                # Gemini CRITICAL: History must start with a 'user' message
                # If the first message is from 'model', we skip it.
                while gemini_history and gemini_history[0]["role"] != "user":
                    gemini_history.pop(0)

                chat_model = self.model.start_chat(history=gemini_history)
                chat_model.send_message(user_message)

            response = chat_model.last.text.strip() if chat_model.last else ""
            return response if response else self._get_fallback_chat(user_message)

        except Exception as e:
            print(f"DEBUG [Gemini Error]: {str(e)}")
            return self._get_fallback_chat(user_message)

    def _get_fallback_chat(self, user_input: str) -> str:
        """Fallback chat response if Gemini fails"""
        inp = user_input.lower()
        if "university" in inp or "suggest" in inp:
            return "Based on strong profiles, I'd recommend exploring Tier 1 universities in the US like Purdue, UMass Amherst, or USC. Check the AI Career Navigator for personalised picks!"
        elif "loan" in inp or "finance" in inp:
            return "Education loans from HDFC Credila and SBI are popular for Indian students. Visit the Finance & Loans section for pre-calculated EMIs and eligibility checks."
        elif "chance" in inp or "admission" in inp:
            return "Admission chances depend on GPA, test scores, and SOP quality. Use the Admission Predictor tool for a personalised probability estimate."
        elif "sop" in inp or "statement" in inp:
            return "A strong SOP should highlight your academic journey, research interests, and career goals. Keep it under 1000 words and tailor it to each university."
        else:
            return "I can help with university selection, education loans, admission chances, and SOP tips. What would you like to explore?"

