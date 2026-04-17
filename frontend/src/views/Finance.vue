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
          <button type="button" class="btn-primary w-100">Check Eligibility</button>
        </form>
      </div>

      <!-- EMI Calculator -->
      <div class="finance-card card emi">
        <div class="card-header">
          <h3>EMI Calculator</h3>
        </div>
        <div class="emi-result">
          <div class="emi-amount">₹42,500 <span class="muted">/mo</span></div>
          <p class="muted-small">Estimated EMI for ₹30 Lakhs @ 10.5% for 10 Years</p>
        </div>
        <div class="slider-group mt-1">
          <label>Loan Amount: ₹30,00,000</label>
          <input type="range" min="100000" max="10000000" value="3000000" class="slider" />
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
            <button class="btn-outline">Apply with AI</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.finance-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.finance-card {
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
}

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
