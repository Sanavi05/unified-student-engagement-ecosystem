<template>
  <div class="bg-white rounded-lg shadow-lg p-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">
      📊 ROI Dashboard
    </h2>

    <!-- Financials Display -->
    <div v-if="profile.financials" class="space-y-6">
      <!-- Estimated Course Cost -->
      <div>
        <div class="flex justify-between items-center mb-2">
          <label class="font-semibold text-gray-700">Estimated Course Cost</label>
          <span class="text-lg font-bold text-blue-600">
            ${{ formatCurrency(profile.financials.estimatedCourseCost) }}
          </span>
        </div>
        <div class="progress-bar">
          <div
            class="progress-bar-fill"
            :style="{
              width: costProgressPercent + '%',
            }"
          ></div>
        </div>
      </div>

      <!-- User Budget -->
      <div>
        <div class="flex justify-between items-center mb-2">
          <label class="font-semibold text-gray-700">Your Budget</label>
          <span class="text-lg font-bold text-green-600">
            ${{ formatCurrency(profile.financials.userBudget) }}
          </span>
        </div>
        <div class="progress-bar">
          <div
            class="progress-bar-fill bg-green-500"
            :style="{
              width: budgetProgressPercent + '%',
            }"
          ></div>
        </div>
      </div>

      <!-- Funding Gap (Dynamic) -->
      <div
        v-if="profile.financials.fundingGap > 0"
        class="bg-yellow-50 p-4 rounded border-l-4 border-yellow-400"
      >
        <div class="flex justify-between items-center mb-2">
          <label class="font-semibold text-gray-700">Funding Gap</label>
          <span class="text-lg font-bold text-yellow-600">
            ${{ formatCurrency(profile.financials.fundingGap) }}
          </span>
        </div>
        <p class="text-sm text-gray-600">
          Amount needed to bridge the gap between cost and your budget
        </p>
      </div>

      <!-- Success State: Fully Funded -->
      <div
        v-else-if="
          profile.financials.estimatedCourseCost > 0 &&
          profile.financials.userBudget >= profile.financials.estimatedCourseCost
        "
        class="bg-green-50 p-4 rounded border-l-4 border-green-400"
      >
        <p class="text-green-700 font-semibold">
          ✅ You're fully funded for this course!
        </p>
      </div>
    </div>

    <!-- Demographics Summary -->
    <div v-if="profile.demographics" class="mt-8 pt-6 border-t">
      <h3 class="font-semibold text-gray-700 mb-3">Your Profile</h3>
      <div class="space-y-2 text-sm">
        <p v-if="profile.demographics.targetCourse">
          <span class="text-gray-600">🎓 Course:</span>
          <span class="font-semibold">{{ profile.demographics.targetCourse }}</span>
        </p>
        <p v-if="profile.demographics.targetCountry">
          <span class="text-gray-600">🌍 Country:</span>
          <span class="font-semibold">{{ profile.demographics.targetCountry }}</span>
        </p>
        <p v-if="profile.demographics.currentCGPA">
          <span class="text-gray-600">📈 CGPA:</span>
          <span class="font-semibold">{{ profile.demographics.currentCGPA }}</span>
        </p>
      </div>
    </div>

    <!-- Apply for Loan Button (Dynamic) -->
    <button
      v-if="shouldShowLoanButton"
      @click="$emit('loan-apply')"
      class="w-full mt-6 btn btn-secondary text-base font-bold"
    >
      💰 Apply for Pre-Qualified Loan
    </button>

    <!-- Reasons to Apply -->
    <div
      v-if="shouldShowLoanButton"
      class="mt-4 bg-blue-50 p-4 rounded text-sm text-blue-700"
    >
      <p class="font-semibold mb-2">Why apply now?</p>
      <ul class="list-disc list-inside space-y-1">
        <li>Zero-touch auto-fill with your profile data</li>
        <li>Instant pre-qualification decision</li>
        <li>Competitive education loan rates</li>
        <li>Flexible repayment terms</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  profile: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['loan-apply'])

// Compute progress percentages
const costProgressPercent = computed(() => {
  const cost = props.profile.financials?.estimatedCourseCost || 0
  return Math.min((cost / 500000) * 100, 100) // Assume max typical cost is $500k
})

const budgetProgressPercent = computed(() => {
  const budget = props.profile.financials?.userBudget || 0
  return Math.min((budget / 500000) * 100, 100)
})

// Show loan button only when fundingGap is calculated and > 0
const shouldShowLoanButton = computed(() => {
  return (
    props.profile.financials?.fundingGap > 0 &&
    props.profile.engagementState?.roiDashboardGenerated === true
  )
})

// Format currency
const formatCurrency = (value) => {
  if (!value) return '0'
  return parseFloat(value).toLocaleString('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  })
}
</script>
