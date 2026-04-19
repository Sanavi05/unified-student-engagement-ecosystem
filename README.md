# EduPath AI: Unified Student Engagement Ecosystem

EduPath AI is a comprehensive platform designed to provide personalized higher education guidance. It leverages AI to offer university recommendations, admission probability predictions, ROI calculations, and tailored financial loan options.

The ecosystem is divided into three main components: a vibrant Vue.js frontend, a robust Express.js backend, and a specialized FastAPI AI service.

## 🚀 Project Architecture

1. **Frontend (`/frontend`)**
   - **Tech Stack:** Vue 3, Vite, clean vanilla CSS.
   - **Features:** Interactive dashboard, AI career navigator, admission predictor, ROI calculator, education finance estimator, and an integrated global AI chatbot.

2. **Backend (`/backend`)**
   - **Tech Stack:** Node.js, Express, MongoDB (via Mongoose).
   - **Features:** REST API to manage users, data flow between the frontend and the AI service, and secure route handling.

3. **AI Service (`/ai_service`)**
   - **Tech Stack:** Python, FastAPI, Google Gemini API.
   - **Features:** Leverages Google's Gemini AI to provide intelligent university matching, admission probability predictions, and personalized educational timelines.

---

## 🛠️ Getting Started

Follow the steps below to run all three services concurrently in your local environment.

### Prerequisites
- Node.js (v16+)
- Python (v3.9+)
- MongoDB (Running locally or via a cloud URI like MongoDB Atlas)

---

### 1. Setup the AI Service (Python/FastAPI)

Navigate to the `ai_service` directory and install the required Python dependencies.

```bash
cd ai_service

# Create a virtual environment (Recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Create a .env file and add your Gemini API key
# Create ai_service/.env with:
# GEMINI_API_KEY=your_api_key_here

# Run the FastAPI server
uvicorn main:app --reload --port 8000
```
> The AI service will be running at `http://localhost:8000`

**Note:** To get a Gemini API key:
1. Visit [Google AI Studio](https://ai.google.dev)
2. Click "Create API Key"
3. Copy your API key and paste it in the `.env` file

---

### 2. Setup the Backend (Node.js/Express)

Navigate to the `backend` directory, install packages, establish your environment variables, and run the server.

```bash
cd backend

# Install dependencies
npm install

# IMPORTANT: Ensure your .env file is set up
# Create a .env file and add your configuration (e.g., PORT, MONGODB_URI)
# Example:
# PORT=3000
# MONGODB_URI=mongodb://localhost:27017/edupath
# FASTAPI_URL=http://localhost:8000

# Start the Expres server
npm start
```
> The Node backend will typically run at `http://localhost:3000`

---

### 3. Setup the Frontend (Vue.js/Vite)

Navigate to the `frontend` directory, install the node modules, and start the development server.

```bash
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```
> The Vue front-end will run at `http://localhost:5173`

---

## ⚡ Quick Start (Run All Services)

Once all prerequisites are installed, you can start all three services in **separate terminals**:

**Terminal 1 - AI Service:**
```bash
cd ai_service
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Backend:**
```bash
cd backend
npm start
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:3000
- AI Service: http://localhost:8000

---

## 🔑 Environment Variables

### AI Service (`ai_service/.env`)
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### Backend (`backend/.env`)
```
PORT=3000
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database
FASTAPI_URL=http://localhost:8000
```

---

## 🆘 Troubleshooting

### AI Service Issues
**Error: "404 models/gemini-* is not found"**
- The model is not available for your API key
- Run `python check_models.py` to see available models
- Update `llm_gemini.py` with an available model name

**Error: "GEMINI_API_KEY not found"**
- Ensure `ai_service/.env` exists with your API key
- Format: `GEMINI_API_KEY=your_key_here`

### Backend Issues
**Error: "Cannot find module 'mongoose'"**
- Run `npm install` in the backend folder

**Error: "AI service unavailable"**
- Ensure FastAPI is running on port 8000
- Check `FASTAPI_URL` in `backend/.env` is set to `http://localhost:8000`

### Frontend Issues
**CORS Errors**
- Ensure all three services are running
- Check that backend is on port 3000 and AI service on port 8000
- Verify `apiBase` URL in frontend components

**No recommendations showing**
- Check browser console for errors
- Ensure MongoDB is running
- Verify API responses in Network tab

---

## 🌟 Features Overview

- **Dashboard**: Get an overview of your profile completion, top university matches, and AI-generated insights regarding your applications.
- **Application Timeline**: AI-generated 5-month timeline for application preparation with color-coded milestones.
- **AI Career Navigator**: Find the most suitable university based on your background and target countries.
- **Admission Predictor**: View your chances of getting admitted into high-tier universities.
- **ROI Calculator**: Calculate estimated payback periods based on course cost.
- **Finance & Loans**: Find loan estimates and discover zero-collateral, AI-optimized offers from banking partners.
- **Chatbot (EduMentor AI)**: A dynamic modal to answer direct queries regarding loans, universities, and application health.

---

## 📋 Project Structure

```
unified-student-engagement-ecosystem/
├── frontend/                   # Vue 3 + Vite application
│   ├── src/
│   │   ├── views/             # Dashboard, Tools, Finance pages
│   │   ├── components/        # Reusable Vue components
│   │   ├── router/            # Vue Router configuration
│   │   └── App.vue
│   └── package.json
├── backend/                    # Express.js REST API
│   ├── routes/
│   │   └── api.js             # API endpoints
│   ├── models/
│   │   └── User.js            # MongoDB schemas
│   ├── server.js              # Express server
│   └── package.json
├── ai_service/                 # FastAPI + Gemini AI
│   ├── llm_gemini.py          # Gemini integration
│   ├── main.py                # FastAPI app
│   ├── requirements.txt        # Python dependencies
│   ├── check_models.py        # Model availability checker
│   └── .env                    # API key configuration
└── README.md
```

---

## 🔧 Tech Stack Summary

| Layer | Technology | Version | Port |
|-------|-----------|---------|------|
| Frontend | Vue 3 + Vite | Latest | 5173 |
| Backend | Node.js + Express | v16+ | 3000 |
| Database | MongoDB | Cloud/Local | - |
| AI Engine | FastAPI + Gemini 2.5 Flash | Latest | 8000 |

---

## 🤝 Contributing
Contributions are welcome. Please open an issue first to discuss what you would like to change.

## 📄 License
ISC License