<template>
  <div class="dashboard">
    <header class="section-header">
      <h2>Welcome back, Student!</h2>
      <p>Here's your personalized higher education breakdown.</p>
    </header>

    <div class="stats-grid">
      <div class="stat-card card">
        <div class="stat-icon" style="background-color: var(--primary-color)">P</div>
        <div class="stat-info">
          <h3>Profile Completion</h3>
          <p class="value">80%</p>
        </div>
      </div>
      <div class="stat-card card">
        <div class="stat-icon" style="background-color: var(--secondary-color)">M</div>
        <div class="stat-info">
          <h3>Top Match</h3>
          <p class="value">Stanford Univ</p>
        </div>
      </div>
      <div class="stat-card card">
        <div class="stat-icon" style="background-color: #f59e0b">A</div>
        <div class="stat-info">
          <h3>Activity Streak</h3>
          <p class="value">12 Days</p>
        </div>
      </div>
    </div>

    <!-- AI Insights Panel -->
    <div class="ai-insights card mt-2">
      <h3>AI Insights & Nudges</h3>
      <ul class="insight-list">
        <li class="insight-item">
          <span class="dot primary"></span>
          <div>
            <strong>Great news!</strong> You have a 75% admission chance based on your latest mock test scores. You should improve your SOP to reach 85%.
          </div>
        </li>
        <li class="insight-item">
          <span class="dot warning"></span>
          <div>
            <strong>Action Required:</strong> Fall intake applications for your top choices close in 45 days. Complete your profile to generate a timeline.
          </div>
        </li>
        <li class="insight-item">
          <span class="dot secondary"></span>
          <div>
            <strong>Finance Alert:</strong> A new low-interest education loan from HDFC Credila has been unlocked for your tier. Check the Finance section.
          </div>
        </li>
      </ul>
      <button class="btn-primary mt-1" @click="generateTimeline">Generate Application Timeline</button>
    </div>

    <!-- Generated Timeline Display -->
    <div v-if="timeline.length" class="timeline-section card mt-2">
      <h3>📅 Your Application Timeline</h3>
      <div class="timeline-container">
        <div v-for="(item, index) in timeline" :key="index" class="timeline-item">
          <div class="timeline-marker" :style="{ backgroundColor: getColor(index) }">
            {{ index + 1 }}
          </div>
          <div class="timeline-content">
            <h4>{{ item.month }}</h4>
            <p>{{ item.task }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const apiBase = 'http://localhost:3000/api';
const timeline = ref([]);

const generateTimeline = async () => {
  try {
    const userProfile = {
      gpa: 8.5,
      country: 'us'
    };
    const res = await axios.post(`${apiBase}/ai/timeline`, userProfile);
    timeline.value = res.data.timeline;
    console.log('Generated Timeline:', timeline.value);
  } catch (err) {
    console.error(err);
    alert('Failed to generate timeline. Ensure backend and AI services are running.');
  }
};

const getColor = (index) => {
  const colors = ['#6366f1', '#f59e0b', '#ef4444', '#10b981', '#3b82f6'];
  return colors[index % colors.length];
};
</script>

<style scoped>
.dashboard {
  animation: fadeIn 0.5s ease;
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.stat-info h3 {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.stat-info p.value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}

.ai-insights {
  background: var(--surface-color);
  border-left: 4px solid var(--primary-color);
}

.ai-insights h3 {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.insight-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.insight-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  padding: 1rem;
  background-color: var(--bg-color);
  border-radius: 8px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 5px;
  flex-shrink: 0;
}

.dot.primary { background-color: var(--primary-color); }
.dot.warning { background-color: #f59e0b; }
.dot.secondary { background-color: var(--secondary-color); }

.mt-1 { margin-top: 1rem; }
.mt-2 { margin-top: 2rem; }

/* Timeline Styles */
.timeline-section {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(59, 130, 246, 0.05) 100%);
  border-left: 4px solid var(--primary-color);
}

.timeline-section h3 {
  margin-bottom: 2rem;
  font-size: 1.25rem;
}

.timeline-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding-left: 2rem;
  position: relative;
}

.timeline-container::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, var(--primary-color), var(--secondary-color));
  opacity: 0.3;
}

.timeline-item {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
  position: relative;
}

.timeline-marker {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 0.875rem;
  flex-shrink: 0;
  margin-top: 0.25rem;
  margin-left: -2.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.timeline-content {
  flex: 1;
  padding: 1rem;
  background-color: var(--bg-color);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.timeline-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: var(--text-primary);
}

.timeline-content p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
