<template>
  <div class="bg-white rounded-lg shadow-lg p-6 h-full flex flex-col">
    <h2 class="text-2xl font-bold text-gray-800 mb-4">
      💬 AI Copilot Chat
    </h2>

    <!-- Chat History -->
    <div class="flex-1 overflow-y-auto mb-4 bg-gray-50 rounded p-4 space-y-3">
      <div
        v-if="chatHistory.length === 0"
        class="text-center text-gray-400 py-8"
      >
        <p class="text-lg">👋 Start a conversation about your study abroad plans!</p>
        <p class="text-sm mt-2">Ask about courses, costs, and scholarship opportunities.</p>
      </div>

      <div
        v-for="(msg, index) in chatHistory"
        :key="index"
        :class="['message', msg.role === 'user' ? 'user' : 'assistant']"
      >
        <p class="text-sm">{{ msg.message }}</p>
      </div>

      <div v-if="isLoading" class="flex items-center space-x-2">
        <div class="animate-pulse space-y-2">
          <div class="h-3 bg-gray-300 rounded w-32"></div>
          <div class="h-3 bg-gray-300 rounded w-24"></div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="flex gap-2">
      <input
        v-model="userMessage"
        type="text"
        placeholder="Tell me about your study abroad plans..."
        @keyup.enter="sendMessage"
        :disabled="isLoading"
        class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
      />
      <button
        @click="sendMessage"
        :disabled="isLoading || !userMessage.trim()"
        class="btn btn-primary disabled:btn-disabled"
      >
        Send
      </button>
    </div>

    <!-- Status -->
    <div v-if="statusMessage" class="mt-2 text-sm text-blue-600">
      {{ statusMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['chat-updated'])

const userMessage = ref('')
const chatHistory = ref([
  {
    role: 'assistant',
    message:
      "Hello! I'm your Study Abroad Copilot. I'll help you plan your international education journey, explore funding options, and calculate your personalized loan offer. What country are you interested in?",
  },
])
const isLoading = ref(false)
const statusMessage = ref('')

const sendMessage = async () => {
  if (!userMessage.value.trim()) return

  // Add user message to chat
  chatHistory.value.push({
    role: 'user',
    message: userMessage.value,
  })

  const messageToSend = userMessage.value
  userMessage.value = ''
  isLoading.value = true
  statusMessage.value = 'Processing your message with AI...'

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        userId: props.userId,
        message: messageToSend,
        demographics: {},
      }),
    })

    const data = await response.json()

    if (data.success) {
      // Get the latest AI response from chat history
      let aiMessageFound = false;
      
      if (data.chatHistory && data.chatHistory.length > 0) {
        // Look for the most recent assistant message
        for (let i = data.chatHistory.length - 1; i >= 0; i--) {
          if (data.chatHistory[i].role === 'assistant') {
            chatHistory.value.push({
              role: 'assistant',
              message: data.chatHistory[i].message,
            })
            aiMessageFound = true
            break
          }
        }
      }

      if (!aiMessageFound) {
        // Fallback: show generic message
        chatHistory.value.push({
          role: 'assistant',
          message: 'I\'m processing your request. Please give me a moment...',
        })
      }

      statusMessage.value = '✓ Profile updated with AI insights'
      setTimeout(() => {
        statusMessage.value = ''
      }, 3000)

      emit('chat-updated', data)
    } else {
      chatHistory.value.push({
        role: 'assistant',
        message: '⚠️ Unable to process request. Please try again.',
      })
    }
  } catch (error) {
    console.error('Chat error:', error)
    chatHistory.value.push({
      role: 'assistant',
      message: '❌ Error: Could not reach the AI service. Check if the backend is running.',
    })
  } finally {
    isLoading.value = false
  }
}
</script>
