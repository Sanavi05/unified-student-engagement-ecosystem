import os
from dotenv import load_dotenv
from celery import shared_task
import json
import requests
import warnings
import traceback
import logging
from prompts import STUDY_ABROAD_COPILOT_PROMPT
from celery_config import celery_app

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress deprecation warning
warnings.filterwarnings('ignore', category=FutureWarning)

# Try to import Google Gemini, but use mock if Python 3.14
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    USE_MOCK_AI = False
except (ImportError, TypeError) as e:
    print(f'[CELERY] Warning: Could not import google.generativeai: {str(e)}')
    print(f'[CELERY] Using mock AI responses for testing')
    USE_MOCK_AI = True

BACKEND_WEBHOOK_URL = os.getenv(
    'BACKEND_WEBHOOK_URL', 'http://localhost:5000/api/webhook/ai-update'
)


def mock_gemini_response(message: str):
    """Mock Gemini response for testing when real API unavailable"""
    return {
        "conversationComplete": True,
        "extractedData": {
            "targetCourse": "Computer Science",
            "targetCountry": "Canada",
            "currentCGPA": 3.8,
            "estimatedCourseCost": 80000,
            "userBudget": 50000
        },
        "friendlyMessage": f"Great question about {message}! Based on what you've told me, here's what I found:\n\n📚 **Program**: Computer Science in Canada\n💰 **Estimated Cost**: $80,000 USD\n👤 **Your Budget**: $50,000 USD\n📊 **Funding Gap**: $30,000 USD\n\nYou'll need about $30,000 more. Let me help you explore scholarship and loan options!",
        "fundingGap": 30000
    }


@celery_app.task
def process_student_chat(userId: str, message: str, chat_history: list, demographics: dict):
    """
    Celery task: Process student chat message using Google Gemini AI.
    Extracts structured data and sends webhook to Node backend.
    """
    try:
        print(f'[CELERY] Starting task for user {userId}')
        print(f'[CELERY] Use Mock AI: {USE_MOCK_AI}')
        print(f'[CELERY] GEMINI_API_KEY present: {bool(os.getenv("GEMINI_API_KEY"))}')
        
        # Format chat history for prompt
        chat_context = "\n".join(
            [
                f"{'Student' if msg.get('role') == 'user' else 'Copilot'}: {msg.get('message', '')}"
                for msg in chat_history[-5:]  # Last 5 messages for context
            ]
        )

        if USE_MOCK_AI:
            print(f'[CELERY] Using mock AI response')
            response_json = mock_gemini_response(message)
            ai_response_text = response_json['friendlyMessage']
            extracted_data = response_json['extractedData']
            financial_update = {
                'estimatedCourseCost': extracted_data['estimatedCourseCost'],
                'userBudget': extracted_data['userBudget']
            }
        else:
            # Prepare prompt
            prompt = STUDY_ABROAD_COPILOT_PROMPT.format(
                chat_history=chat_context,
                user_message=message,
            )

            print(f'[CELERY] Calling Gemini API...')
            
            # Call Gemini API
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            ai_response_text = response.text
            
            print(f'[CELERY] Got response from Gemini: {len(ai_response_text)} chars')

            # Extract JSON from response
            extracted_data = None
            financial_update = None

            try:
                # Try to extract JSON from the response
                json_start = ai_response_text.find('{')
                json_end = ai_response_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = ai_response_text[json_start:json_end]
                    parsed_json = json.loads(json_str)

                    extracted_data = parsed_json.get('extractedData', {})
                    ai_response_text = parsed_json.get('friendlyMessage', ai_response_text)
                    
                    # Prepare financial update
                    if extracted_data:
                        financial_update = {}
                        if extracted_data.get('estimatedCourseCost'):
                            financial_update['estimatedCourseCost'] = extracted_data.get(
                                'estimatedCourseCost'
                            )
                        if extracted_data.get('userBudget'):
                            financial_update['userBudget'] = extracted_data.get('userBudget')
            except json.JSONDecodeError:
                # If JSON extraction fails, use full response as message
                pass

        # Send webhook to Node backend
        webhook_payload = {
            'userId': userId,
            'aiMessage': ai_response_text,
            'extractedData': extracted_data if not USE_MOCK_AI else extracted_data,
            'financialUpdate': financial_update if not USE_MOCK_AI else financial_update,
        }

        print(f'[CELERY] Sending webhook to {BACKEND_WEBHOOK_URL}')
        response = requests.post(BACKEND_WEBHOOK_URL, json=webhook_payload, timeout=10)
        response.raise_for_status()
        print(f'[CELERY] Webhook successful')

        return {
            'success': True,
            'userId': userId,
            'aiResponse': ai_response_text,
            'extractedData': extracted_data,
        }

    except Exception as e:
        error_msg = str(e)
        error_traceback = traceback.format_exc()
        print(f'[CELERY ERROR] Processing chat for user {userId}')
        print(f'[CELERY ERROR] Error: {error_msg}')
        print(f'[CELERY ERROR] Traceback:\n{error_traceback}')
        logger.error(f'Error processing chat: {error_msg}\n{error_traceback}')
        return {
            'success': False,
            'userId': userId,
            'error': error_msg,
        }
