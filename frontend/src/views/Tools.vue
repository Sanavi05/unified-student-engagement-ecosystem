<template>
  <div class="tools-page">
    <header class="section-header">
      <h2>AI Engagement Tools</h2>
      <p>Discover courses, predict admissions, and calculate your return on investment.</p>
    </header>

    <div class="tools-grid">
      <!-- AI Career Navigator -->
      <div class="tool-card card">
        <div class="tool-header">
          <div class="tool-icon">N</div>
          <h3>AI Career Navigator</h3>
        </div>
        <p class="tool-desc">Enter your profile to get personalized university and course recommendations.</p>
        
        <form class="tool-form" @submit.prevent="navigateCareer">
          <div class="form-group">
            <label>Current GPA (out of 10)</label>
            <input type="number" step="0.1" v-model="careerForm.gpa" placeholder="e.g. 8.5" required />
          </div>
          <div class="form-group">
            <label>Preferred Country</label>
            <select v-model="careerForm.country" required>
              <option value="">Select...</option>
              <option value="us">United States</option>
              <option value="uk">United Kingdom</option>
              <option value="ca">Canada</option>
              <option value="au">Australia</option>
            </select>
          </div>
          <button type="submit" class="btn-primary w-100" :disabled="loadingCareer">
            {{ loadingCareer ? 'Analyzing...' : 'Get Recommendations' }}
          </button>
        </form>

        <div v-if="recommendations.length" class="mock-result mt-1">
          <h4 style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.5rem;">Top Matches:</h4>
          <ul style="padding-left: 1.5rem; color: var(--primary-color); font-weight: 600;">
            <li v-for="uni in recommendations" :key="uni">{{ uni }}</li>
          </ul>
        </div>
      </div>

      <!-- Admission Probability Predictor -->
      <div class="tool-card card">
        <div class="tool-header">
          <div class="tool-icon">P</div>
          <h3>Admission Predictor</h3>
        </div>
        <p class="tool-desc">Check your chances of getting into your dream university.</p>
        
        <form class="tool-form" @submit.prevent="predictAdmission">
          <div class="form-group">
            <label>Target University</label>
            <input type="text" v-model="admissionForm.targetUniversity" placeholder="e.g. MIT, Stanford" required />
          </div>
          <div class="form-group">
            <label>Test Score (GRE/GMAT limit 340)</label>
            <input type="number" v-model="admissionForm.testScore" placeholder="Enter score" required />
          </div>
          <button type="submit" class="btn-primary w-100 secondary-btn" :disabled="loadingAdmission">
            {{ loadingAdmission ? 'Predicting...' : 'Predict Chances' }}
          </button>
        </form>
        
        <!-- Mock Result -->
        <div class="mock-result mt-1" v-if="admissionResult">
          <div class="progress-bar">
            <div class="progress" :style="`width: ${admissionResult.probability}`"></div>
          </div>
          <p class="text-center">{{ admissionResult.probability }} Probability</p>
        </div>
      </div>

      <!-- ROI Calculator -->
      <div class="tool-card card">
        <div class="tool-header">
          <div class="tool-icon">C</div>
          <h3>ROI Calculator</h3>
        </div>
        <p class="tool-desc">Estimate your post-graduation salary and payback period.</p>
        
        <form class="tool-form" @submit.prevent="calculateROI">
          <div class="form-group">
            <label>Course Cost (USD)</label>
            <input type="number" v-model="roiForm.cost" placeholder="e.g. 50000" required />
          </div>
          <button type="submit" class="btn-primary w-100">Calculate ROI</button>
        </form>

        <div v-if="roiResult" class="mock-result mt-1 text-center" style="color: var(--primary-color);">
          <p>Estimated Payback: <strong>{{ roiResult }} Years</strong></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const apiBase = 'http://localhost:3000/api';

// Career Navigator State
const careerForm = ref({ gpa: null, country: '' });
const loadingCareer = ref(false);
const recommendations = ref([]);

const navigateCareer = async () => {
  loadingCareer.value = true;
  try {
    const res = await axios.post(`${apiBase}/ai/recommend`, careerForm.value);
    recommendations.value = res.data.recommendations;
  } catch (err) {
    console.error(err);
    alert('Failed to connect to AI Engine. Ensure Node and FastAPI servers are running.');
  } finally {
    loadingCareer.value = false;
  }
};

// Admission Predictor State
const admissionForm = ref({ targetUniversity: '', testScore: null });
const loadingAdmission = ref(false);
const admissionResult = ref(null);

const predictAdmission = async () => {
  loadingAdmission.value = true;
  try {
    const res = await axios.post(`${apiBase}/ai/predict-admission`, admissionForm.value);
    admissionResult.value = res.data;
  } catch (err) {
    console.error(err);
    alert('Failed to connect to AI Engine. Ensure Node and FastAPI servers are running.');
  } finally {
    loadingAdmission.value = false;
  }
};

// ROI State
const roiForm = ref({ cost: null });
const roiResult = ref(null);

const calculateROI = () => {
  if (roiForm.value.cost) {
    // Simple mock logic directly in frontend for instant feedback
    const baseSalary = 80000;
    const payback = (roiForm.value.cost / (baseSalary * 0.3)).toFixed(1);
    roiResult.value = payback;
  }
};
</script>

<style scoped>
.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.tool-card {
  display: flex;
  flex-direction: column;
}

.tool-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.tool-icon {
  font-size: 2rem;
  background: rgba(99, 102, 241, 0.1);
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.tool-desc {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.tool-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: auto;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--bg-color);
  color: var(--text-primary);
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

.w-100 { width: 100%; }
.mt-1 { margin-top: 1rem; }
.text-center { text-align: center; margin-top: 0.5rem; font-weight: 600; color: var(--primary-color); }

.secondary-btn {
  background-color: var(--secondary-color);
}
.secondary-btn:hover {
  background-color: #0d9488;
}

.progress-bar {
  height: 8px;
  background-color: var(--border-color);
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: var(--secondary-color);
  transition: width 1s ease;
}
</style>
