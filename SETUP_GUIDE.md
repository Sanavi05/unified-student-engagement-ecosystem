# 🚀 Complete Setup Guide

Step-by-step instructions to get the Unified Student Engagement Ecosystem running locally.

## Prerequisites

Before starting, ensure you have:

- **Node.js** >= 16.x [Download](https://nodejs.org/)
- **Python** >= 3.9 [Download](https://www.python.org/)
- **Git** [Download](https://git-scm.com/)
- **Redis** (See installation below)
- **MongoDB** account (Atlas or local) [Create Free Account](https://www.mongodb.com/cloud/atlas)
- **Google Gemini API Key** [Get API Key](https://makersuite.google.com/app/apikey)

### Install Redis

**macOS (using Homebrew):**
```bash
brew install redis
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install redis-server
```

**Windows:**
Download from [here](https://github.com/microsoftarchive/redis/releases) or use Docker:
```bash
docker run -d -p 6379:6379 redis
```

**Docker (Any OS):**
```bash
docker run -d -p 6379:6379 redis
```

Verify Redis installation:
```bash
redis-cli ping
# Should return: PONG
```

---

## Step 1: Clone & Navigate to Project

```bash
cd ~/Desktop/unified-student-engagement-ecosystem
```

---

## Step 2: Create & Configure `.env` File

```bash
# Copy template
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# MongoDB - Get from MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/student_engagement?retryWrites=true&w=majority

# Google Gemini API - Get from Google AI Studio
GEMINI_API_KEY=your_gemini_api_key_here

# Redis Connection (default local)
REDIS_URL=redis://localhost:6379

# Server Ports
NODE_PORT=5000
PYTHON_PORT=8000
```

### Getting Your API Credentials

#### MongoDB URI
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user
4. Get connection string (looks like: `mongodb+srv://user:pass@cluster0...`)
5. Replace `password` with your user password

#### Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and paste in `.env`

---

## Step 3: Start Redis

Open a terminal and start Redis:

```bash
redis-server
```

You should see:
```
Ready to accept connections
```

Leave this terminal running!

---

## Step 4: Setup & Start Backend (Node.js)

Open a **new terminal**:

```bash
cd backend-node

# Install dependencies
npm install

# Start the server
npm run dev
```

You should see:
```
✓ Backend API running on http://localhost:5000
✓ Forwarding to Python service on http://localhost:8000
```

Leave this terminal running!

---

## Step 5: Setup & Start Python AI Service

Open a **new terminal**:

```bash
cd ai-python-service

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 5a: Start Celery Worker

```bash
celery -A celery_config worker --loglevel=info
```

You should see:
```
--- * ----
- *** -----
-- ******* ----
--- ***** -----
[tasks]
. celery_config.process_student_chat
```

Leave this terminal running! Open another terminal for the FastAPI server.

### 5b: Start FastAPI Server

Open a **new terminal** and navigate to `ai-python-service`:

```bash
cd ai-python-service

# Make sure venv is activated:
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Start FastAPI
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
Uvicorn running on http://0.0.0.0:8000
Application startup complete
```

Leave this terminal running!

---

## Step 6: Setup & Start Frontend (Vue 3)

Open a **new terminal**:

```bash
cd frontend-vue

# Install dependencies
npm install

# Start dev server
npm run dev
```

You should see:
```
VITE v4.4.0  ready in 123 ms

➜  Local:   http://localhost:3000/
➜  press h to show help
```

---

## Step 7: Open in Browser

Open your browser and navigate to:

```
http://localhost:3000
```

You should see:
- Header: "🎓 Student Engagement Ecosystem"
- Left side: ChatWidget with AI Copilot
- Right side: ROI Dashboard

---

## 🧪 Testing the Full Flow

### Test 1: Basic Chat

1. In ChatWidget, type:
   ```
   Hi! I want to study Computer Science in Canada. My budget is $50,000.
   ```

2. Expected results:
   - Message appears in chat
   - "Processing..." status shows
   - AI responds with extracted data
   - Dashboard updates with financials

### Test 2: ROI Dashboard

1. Check if financials appear:
   - Estimated Course Cost: Should show a value
   - Your Budget: Should show $50,000
   - Funding Gap: Should calculate difference

2. Progress bars should display visually

### Test 3: Loan Application

1. If fundingGap > 0, "Apply for Loan" button should appear
2. Click the button
3. You should see success alert:
   ```
   ✅ Loan Application Submitted!
   Your pre-qualified offer has been auto-filled...
   ```

---

## 🔍 Troubleshooting

### Issue: Backend won't start (MongoDB error)

**Solution:**
```bash
# Check .env MONGODB_URI
cat .env | grep MONGODB_URI

# Test MongoDB connection
mongod --version
# or test atlas connection string in a tool like MongoDB Compass
```

### Issue: Redis connection refused

**Solution:**
```bash
# Check if Redis is running
redis-cli ping

# If not running, start it:
redis-server

# On macOS with Homebrew:
brew services start redis
```

### Issue: Python dependencies failing

**Solution:**
```bash
# Make sure virtual environment is activated:
which python  # Should show venv path

# Reinstall dependencies:
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Chat not responding from AI

**Solution:**
1. Check Celery worker is running (should see "ready to accept tasks")
2. Verify GEMINI_API_KEY in .env is correct
3. Check Python service is forwarding to MongoDB correctly
4. Look at Celery worker terminal for error messages

### Issue: Frontend showing "API Error"

**Solution:**
```bash
# Check backend is running
curl http://localhost:5000/health

# Check Python service is running
curl http://localhost:8000/health

# Check browser console for detailed errors (F12 > Console)
```

### Issue: MongoDB connection string not working

**Solution:**
1. Verify MongoDB Atlas user password doesn't have special characters
   - If it does, URL encode them (e.g., `@` → `%40`)
2. Get new connection string from Atlas > Connect > Drivers
3. Make sure IP address is whitelisted (use "Allow access from anywhere" for testing)

---

## 📊 Service Status Check

Verify all services are running:

```bash
# Terminal 1: Redis
redis-cli ping
# Should return: PONG

# Terminal 2: Backend
curl http://localhost:5000/health
# Should return: {"status":"Backend API is running"}

# Terminal 3: Python Service
curl http://localhost:8000/health
# Should return: {"status":"AI Service is running",...}

# Terminal 4: Frontend
# Should see app at http://localhost:3000
```

---

## 🚀 Quick Start (Next Time)

After first-time setup, use the startup script:

**macOS/Linux:**
```bash
chmod +x start-all.sh
./start-all.sh
```

**Windows:**
```bash
start-all.bat
```

---

## 📁 Project Structure Reference

```
unified-student-engagement-ecosystem/
├── frontend-vue/          ← Vue 3 app (Port 3000)
├── backend-node/          ← Express API (Port 5000)
├── ai-python-service/     ← FastAPI (Port 8000)
├── .env                   ← Your credentials (don't commit!)
├── .env.example           ← Template
├── start-all.sh           ← Quick startup (macOS/Linux)
└── start-all.bat          ← Quick startup (Windows)
```

---

## 🎓 Learning Path

1. **Frontend** - Understand Vue 3 components in `frontend-vue/src/components/`
2. **Backend** - Review API routes in `backend-node/server.js`
3. **AI** - Check prompt template in `ai-python-service/prompts.py`
4. **Data Flow** - See webhook integration in `backend-node/server.js` lines 85-145

---

## 🆘 Still Having Issues?

1. Check the README.md for architecture overview
2. Review service-specific READMEs:
   - `frontend-vue/README.md`
   - `backend-node/README.md`
   - `ai-python-service/README.md`
3. Check terminal error messages carefully
4. Verify all prerequisites are installed: `node --version`, `python3 --version`, `redis-cli --version`

---

## 🎉 Next Steps

Once everything is running:

- Explore the chat with various study abroad scenarios
- Check MongoDB directly to see StudentProfile documents
- Review Celery task execution in worker terminal
- Extend with additional features (email notifications, more LLM models, etc.)

Happy coding! 🚀
