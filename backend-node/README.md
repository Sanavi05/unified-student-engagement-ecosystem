# Backend Node.js Server

This is the Express.js backend API for the Unified Student Engagement Ecosystem.

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create `.env` file from `.env.example` and configure your MongoDB URI, Python service port, etc.

3. Start the server:
   ```bash
   npm run dev
   ```

## API Endpoints

### POST `/api/chat`
- **Description**: Accept user messages, update StudentProfile, forward to Python AI service
- **Request Body**:
  ```json
  {
    "userId": "string",
    "message": "string",
    "demographics": {
      "targetCountry": "string",
      "targetCourse": "string",
      "currentCGPA": number
    }
  }
  ```
- **Response**: Chat history and initial AI response

### GET `/api/dashboard/:userId`
- **Description**: Fetch populated StudentProfile for ROI dashboard
- **Response**: Profile with demographics, financials, engagement state

### POST `/api/webhook/ai-update`
- **Description**: Receives updates from Python AI service (webhook callback)
- **Request Body**:
  ```json
  {
    "userId": "string",
    "aiMessage": "string",
    "extractedData": {
      "targetCourse": "string",
      "targetCountry": "string",
      "currentCGPA": number
    },
    "financialUpdate": {
      "estimatedCourseCost": number,
      "userBudget": number
    }
  }
  ```

### GET `/health`
- **Description**: Health check endpoint

## Environment Variables

See `.env.example` in the root directory.
