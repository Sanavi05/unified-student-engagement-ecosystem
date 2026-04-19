import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from celery_config import celery_app 
from tasks import process_student_chat
import logging

# Load environment variables from .env file
load_dotenv()

from tasks import process_student_chat
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title='Unified Student Engagement AI Service',
    description='Python FastAPI service with Gemini AI and Celery async processing',
    version='1.0.0',
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# Pydantic models
class ChatMessage(BaseModel):
    role: str
    message: str
    timestamp: Optional[str] = None


class ProcessChatRequest(BaseModel):
    userId: str
    message: str
    demographics: Optional[Dict] = None
    chatHistory: Optional[List[Dict]] = None


class ProcessChatResponse(BaseModel):
    success: bool
    taskId: str
    message: str


# Routes


@app.get('/health')
def health_check():
    """Health check endpoint"""
    return {
        'status': 'AI Service is running',
        'service': 'Unified Student Engagement AI',
    }


@app.post('/process-chat', response_model=ProcessChatResponse)
async def process_chat(request: ProcessChatRequest):
    """
    Accepts chat payload from Node backend.
    Triggers Celery task for async Gemini processing.
    Returns task ID for tracking.
    """
    try:
        if not request.userId or not request.message:
            raise HTTPException(
                status_code=400,
                detail='userId and message are required',
            )

        logger.info(f'[FastAPI] Received chat request from user: {request.userId}')
        print(f'[FastAPI] Message: {request.message[:50]}...')

        # Queue Celery task
        task = process_student_chat.delay(
            userId=request.userId,
            message=request.message,
            chat_history=request.chatHistory or [],
            demographics=request.demographics or {},
        )

        logger.info(f'[FastAPI] Queued Celery task {task.id} for user {request.userId}')
        print(f'[FastAPI] Task queued with ID: {task.id}')

        return ProcessChatResponse(
            success=True,
            taskId=str(task.id),
            message=f'Chat processing started. Task ID: {task.id}',
        )

    except Exception as e:
        logger.error(f'Error processing chat: {str(e)}')
        print(f'[FastAPI ERROR] {str(e)}')
        raise HTTPException(
            status_code=500,
            detail=f'Error processing chat: {str(e)}',
        )


@app.get('/task-status/{task_id}')
def get_task_status(task_id: str):
    """Get the status of a Celery task"""
    try:
        from celery_config import celery_app

        task = celery_app.AsyncResult(task_id)
        
        print(f'[FastAPI] Checking task status: {task_id}')
        print(f'[FastAPI] Status: {task.status}')
        
        if task.status == 'FAILURE':
            print(f'[FastAPI] Task failed with error: {task.info}')

        return {
            'taskId': task_id,
            'status': task.status,
            'result': task.result if task.ready() else None,
        }

    except Exception as e:
        logger.error(f'Error fetching task status: {str(e)}')
        print(f'[FastAPI ERROR] Getting task status: {str(e)}')
        raise HTTPException(
            status_code=500,
            detail=f'Error fetching task status: {str(e)}',
        )


if __name__ == '__main__':
    import uvicorn

    PORT = int(os.getenv('PYTHON_PORT', 8000))
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=PORT,
        log_level='info',
    )
