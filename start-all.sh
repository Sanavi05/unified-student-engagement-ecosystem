#!/bin/bash

# Unified Student Engagement Ecosystem - Startup Script
# This script starts all services in separate terminal tabs/windows

set -e

# Colors for output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}🚀 Unified Student Engagement Ecosystem - Startup${NC}"
echo -e "${CYAN}================================================${NC}\n"

# Kill any existing processes on ports 3000, 5000, 8000
echo -e "${YELLOW}Cleaning up old processes...${NC}"
lsof -i :3000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9 2>/dev/null || true
lsof -i :5000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9 2>/dev/null || true
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9 2>/dev/null || true
sleep 1

# Check if .env exists
if [ ! -f .env ]; then
  echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
  cp .env.example .env
  echo -e "${YELLOW}Please update .env with your API keys and credentials${NC}\n"
fi

# Check if Redis is running
echo -e "${CYAN}Checking Redis...${NC}"
if ! command -v redis-cli &> /dev/null; then
  echo -e "${YELLOW}⚠️  Redis CLI not found. Please install Redis.${NC}"
  echo -e "${YELLOW}   macOS: brew install redis${NC}"
  echo -e "${YELLOW}   Linux: sudo apt-get install redis-server${NC}"
  echo -e "${YELLOW}   Docker: docker run -d -p 6379:6379 redis${NC}"
else
  if redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Redis is running${NC}"
  else
    echo -e "${YELLOW}⚠️  Redis is not running. Starting...${NC}"
    redis-server &
    sleep 2
    echo -e "${GREEN}✓ Redis started${NC}"
  fi
fi

# Start Node.js Backend
echo -e "\n${CYAN}Starting Node.js Backend... (Port 5000)${NC}"
cd backend-node
if [ ! -d node_modules ]; then
  echo -e "${YELLOW}Installing dependencies...${NC}"
  npm install
fi
npm run dev &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
sleep 3  # Wait for backend to fully start and bind to port
cd ..

# Start Python AI Service
echo -e "\n${CYAN}Starting Python AI Service... (Port 8000)${NC}"
cd ai-python-service

# Create virtual environment if it doesn't exist
if [ ! -d venv ]; then
  echo -e "${YELLOW}Creating Python virtual environment...${NC}"
  python3 -m venv venv
fi

# Activate venv and install/update dependencies
source venv/bin/activate
echo -e "${YELLOW}Checking Python dependencies...${NC}"
pip install -r requirements.txt > /dev/null 2>&1

# Start Celery worker in background
echo -e "${YELLOW}Starting Celery worker...${NC}"
celery -A celery_config worker --loglevel=info &
CELERY_PID=$!
sleep 3
echo -e "${GREEN}✓ Celery worker started (PID: $CELERY_PID)${NC}"

# Start FastAPI server
echo -e "${YELLOW}Starting FastAPI server...${NC}"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
FASTAPI_PID=$!
sleep 2
echo -e "${GREEN}✓ FastAPI started (PID: $FASTAPI_PID)${NC}"
cd ..

# Start Vue 3 Frontend
echo -e "\n${CYAN}Starting Vue 3 Frontend... (Port 3000)${NC}"
cd frontend-vue
if [ ! -d node_modules ]; then
  echo -e "${YELLOW}Installing dependencies...${NC}"
  npm install
fi
echo -e "${YELLOW}Starting dev server...${NC}"
npm run dev &
FRONTEND_PID=$!
sleep 2
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
cd ..

# Summary
echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}✅ All services started successfully!${NC}"
echo -e "${GREEN}================================================${NC}\n"

echo -e "${CYAN}📍 Service URLs:${NC}"
echo -e "   Frontend:    ${GREEN}http://localhost:3000${NC}"
echo -e "   Backend:     ${GREEN}http://localhost:5000${NC}"
echo -e "   AI Service:  ${GREEN}http://localhost:8000${NC}"
echo -e "   Redis:       ${GREEN}localhost:6379${NC}\n"

echo -e "${CYAN}🛑 To stop all services, press Ctrl+C${NC}\n"

# Wait for all background processes
wait $BACKEND_PID $CELERY_PID $FASTAPI_PID $FRONTEND_PID

echo -e "\n${YELLOW}Services stopped.${NC}"
