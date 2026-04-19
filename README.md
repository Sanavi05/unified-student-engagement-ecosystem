# 🎓 Unified Student Engagement Ecosystem

A comprehensive AI-powered platform for student engagement, study abroad planning, and education loan qualification. Built with Vue 3, Node.js/Express, Python/FastAPI, and Google Gemini AI.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Vue 3 Frontend (Vite)                          │
│                  ChatWidget + ROI Dashboard                         │
└─────────────────────────────────────────────────────────────────────┘
                              ↓↑
                         (Port 3000)
                              ↓↑
┌─────────────────────────────────────────────────────────────────────┐
│                 Node.js Backend (Express API)                       │
│              POST /api/chat, GET /api/dashboard                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓↑
                         (Port 5000)
                         ↓↑
        ┌────────────────────────────────────────┐
        │       MongoDB (StudentProfile)         │
        │  - Demographics                        │
        │  - Financials                          │
        │  - Chat History                        │
        │  - Engagement State                    │
        └────────────────────────────────────────┘
                              ↓↑
                         (Webhook)
                              ↓↑
┌─────────────────────────────────────────────────────────────────────┐
│          Python FastAPI (AI Microservice)                           │
│        - Celery Task Queue + Redis Broker                           │
│        - Google Gemini API Integration                              │
│        - Structured Data Extraction                                 │
└─────────────────────────────────────────────────────────────────────┘
                              ↓↑
                         (Port 8000)
```

## 📦 Project Structure

```
unified-student-engagement-ecosystem/
├── frontend-vue/                  # Vue 3 + Vite + TailwindCSS
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWidget.vue     # AI chat interface
│   │   │   └── ROIDashboard.vue   # Financial dashboard
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── README.md
│
├── backend-node/                  # Express.js API Server
│   ├── models/
│   │   └── StudentProfile.js      # Mongoose schema
│   ├── server.js                  # Express app
│   ├── package.json
│   └── README.md
│
├── ai-python-service/             # FastAPI + Celery + Gemini
│   ├── celery_config.py           # Celery configuration
│   ├── prompts.py                 # Gemini prompt template
│   ├── tasks.py                   # Celery tasks
│   ├── main.py                    # FastAPI app
│   ├── requirements.txt
│   └── README.md
│
├── .env.example                   # Root environment template
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites

- Node.js >= 16
- Python >= 3.9
- MongoDB (Atlas or local)
- Redis (for Celery)
- Google Gemini API Key

### 1️⃣ Setup Environment Variables

```bash
# Copy and fill in .env.example
cp .env.example .env
```

Update `.env` with your credentials:
```env
MONGODB_URI=your_mongodb_connection_string
GEMINI_API_KEY=your_gemini_api_key
REDIS_URL=redis://localhost:6379
NODE_PORT=5000
PYTHON_PORT=8000
```

### 2️⃣ Start Redis (Required for Celery)

```bash
# macOS
brew install redis
redis-server

# Linux
sudo apt-get install redis-server
redis-server

# Docker
docker run -d -p 6379:6379 redis
```

### 3️⃣ Start Python AI Service

```bash
cd ai-python-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Celery worker (Terminal 1)
celery -A celery_config worker --loglevel=info

# Start FastAPI server (Terminal 2)
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4️⃣ Start Node.js Backend

```bash
cd backend-node

# Install dependencies
npm install

# Start backend server
npm run dev
```

Backend runs on `http://localhost:5000`. Verify with:
```bash
curl http://localhost:5000/health
```

### 5️⃣ Start Vue 3 Frontend

```bash
cd frontend-vue

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs on `http://localhost:3000`. Open in browser!

---

## 🔄 Core Data Flow

1. **User Interaction** (Frontend)
   - User opens ChatWidget and sends message about study plans

2. **Chat Submission** (Frontend → Backend)
   - Vue sends POST to `/api/chat` with userId + message
   - Backend creates/updates StudentProfile in MongoDB
   - Backend forwards to Python service

3. **AI Processing** (Backend → Python Service)
   - Python queues Celery task
   - Celery worker calls Google Gemini API with Study Abroad Copilot prompt
   - Gemini extracts: targetCourse, targetCountry, currentCGPA, estimatedCourseCost, userBudget

4. **Data Extraction** (Python Service)
   - Gemini returns structured JSON + friendly message
   - Python parses and validates extracted data
   - Calculates fundingGap = estimatedCourseCost - userBudget

5. **Webhook Update** (Python Service → Backend)
   - Python webhooks POST to `/api/webhook/ai-update`
   - Backend updates StudentProfile with extracted data
   - Sets `roiDashboardGenerated = true`

6. **Dashboard Refresh** (Frontend)
   - Frontend polls `/api/dashboard/:userId`
   - ROI Dashboard displays financials + progress bars
   - "Apply for Loan" button appears if fundingGap > 0

7. **Loan Application** (Frontend → User)
   - User clicks "Apply for Loan"
   - Mock success alert shows zero-touch auto-fill message
   - Demo completes

---

## 🎯 Key Features

### ✅ ChatWidget Component
- Real-time conversational AI chat
- Study Abroad Copilot persona
- Chat history display
- Loading states and error handling
- Auto-updates profile on message send

### ✅ ROI Dashboard Component
- **Financial Visualization**: Cost vs Budget progress bars
- **Funding Gap Calculation**: Dynamic display when gap exists
- **Student Profile Display**: Course, country, CGPA summary
- **Pre-Qualified Loan Button**: 
  - Appears only when fundingGap > 0
  - Requires roiDashboardGenerated flag
  - Zero-touch auto-fill with student data
  - Mock success alert confirms submission

### ✅ MongoDB StudentProfile Schema
```javascript
{
  userId: String,
  demographics: {
    targetCountry: String,
    targetCourse: String,
    currentCGPA: Number
  },
  financials: {
    estimatedCourseCost: Number,
    userBudget: Number,
    fundingGap: Number
  },
  engagementState: {
    copilotChatHistory: Array,  // [{ role, message, timestamp }]
    roiDashboardGenerated: Boolean,
    loanPreQualified: Boolean
  },
  timestamps: { createdAt, updatedAt }
}
```

### ✅ Google Gemini Integration
- Study Abroad Copilot prompt template
- Structured JSON extraction
- Fallback conversational responses
- Error handling for API failures

### ✅ Celery + Redis Async Processing
- Non-blocking Gemini API calls
- Background task queue
- Result tracking
- Webhook callbacks to backend

---

## 🔧 API Endpoints

### Backend (Node.js) - Port 5000

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send chat message, update profile, trigger AI |
| GET | `/api/dashboard/:userId` | Fetch student profile + financials |
| POST | `/api/webhook/ai-update` | Receive AI-processed data (from Python) |
| GET | `/health` | Health check |

### AI Service (Python) - Port 8000

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/process-chat` | Queue Celery task for Gemini processing |
| GET | `/task-status/{task_id}` | Get Celery task status |
| GET | `/health` | Health check |

---

## 📊 Sequence Diagram

```
User          Frontend         Backend         Python          Gemini
 │                │              │               │               │
 ├─ Chat Message ─→│              │               │               │
 │                │─ POST /chat ──→              │               │
 │                │              │─ POST /process-chat ─→        │
 │                │              │               ├─ Queue Task   │
 │                │              │               │  (Celery)     │
 │                │              │               ├─ Call API ────→
 │                │              │               │               │
 │                │              │               │      ← Response ─ JSON
 │                │              │               │  Parse & Extract
 │                │              │← Webhook ─────┤─ /api/webhook
 │                │              │  Update       │
 │                │  GET /dash   │               │
 │                │← Profile    │               │
 │  ROI Display  │               │               │
 └─ Show Results ┘               │               │
```

---

## 🧪 Testing the Full Flow

### Manual End-to-End Test

1. **Start all services** (Redis, Backend, Python, Frontend)
2. **Open** http://localhost:3000 in browser
3. **Send message** to ChatWidget:
   ```
   "Hi, I'm interested in studying Computer Science in Canada. 
   My budget is $50,000 and I think the course costs around $80,000."
   ```
4. **Observe**:
   - Message appears in chat
   - "Processing..." status shows
   - AI response with extracted data appears
   - ROI Dashboard updates with financials
   - Progress bars display costs
   - **"Apply for Loan"** button appears (if fundingGap > 0)
5. **Click** "Apply for Loan"
6. **Confirm** success alert with auto-fill message

---

## 🛠️ Troubleshooting

### Backend won't connect to MongoDB
```bash
# Check MongoDB connection string in .env
# Verify network connectivity
# Test: mongo "your_connection_string"
```

### Python service not responding
```bash
# Verify Redis is running
redis-cli ping  # Should return "PONG"

# Check Python dependencies
pip list  # Verify google-generativeai, celery, fastapi installed

# Start Celery worker
celery -A celery_config worker --loglevel=info
```

### Frontend showing API errors
```bash
# Check backend proxy is configured correctly
# vite.config.js should proxy /api to :5000
# Network tab should show requests to http://localhost:5000
```

### Loan button not appearing
- Ensure AI extracted financial data (check chat for amount mentions)
- Verify `roiDashboardGenerated = true` in MongoDB
- Check fundingGap > 0 condition
- Refresh page to see latest profile

---

## 📚 Documentation

- [Frontend README](frontend-vue/README.md) - Vue 3 setup & components
- [Backend README](backend-node/README.md) - Express API routes & Mongoose
- [AI Service README](ai-python-service/README.md) - FastAPI, Celery, Gemini

---

## 🔐 Environment Variables

Create `.env` in root:

```env
# MongoDB
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db

# Gemini API
GEMINI_API_KEY=your_api_key

# Redis (Celery)
REDIS_URL=redis://localhost:6379

# Services
NODE_PORT=5000
PYTHON_PORT=8000
BACKEND_WEBHOOK_URL=http://localhost:5000/api/webhook/ai-update
```

---

## 📋 Tech Stack

| Layer | Technology | Port |
|-------|-----------|------|
| Frontend | Vue 3, Vite, TailwindCSS | 3000 |
| Backend API | Node.js, Express, Mongoose | 5000 |
| Database | MongoDB (Atlas) | Remote |
| AI Service | Python, FastAPI | 8000 |
| Task Queue | Celery, Redis | 6379 |
| LLM | Google Gemini API | Remote |

---

## 🎉 Success Criteria

✅ Frontend loads with ChatWidget + ROI Dashboard  
✅ Chat accepts user input and shows responses  
✅ AI extracts financial data from conversation  
✅ ROI Dashboard displays Cost vs Budget  
✅ Funding Gap calculated correctly  
✅ "Apply for Loan" button appears when fundingGap > 0  
✅ Zero-touch loan auto-fill alert on button click  
✅ All services communicate via webhooks  

---

## 📄 License

ISC

---

## 👨‍💻 Developer Notes

- **Hot Reload**: Frontend has Vite hot reload enabled
- **MongoDB Indexing**: StudentProfile has userId index for fast lookups
- **Celery Retry Logic**: Add retry on Gemini API failures (see tasks.py)
- **Webhook Security**: Add API key validation (future enhancement)
- **Scaling**: Deploy Redis, MongoDB, Python workers separately for production

---

Built with ❤️ for students planning their international education journey.
