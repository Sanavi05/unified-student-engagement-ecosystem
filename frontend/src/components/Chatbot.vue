<template>
  <div class="chatbot-container" :class="{ 'is-open': isOpen }">
    <div class="chatbot-window" v-if="isOpen">
      <div class="chatbot-header">
        <div class="header-info">
          <span class="bot-icon">🤖</span>
          <div>
            <h3>EduMentor AI</h3>
            <span class="status">Online</span>
          </div>
        </div>
        <button class="close-btn" @click="$emit('close')">✖</button>
      </div>
      
      <div class="chatbot-messages" ref="messagesContainer">
        <div 
          v-for="(msg, index) in messages" 
          :key="index" 
          class="message-wrapper"
          :class="msg.sender === 'user' ? 'user-wrapper' : 'bot-wrapper'"
        >
          <div class="message" :class="msg.sender">
            {{ msg.text }}
          </div>
          <div v-if="msg.sender === 'bot' && msg.options" class="options-wrapper">
            <button 
              v-for="opt in msg.options" 
              :key="opt" 
              class="option-btn"
              @click="sendMessage(opt)"
            >
              {{ opt }}
            </button>
          </div>
        </div>
        <div v-if="isTyping" class="message-wrapper bot-wrapper">
          <div class="message bot typing">
            <span class="dot"></span><span class="dot"></span><span class="dot"></span>
          </div>
        </div>
      </div>

      <div class="chatbot-input">
        <input 
          type="text" 
          v-model="newMessage" 
          placeholder="Ask about universities, loans, SOPs..." 
          @keypress.enter="sendMessage(newMessage)"
        />
        <button class="send-btn" @click="sendMessage(newMessage)">➤</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';

const props = defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['close']);

const messagesContainer = ref(null);
const newMessage = ref('');
const isTyping = ref(false);

const messages = ref([
  {
    sender: 'bot',
    text: 'Hi there! 👋 I am your EduMentor AI. How can I help you plan your higher education today?',
    options: ['Suggest Universities', 'Explain Loans', 'Check Admission Chances']
  }
]);

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const sendMessage = (text) => {
  if (!text || !text.trim()) return;
  
  // Add user message
  messages.value.push({
    sender: 'user',
    text: text.trim()
  });
  
  newMessage.value = '';
  scrollToBottom();
  
  // Mock AI response
  isTyping.value = true;
  setTimeout(() => {
    isTyping.value = false;
    generateMockResponse(text);
    scrollToBottom();
  }, 1000);
};

const generateMockResponse = (userInput) => {
  const input = userInput.toLowerCase();
  let botReply = "I can certainly help with that! Let's explore your options in the Dashboard.";
  
  if (input.includes('university') || input.includes('suggest')) {
    botReply = "Based on your 8.5 GPA, I recommend looking into Tier 1 universities in the US. Shall we navigate to the AI Career Navigator?";
  } else if (input.includes('loan')) {
    botReply = "Education loans typically range from 8-12% interest. Our Finance section has some pre-approved offers for you without collateral. Check out HDFC Credila!";
  } else if (input.includes('chance') || input.includes('admission')) {
    botReply = "Your admission chances are currently around 75%. Improving your Statement of Purpose (SOP) could boost this to 85% or higher.";
  }

  messages.value.push({ sender: 'bot', text: botReply });
};

watch(() => props.isOpen, (newVal) => {
  if (newVal) scrollToBottom();
});

</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 90px;
  right: 2rem;
  z-index: 1000;
  pointer-events: none;
}

.chatbot-container.is-open {
  pointer-events: all;
}

.chatbot-window {
  width: 350px;
  height: 500px;
  background-color: var(--surface-color);
  border-radius: 16px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--border-color);
  animation: slideUp 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.chatbot-header {
  padding: 1rem;
  background: var(--primary-color);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.bot-icon {
  font-size: 1.5rem;
  background: rgba(255, 255, 255, 0.2);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.header-info h3 {
  font-size: 1rem;
  margin: 0;
}

.status {
  font-size: 0.75rem;
  opacity: 0.8;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.close-btn:hover {
  opacity: 1;
}

.chatbot-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: var(--bg-color);
}

.message-wrapper {
  display: flex;
  flex-direction: column;
  max-width: 85%;
}

.user-wrapper {
  align-self: flex-end;
}

.bot-wrapper {
  align-self: flex-start;
}

.message {
  padding: 0.75rem 1rem;
  border-radius: 16px;
  font-size: 0.9rem;
  line-height: 1.4;
}

.message.user {
  background-color: var(--primary-color);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.bot {
  background-color: var(--surface-color);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-bottom-left-radius: 4px;
}

.options-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.option-btn {
  background-color: var(--surface-color);
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
  padding: 0.5rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}

.option-btn:hover {
  background-color: var(--primary-color);
  color: white;
}

.typing .dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--text-secondary);
  margin-right: 4px;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing .dot:nth-child(1) { animation-delay: -0.32s; }
.typing .dot:nth-child(2) { animation-delay: -0.16s; }
.typing .dot:nth-child(3) { margin-right: 0; }

.chatbot-input {
  display: flex;
  padding: 1rem;
  background-color: var(--surface-color);
  border-top: 1px solid var(--border-color);
  gap: 0.5rem;
}

.chatbot-input input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background-color: var(--bg-color);
  color: var(--text-primary);
  font-family: inherit;
  outline: none;
}

.chatbot-input input:focus {
  border-color: var(--primary-color);
}

.send-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-btn:hover {
  background-color: var(--primary-hover);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
</style>
