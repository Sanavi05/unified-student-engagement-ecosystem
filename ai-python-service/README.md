# AI Python Service with FastAPI + Celery + Google Gemini

Python FastAPI microservice for AI-powered student engagement.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Fill in your GEMINI_API_KEY and Redis URL.

3. Start Redis (required for Celery):
   ```bash
   redis-server
   ```

4. Start Celery worker (in a separate terminal):
   ```bash
   celery -A celery_config worker --loglevel=info
   ```

5. Start FastAPI server:
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Architecture

- **FastAPI**: HTTP endpoints for receiving chat payloads
- **Celery**: Async task queue for long-running Gemini API calls
- **Redis**: Message broker for Celery + result backend
- **Google Gemini**: LLM for structured data extraction

## API Endpoints

### POST `/process-chat`
Receives chat payload from Node.js backend and queues async Gemini processing.

**Request:**
```json
{
  "userId": "string",
  "message": "string",
  "demographics": { "targetCourse": "...", ... },
  "chatHistory": [{ "role": "user", "message": "..." }, ...]
}
```

**Response:**
```json
{
  "success": true,
  "taskId": "celery-task-id",
  "message": "Chat processing started..."
}
```

### GET `/task-status/{task_id}`
Check status of a Celery task.

**Response:**
```json
{
  "taskId": "task-id",
  "status": "PENDING|PROGRESS|SUCCESS|FAILURE",
  "result": { ...task result if ready... }
}
```

### GET `/health`
Health check endpoint.

## Prompt Template

The service uses `prompts.py` to guide Gemini in extracting:
- Target course
- Target country
- Estimated course cost
- Student's budget
- Current CGPA
- Funding gap calculation

Gemini responds with both a friendly message and structured JSON for programmatic processing.

## Celery Task: `process_student_chat`

1. Receives user message and chat history
2. Calls Google Gemini API with Study Abroad Copilot prompt
3. Extracts structured JSON from Gemini response
4. Sends webhook to Node.js backend with extracted data
5. Node.js updates MongoDB StudentProfile

## Environment Variables

See `.env.example`
