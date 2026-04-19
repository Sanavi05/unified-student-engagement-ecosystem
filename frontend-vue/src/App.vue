<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- Header -->
    <header class="bg-white shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <h1 class="text-3xl font-bold text-blue-600">
          🎓 Student Engagement Ecosystem
        </h1>
        <p class="text-gray-600 mt-1">
          AI-Powered Study Abroad & Loan Planning Platform
        </p>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Chat Widget (Left/Top) -->
        <div class="lg:col-span-2">
          <ChatWidget
            :userId="userId"
            @chat-updated="onChatUpdated"
          />
        </div>

        <!-- ROI Dashboard (Right/Bottom) -->
        <div class="lg:col-span-1">
          <ROIDashboard
            :profile="studentProfile"
            @loan-apply="onLoanApply"
          />
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white mt-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <p class="text-center">
          © 2026 Unified Student Engagement Ecosystem. Powered by AI & Gemini.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ChatWidget from './components/ChatWidget.vue'
import ROIDashboard from './components/ROIDashboard.vue'

const userId = ref('student_' + Date.now())
const studentProfile = ref({
  demographics: {},
  financials: { fundingGap: 0 },
  engagementState: { roiDashboardGenerated: false },
})

const onChatUpdated = (data) => {
  console.log('Chat updated:', data)
  // Fetch updated profile from backend
  fetchProfile()
}

const onLoanApply = () => {
  alert(
    '✅ Loan Application Submitted!\n\nYour pre-qualified offer has been auto-filled and sent for processing.\n\nExpected approval in 24 hours.'
  )
}

const fetchProfile = async () => {
  try {
    const response = await fetch(`/api/dashboard/${userId.value}`)
    const data = await response.json()
    if (data.success) {
      studentProfile.value = data.profile
    }
  } catch (error) {
    console.error('Error fetching profile:', error)
  }
}

onMounted(() => {
  fetchProfile()
})
</script>
