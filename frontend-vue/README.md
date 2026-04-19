# Student Engagement Ecosystem

Modern, responsive frontend built with Vue 3 (Composition API), Vite, and TailwindCSS.

## Features

- ✅ **ChatWidget.vue** - Real-time AI chat with Study Abroad Copilot
- ✅ **ROIDashboard.vue** - Interactive ROI financial dashboard with:
  - Course cost visualization
  - Budget tracking with progress bars
  - Dynamic funding gap calculation
  - Zero-touch loan pre-qualification
- ✅ **Responsive Design** - Mobile-first with TailwindCSS
- ✅ **Real-time Profile Sync** - Auto-updates from backend
- ✅ **Professional UI** - Gradient backgrounds, smooth animations

## Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
Create a `.env` file with backend API endpoint (optional - defaults to proxy):
```bash
VITE_API_URL=http://localhost:5000
```

### 3. Start Development Server
```bash
npm run dev
```
App runs on http://localhost:3000 with automatic hot reload.

### 4. Build for Production
```bash
npm run build
npm run preview
```

## Project Structure

```
frontend-vue/
├── src/
│   ├── components/
│   │   ├── ChatWidget.vue       # AI chat interface
│   │   └── ROIDashboard.vue     # Financial dashboard
│   ├── App.vue                  # Root component
│   ├── main.js                  # Entry point
│   └── style.css                # TailwindCSS imports
├── index.html                   # HTML template
├── vite.config.js               # Vite configuration
├── tailwind.config.js           # TailwindCSS config
├── postcss.config.js            # PostCSS config
└── package.json                 # Dependencies
```

## Key Components

### ChatWidget
- Accepts user messages about study abroad plans
- Sends to backend `/api/chat` endpoint
- Displays AI responses from Gemini
- Real-time chat history
- Auto-detects when backend is unavailable

### ROIDashboard
- Displays extracted financial data:
  - **Estimated Course Cost** - Visual progress bar
  - **Your Budget** - Visual progress bar
  - **Funding Gap** - Calculated difference (if > $0)
- Shows student demographics (course, country, CGPA)
- **"Apply for Loan"** button:
  - Only appears when fundingGap > 0
  - Requires `roiDashboardGenerated = true` flag
  - Triggers mock success alert with zero-touch auto-fill message
- Displays reasons to apply (rates, flexibility, etc.)

## API Integration

### Backend Endpoints Used:
- **POST `/api/chat`** - Send chat message
- **GET `/api/dashboard/:userId`** - Fetch student profile

### Proxy Configuration:
Vite forwards `/api/*` requests to `http://localhost:5000` (configurable in `vite.config.js`)

## Data Flow

1. User types message in ChatWidget
2. Message sent to `/api/chat` endpoint
3. Node backend updates MongoDB
4. Node triggers Python AI service
5. Gemini processes and returns structured JSON
6. Backend webhooks back with extracted data
7. Frontend fetches updated profile via `/api/dashboard`
8. ROIDashboard re-renders with new financials
9. "Apply for Loan" button shows if fundingGap > 0

## Styling

- **TailwindCSS** - Utility-first CSS framework
- **Custom Classes** - Message styles, buttons, progress bars
- **Responsive Grid** - 2 columns (chat + dashboard) on desktop, stacked on mobile
- **Gradient Header** - Blue to indigo gradient background

## Technologies

- Vue 3.3 (Composition API)
- Vite 4.4 (Lightning-fast bundler)
- TailwindCSS 3.3 (Utility CSS)
- PostCSS + Autoprefixer (CSS processing)
- Axios (HTTP client)

## Troubleshooting

### Backend not responding?
- Ensure Node.js backend is running on port 5000
- Check that MongoDB is connected
- See backend README for setup

### Chat messages not appearing?
- Open browser console for errors
- Check network tab to see `/api/chat` request
- Verify backend is forwarding to Python service

### Loan button not showing?
- Ensure Python AI service is running
- Chat with the Copilot about course costs and budget
- Wait for AI to extract financial data
- Dashboard needs `roiDashboardGenerated = true` flag

## Development Tips

- Hot reload enabled with Vite
- Use Vue DevTools browser extension for debugging
- Check browser console for error messages
- Network tab shows all API requests/responses
- TailwindCSS IntelliSense extension recommended
