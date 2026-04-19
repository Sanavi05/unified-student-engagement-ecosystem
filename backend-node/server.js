require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const StudentProfile = require('./models/StudentProfile');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB Connection
mongoose
  .connect(process.env.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log('✓ MongoDB connected'))
  .catch((err) => console.error('MongoDB connection error:', err));

// Routes

/**
 * POST /api/chat
 * Accepts user message, updates StudentProfile, forwards to Python AI service
 */
app.post('/api/chat', async (req, res) => {
  try {
    const { userId, message, demographics } = req.body;

    if (!userId || !message) {
      return res.status(400).json({ error: 'userId and message are required' });
    }

    // Find or create student profile
    let student = await StudentProfile.findOne({ userId });

    if (!student) {
      student = new StudentProfile({
        userId,
        demographics: demographics || {},
        engagementState: {
          copilotChatHistory: [],
        },
      });
    }

    // Add user message to chat history
    student.engagementState.copilotChatHistory.push({
      role: 'user',
      message,
      timestamp: new Date(),
    });

    // Save to MongoDB
    await student.save();

    // Forward to Python AI service
    try {
      const pythonResponse = await axios.post(
        `http://127.0.0.1:${process.env.PYTHON_PORT}/process-chat`,
        {
          userId,
          message,
          demographics: student.demographics,
          chatHistory: student.engagementState.copilotChatHistory,
        },
        { timeout: 60000 } // Increased timeout to 60 seconds
      );

      // If we got a task ID, wait for it to complete
      const taskId = pythonResponse.data.taskId;
      if (taskId) {
        // Poll for task completion (max 50 seconds)
        let taskComplete = false;
        let attempts = 0;
        const maxAttempts = 50;

        while (!taskComplete && attempts < maxAttempts) {
          try {
            const taskStatus = await axios.get(
              `http://127.0.0.1:${process.env.PYTHON_PORT}/task-status/${taskId}`,
              { timeout: 5000 }
            );

            if (taskStatus.data.status === 'SUCCESS') {
              taskComplete = true;
              // Fetch updated profile from MongoDB (webhook should have updated it)
              const updatedStudent = await StudentProfile.findOne({ userId });
              if (updatedStudent) {
                return res.status(200).json({
                  success: true,
                  studentId: updatedStudent._id,
                  chatHistory: updatedStudent.engagementState.copilotChatHistory,
                  profile: {
                    demographics: updatedStudent.demographics,
                    financials: updatedStudent.financials,
                  },
                });
              }
            } else if (taskStatus.data.status === 'FAILURE') {
              throw new Error('Celery task failed');
            }
          } catch (taskError) {
            // Ignore status check errors and retry
          }

          await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait 1 second before retry
          attempts++;
        }

        // If task didn't complete, return current state
        if (!taskComplete) {
          const currentStudent = await StudentProfile.findOne({ userId });
          return res.status(200).json({
            success: true,
            studentId: student._id,
            chatHistory: student.engagementState.copilotChatHistory,
            profile: currentStudent
              ? {
                  demographics: currentStudent.demographics,
                  financials: currentStudent.financials,
                }
              : {},
            message: 'Processing AI response...',
          });
        }
      }

      return res.status(200).json({
        success: true,
        studentId: student._id,
        chatHistory: student.engagementState.copilotChatHistory,
        aiResponse: pythonResponse.data,
      });
    } catch (pythonError) {
      console.error('Error calling Python service:', pythonError.message);
      return res.status(500).json({
        success: false,
        error: 'AI service temporarily unavailable',
        message:
          "We couldn't process your request. Please try again in a moment.",
      });
    }
  } catch (error) {
    console.error('Chat endpoint error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
    });
  }
});

/**
 * GET /api/dashboard/:userId
 * Fetches the populated StudentProfile for ROI dashboard
 */
app.get('/api/dashboard/:userId', async (req, res) => {
  try {
    const { userId } = req.params;

    const student = await StudentProfile.findOne({ userId });

    if (!student) {
      return res.status(404).json({
        success: false,
        error: 'Student profile not found',
      });
    }

    res.status(200).json({
      success: true,
      profile: {
        userId: student.userId,
        demographics: student.demographics,
        financials: student.financials,
        engagementState: {
          roiDashboardGenerated: student.engagementState.roiDashboardGenerated,
          loanPreQualified: student.engagementState.loanPreQualified,
          chatHistoryCount: student.engagementState.copilotChatHistory.length,
        },
      },
    });
  } catch (error) {
    console.error('Dashboard endpoint error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
    });
  }
});

/**
 * POST /api/webhook/ai-update
 * Receives updates from Python service after Gemini processing
 */
app.post('/api/webhook/ai-update', async (req, res) => {
  try {
    const {
      userId,
      aiMessage,
      extractedData,
      financialUpdate,
    } = req.body;

    if (!userId) {
      return res.status(400).json({ error: 'userId is required' });
    }

    const student = await StudentProfile.findOne({ userId });

    if (!student) {
      return res.status(404).json({ error: 'Student profile not found' });
    }

    // Add AI response to chat history
    if (aiMessage) {
      student.engagementState.copilotChatHistory.push({
        role: 'assistant',
        message: aiMessage,
        timestamp: new Date(),
      });
    }

    // Update demographics if extracted data available
    if (extractedData) {
      if (extractedData.targetCourse) {
        student.demographics.targetCourse = extractedData.targetCourse;
      }
      if (extractedData.targetCountry) {
        student.demographics.targetCountry = extractedData.targetCountry;
      }
      if (extractedData.currentCGPA) {
        student.demographics.currentCGPA = extractedData.currentCGPA;
      }
    }

    // Update financials if provided
    if (financialUpdate) {
      if (financialUpdate.estimatedCourseCost) {
        student.financials.estimatedCourseCost =
          financialUpdate.estimatedCourseCost;
      }
      if (financialUpdate.userBudget) {
        student.financials.userBudget = financialUpdate.userBudget;
      }
      // Calculate funding gap
      student.financials.fundingGap =
        student.financials.estimatedCourseCost -
        student.financials.userBudget;
      if (student.financials.fundingGap < 0) {
        student.financials.fundingGap = 0;
      }

      student.engagementState.roiDashboardGenerated = true;
    }

    await student.save();

    res.status(200).json({
      success: true,
      message: 'Profile updated successfully',
      profile: student,
    });
  } catch (error) {
    console.error('Webhook endpoint error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'Backend API is running' });
});

// Start server
const PORT = process.env.NODE_PORT || 5000;
app.listen(PORT, '127.0.0.1', () => {
  console.log(`✓ Backend API running on http://localhost:${PORT}`);
  console.log(
    `✓ Forwarding to Python service on http://localhost:${process.env.PYTHON_PORT || 8000}`
  );
});
