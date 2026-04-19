<template>
  <div class="finance-page">
    <header class="section-header">
      <h2>Education Finance & Loans</h2>
      <p>Discover your loan eligibility and plan your repayment with ease.</p>
    </header>

    <div class="finance-grid">
      <!-- Loan Eligibility Estimator -->
      <div class="finance-card card eligibility">
        <div class="card-header">
          <h3>Loan Eligibility Estimator</h3>
        </div>
        <form class="finance-form">
          <div class="form-row">
            <div class="form-group">
              <label>Family Income (Annual)</label>
              <input type="number" v-model="eligibilityForm.income" placeholder="e.g. 1500000" />
            </div>
            <div class="form-group">
              <label>Co-applicant Status</label>
              <select v-model="eligibilityForm.coApplicant">
                <option>Salaried</option>
                <option>Self-Employed</option>
                <option>None</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>University Tier</label>
            <select v-model="eligibilityForm.universityTier">
              <option>Tier 1 (Ivy League, Top 50)</option>
              <option>Tier 2 (Top 200)</option>
              <option>Tier 3 (Others)</option>
            </select>
          </div>
          <button type="button" class="btn-primary w-100" @click="checkEligibility" :disabled="loadingEligibility">
            {{ loadingEligibility ? 'Analyzing with AI...' : 'Check Eligibility' }}
          </button>
        </form>

        <!-- AI Eligibility Result -->
        <div v-if="eligibilityResult" class="ai-result mt-1">
          <div class="eligibility-score">
            <div class="score-badge" :class="eligibilityResult.eligible ? 'eligible' : 'not-eligible'">
              {{ eligibilityResult.eligible ? '✓ Eligible' : '✗ Not Eligible' }}
            </div>
            <div class="score-details">
              <span class="score-label">Score</span>
              <span class="score-value">{{ eligibilityResult.eligibilityScore }}</span>
            </div>
            <div class="score-details">
              <span class="score-label">Max Loan</span>
              <span class="score-value">{{ eligibilityResult.maxLoanAmount }}</span>
            </div>
          </div>
          <p class="ai-summary">{{ eligibilityResult.summary }}</p>
          <ul class="ai-tips">
            <li v-for="tip in eligibilityResult.tips" :key="tip">{{ tip }}</li>
          </ul>
        </div>
      </div>

      <!-- EMI Calculator -->
      <div class="finance-card card emi">
        <div class="card-header">
          <h3>EMI Calculator</h3>
        </div>
        <div class="emi-result">
          <div class="emi-amount">₹{{ emiAmount.toLocaleString('en-IN') }} <span class="muted">/mo</span></div>
          <p class="muted-small">Estimated EMI for ₹{{ loanAmount.toLocaleString('en-IN') }} @ {{ interestRate }}% for {{ loanTenure }} Years</p>
        </div>
        <div class="slider-group mt-1">
          <label>Loan Amount: ₹{{ loanAmount.toLocaleString('en-IN') }}</label>
          <input type="range" min="100000" max="10000000" v-model="loanAmount" class="slider" @change="calculateEMI" />
        </div>
      </div>

      <div class="finance-card card offers" style="grid-column: 1 / -1;">
        <div class="card-header">
          <h3>Customized Loan Offers</h3>
          <span class="badge new">New</span>
        </div>
        <div class="offers-list">
          <!-- Offer 1 -->
          <div class="offer-item">
            <div class="bank-info">
              <div class="bank-logo hdfc">H</div>
              <div>
                <strong>HDFC Credila</strong>
                <p class="muted-small">No collateral for Tier 1</p>
              </div>
            </div>
            <div class="offer-details">
              <div class="detail">
                <span class="label">Interest</span>
                <span class="value">10.25%</span>
              </div>
              <div class="detail">
                <span class="label">Processing Fee</span>
                <span class="value">1%</span>
              </div>
            </div>
            <button class="btn-outline" @click="applyWithAI('HDFC Credila')" :disabled="loadingAdvice === 'HDFC Credila'">
              {{ loadingAdvice === 'HDFC Credila' ? 'Fetching...' : 'Apply with AI' }}
            </button>
          </div>

          <!-- Offer 2 -->
          <div class="offer-item">
            <div class="bank-info">
              <div class="bank-logo sbi">S</div>
              <div>
                <strong>SBI Global Ed-Vantage</strong>
                <p class="muted-small">Govt. subsidized rates</p>
              </div>
            </div>
            <div class="offer-details">
              <div class="detail">
                <span class="label">Interest</span>
                <span class="value">9.15%</span>
              </div>
              <div class="detail">
                <span class="label">Processing Fee</span>
                <span class="value">₹10,000</span>
              </div>
            </div>
            <button class="btn-outline" @click="applyWithAI('SBI Global Ed-Vantage')" :disabled="loadingAdvice === 'SBI Global Ed-Vantage'">
              {{ loadingAdvice === 'SBI Global Ed-Vantage' ? 'Fetching...' : 'Apply with AI' }}
            </button>
          </div>

          <!-- AI Loan Advice Result -->
          <div v-if="loanAdvice" class="loan-advice-result">
            <div class="advice-header">
              <span class="advice-bank">AI Advice for {{ loanAdvice.bank }}</span>
              <span class="advice-time">⏱ {{ loanAdvice.estimatedApprovalTime }}</span>
            </div>
            <p class="advice-text">{{ loanAdvice.recommendation }}</p>
            <div class="advice-docs">
              <span class="docs-label">📄 Documents needed:</span>
              <span v-for="doc in loanAdvice.requiredDocuments" :key="doc" class="doc-chip">{{ doc }}</span>
            </div>
            <div class="advice-tip">💡 {{ loanAdvice.tip }}</div>
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

// EMI Calculator State
const loanAmount = ref(3000000);
const emiAmount = ref(42500);
const interestRate = ref(10.5);
const loanTenure = ref(10);

// Calculate EMI using formula: P * [r(1+r)^n] / [(1+r)^n - 1]
const calculateEMI = () => {
  const principal = parseFloat(loanAmount.value);
  const monthlyRate = interestRate.value / 100 / 12;
  const numberOfMonths = loanTenure.value * 12;
  
  if (monthlyRate === 0) {
    emiAmount.value = principal / numberOfMonths;
  } else {
    const emi = (principal * (monthlyRate * Math.pow(1 + monthlyRate, numberOfMonths))) / 
                (Math.pow(1 + monthlyRate, numberOfMonths) - 1);
    emiAmount.value = Math.round(emi);
  }
};

// Loan Eligibility State
const eligibilityForm = ref({
  income: null,
  coApplicant: 'Salaried',
  universityTier: 'Tier 1 (Ivy League, Top 50)'
});
const loadingEligibility = ref(false);
const eligibilityResult = ref(null);

const checkEligibility = async () => {
  if (!eligibilityForm.value.income) {
    alert('Please enter your family income.');
    return;
  }
  loadingEligibility.value = true;
  eligibilityResult.value = null;
  try {
    const res = await axios.post(`${apiBase}/finance/eligibility`, {
      income: parseFloat(eligibilityForm.value.income),
      coApplicant: eligibilityForm.value.coApplicant,
      universityTier: eligibilityForm.value.universityTier
    });
    eligibilityResult.value = res.data;
  } catch (err) {
    console.error(err);
    alert('Failed to connect to AI service. Make sure all servers are running.');
  } finally {
    loadingEligibility.value = false;
  }
};

// Loan Advice State
const loadingAdvice = ref(null);
const loanAdvice = ref(null);

const applyWithAI = async (bankName) => {
  loadingAdvice.value = bankName;
  loanAdvice.value = null;
  try {
    const res = await axios.post(`${apiBase}/finance/loan-advice`, {
      bankName,
      income: parseFloat(eligibilityForm.value.income) || 1500000,
      universityTier: eligibilityForm.value.universityTier
    });
    loanAdvice.value = res.data;
  } catch (err) {
    console.error(err);
    alert('Failed to get loan advice. Make sure all servers are running.');
  } finally {
    loadingAdvice.value = null;
  }
};
</script>

<style scoped>

.form-row {
  display: flex;
  gap: 1rem;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.form-group label {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--bg-color);
  color: var(--text-primary);
}

.emi-result {
  background: rgba(99, 102, 241, 0.05);
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  border: 1px dashed var(--primary-color);
}

.emi-amount {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.muted { font-size: 1rem; color: var(--text-secondary); font-weight: normal; }
.muted-small { font-size: 0.8rem; color: var(--text-secondary); }

.slider-group {
  margin-top: 2rem;
}

.slider {
  width: 100%;
  margin-top: 0.5rem;
}

.offers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.offer-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background-color: var(--bg-color);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.bank-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 2;
}

.bank-logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
}

.hdfc { background-color: #004c8f; }
.sbi { background-color: #0077b5; }

.offer-details {
  display: flex;
  gap: 2rem;
  flex: 2;
}

.detail {
  display: flex;
  flex-direction: column;
}

.detail .label { font-size: 0.75rem; color: var(--text-secondary); }
.detail .value { font-weight: 600; }

.btn-outline {
  background: transparent;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.btn-outline:hover {
  background: var(--primary-color);
  color: white;
}

.badge.new {
  background-color: #ef4444;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
}

.w-100 { width: 100%; }
.mt-1 { margin-top: 1rem; }

/* AI Result Styles */
.ai-result {
  border-top: 1px solid var(--border-color);
  padding-top: 1rem;
  animation: fadeIn 0.4s ease;
}

.eligibility-score {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
}

.score-badge {
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.9rem;
}
.score-badge.eligible { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.score-badge.not-eligible { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

.score-details {
  display: flex;
  flex-direction: column;
}
.score-label { font-size: 0.75rem; color: var(--text-secondary); }
.score-value { font-weight: 700; color: var(--primary-color); }

.ai-summary {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.ai-tips {
  padding-left: 1.25rem;
  margin: 0;
  font-size: 0.82rem;
  color: var(--text-secondary);
}
.ai-tips li { margin-bottom: 0.25rem; }

/* Loan Advice Result */
.loan-advice-result {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 10px;
  background: rgba(99, 102, 241, 0.05);
  border: 1px solid rgba(99, 102, 241, 0.2);
  animation: fadeIn 0.4s ease;
}

.advice-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.6rem;
}
.advice-bank { font-weight: 700; color: var(--primary-color); }
.advice-time { font-size: 0.8rem; color: var(--text-secondary); }

.advice-text {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.advice-docs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  align-items: center;
  margin-bottom: 0.75rem;
}
.docs-label { font-size: 0.8rem; color: var(--text-secondary); }
.doc-chip {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  font-size: 0.75rem;
  color: var(--text-primary);
}

.advice-tip {
  font-size: 0.82rem;
  color: var(--secondary-color);
  font-style: italic;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
