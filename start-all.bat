@echo off
REM Unified Student Engagement Ecosystem - Startup Script for Windows

setlocal enabledelayedexpansion

echo.
echo ================================================
echo Unified Student Engagement Ecosystem - Startup
echo ================================================
echo.

REM Check if .env exists
if not exist .env (
  echo WARNING: .env file not found. Creating from .env.example...
  copy .env.example .env
  echo Please update .env with your API keys and credentials
  echo.
)

REM Check Redis
echo Checking Redis...
redis-cli ping >nul 2>&1
if %errorlevel% neq 0 (
  echo WARNING: Redis is not running. Please start Redis first:
  echo    - Manual: redis-server
  echo    - Docker: docker run -d -p 6379:6379 redis
  echo.
) else (
  echo OK: Redis is running
)

REM Start Backend
echo.
echo Starting Node.js Backend... (Port 5000)
cd backend-node
if not exist node_modules (
  echo Installing dependencies...
  call npm install
)
start "Backend Server" cmd /k "npm run dev"
cd ..
echo Backend started

REM Start Python AI Service
echo.
echo Starting Python AI Service... (Port 8000)
cd ai-python-service
if not exist venv (
  echo Creating Python virtual environment...
  python -m venv venv
)
call venv\Scripts\activate.bat
echo Checking Python dependencies...
pip install -r requirements.txt >nul 2>&1
start "Celery Worker" cmd /k "celery -A celery_config worker --loglevel=info"
timeout /t 3 /nobreak
start "FastAPI Server" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
cd ..
echo Python services started

REM Start Frontend
echo.
echo Starting Vue 3 Frontend... (Port 3000)
cd frontend-vue
if not exist node_modules (
  echo Installing dependencies...
  call npm install
)
start "Frontend Dev Server" cmd /k "npm run dev"
cd ..
echo Frontend started

echo.
echo ================================================
echo All services started successfully!
echo ================================================
echo.
echo Service URLs:
echo   Frontend:    http://localhost:3000
echo   Backend:     http://localhost:5000
echo   AI Service:  http://localhost:8000
echo.
echo Open http://localhost:3000 in your browser
echo Press any key to continue...
pause
