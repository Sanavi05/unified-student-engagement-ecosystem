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
   - **Tech Stack:** Python, FastAPI.
   - **Features:** Houses specific machine learning or logical models (like mock LLM integrations) to provide dynamic university matching, admission tracking, and personalized insights.

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

# Install dependencies (typically fastapi, uvicorn)
pip install fastapi uvicorn pydantic

# Run the FastAPI server
uvicorn main:app --reload --port 5000
```
> The AI service will be running at `http://localhost:5000`

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
# AI_SERVICE_URL=http://localhost:5000

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

## 🌟 Features Overview

- **Dashboard**: Get an overview of your profile completion, top university matches, and AI-generated insights regarding your applications.
- **AI Career Navigator**: Find the most suitable university based on your background and target countries.
- **Admission Predictor**: View your chances of getting admitted into high-tier universities.
- **ROI Calculator**: Calculate estimated payback periods based on course cost.
- **Finance & Loans**: Find loan estimates and discover zero-collateral, AI-optimized offers from banking partners.
- **Chatbot (EduMentor AI)**: A dynamic modal to answer direct queries regarding loans, universities, and application health.

## 🤝 Contributing
Contributions are welcome. Please open an issue first to discuss what you would like to change.

## 📄 License
ISC License