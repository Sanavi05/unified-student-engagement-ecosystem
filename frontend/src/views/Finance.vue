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
              <input type="number" placeholder="e.g. 1500000" />
            </div>
            <div class="form-group">
              <label>Co-applicant Status</label>
              <select>
                <option>Salaried</option>
                <option>Self-Employed</option>
                <option>None</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>University Tier</label>
            <select>
              <option>Tier 1 (Ivy League, Top 50)</option>
              <option>Tier 2 (Top 200)</option>
              <option>Tier 3 (Others)</option>
            </select>
          </div>
          <button type="button" class="btn-primary w-100" @click="checkEligibility">Check Eligibility</button>
        </form>
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

      <!-- Dynamic Loan Offers -->
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
            <button class="btn-outline">Apply with AI</button>
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
            <button class="btn-outline" @click="applyWithAI('SBI Global Ed-Vantage')">Apply with AI</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

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

const checkEligibility = () => {
  alert('✅ Eligibility check initiated!\n\nBased on your profile:\n- Annual Income: Good\n- Co-applicant: Yes\n- University Tier: Tier 1\n\nYou are eligible for up to 50 Lakhs (+50% with co-applicant)');
};

const applyWithAI = (bankName) => {
  alert(`🎉 Redirecting to ${bankName} application form...\n\nOur AI will help fill your details automatically!`);
  console.log(`Applying with ${bankName}`);
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
</style>
