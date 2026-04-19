import express from 'express';
import { User } from '../models/User.js';
import axios from 'axios';

const router = express.Router();

// Mock Auth - Return a fixed user
router.get('/user/profile', async (req, res) => {
  try {
    let user = await User.findOne({ email: 'student@edupath.ai' });
    if (!user) {
      user = await User.create({
        name: 'Student',
        email: 'student@edupath.ai',
        gpa: 8.5,
        preferredCountry: 'us',
        familyIncome: 1500000
      });
    }
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: 'Database error' });
  }
});

// Proxy route to FastAPI for AI Recommendations
router.post('/ai/recommend', async (req, res) => {
  try {
    const aiResponse = await axios.post(`${process.env.FASTAPI_URL}/recommend`, req.body);
    res.json(aiResponse.data);
  } catch (error) {
    console.error('FastAPI error:', error.message);
    res.status(500).json({ error: 'AI service unavailable' });
  }
});

// Proxy route for Admission Chances
router.post('/ai/predict-admission', async (req, res) => {
  try {
    const aiResponse = await axios.post(`${process.env.FASTAPI_URL}/predict-admission`, req.body);
    res.json(aiResponse.data);
  } catch (error) {
    console.error('FastAPI error:', error.message);
    res.status(500).json({ error: 'AI service unavailable' });
  }
});

// Proxy route to FastAPI for Timeline Generation
router.post('/ai/timeline', async (req, res) => {
  try {
    const userProfile = {
      gpa: req.body.gpa || 8.5,
      country: req.body.country || 'us',
      testScore: req.body.testScore || 300
    };
    // Using the generate_timeline endpoint if available, otherwise use mock
    const timeline = [
      { month: "Month 1", task: "Shortlist Universities and prepare for GRE/GMAT." },
      { month: "Month 2", task: "Write first draft of Statement of Purpose (SOP)." },
      { month: "Month 3", task: "Finalize Letters of Recommendation (LORs) and submit applications." },
      { month: "Month 4", task: "Apply for Education Loans based on admits." },
      { month: "Month 5", task: "Visa interview preparation and mock interviews." }
    ];
    res.json({ timeline });
  } catch (error) {
    console.error('Timeline generation error:', error.message);
    res.status(500).json({ error: 'Timeline generation failed' });
  }
});

// Proxy route for Loan Eligibility Check
router.post('/finance/eligibility', async (req, res) => {
  try {
    const aiResponse = await axios.post(`${process.env.FASTAPI_URL}/finance/eligibility`, req.body);
    res.json(aiResponse.data);
  } catch (error) {
    console.error('FastAPI finance eligibility error:', error.message);
    res.status(500).json({ error: 'AI eligibility service unavailable' });
  }
});

// Proxy route for Loan Offer Advice
router.post('/finance/loan-advice', async (req, res) => {
  try {
    const aiResponse = await axios.post(`${process.env.FASTAPI_URL}/finance/loan-advice`, req.body);
    res.json(aiResponse.data);
  } catch (error) {
    console.error('FastAPI loan advice error:', error.message);
    res.status(500).json({ error: 'AI loan advice service unavailable' });
  }
});

// Proxy route for Chatbot (Gemini)
router.post('/chat', async (req, res) => {
  try {
    const aiResponse = await axios.post(`${process.env.FASTAPI_URL}/chat`, req.body);
    res.json(aiResponse.data);
  } catch (error) {
    console.error('FastAPI chat error:', error.message);
    res.status(500).json({ error: 'Chat service unavailable' });
  }
});

export default router;
