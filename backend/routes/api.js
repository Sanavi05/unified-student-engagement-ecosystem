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

export default router;
