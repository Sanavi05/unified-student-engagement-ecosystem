<template>
  <div class="app-layout" :data-theme="isDarkMode ? 'dark' : 'light'">
    <!-- Top Navigation -->
    <header class="topbar">
      <div class="logo">
        <h1>EduPath AI</h1>
      </div>
      <div class="topbar-actions">
        <button class="theme-toggle" @click="toggleTheme">
          {{ isDarkMode ? '☀️ Light' : '🌙 Dark' }}
        </button>
        <div class="user-profile">
          <img src="https://ui-avatars.com/api/?name=Student&background=6366f1&color=fff" alt="Profile" />
        </div>
      </div>
    </header>

    <div class="main-body">
      <!-- Sidebar Navigation -->
      <aside class="sidebar">
        <nav>
          <router-link to="/dashboard" class="nav-item">
            Dashboard
          </router-link>
          <router-link to="/tools" class="nav-item">
            AI Tools
          </router-link>
          <router-link to="/finance" class="nav-item">
            Finance & Loans
          </router-link>
        </nav>
        
        <div class="sidebar-footer">
          <div class="ai-status">
            <span class="status-dot"></span>
            AI Services Online
          </div>
        </div>
      </aside>

      <!-- Main Content Area -->
      <main class="content-area">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
    
    <!-- Global Chatbot FAB -->
    <button class="chatbot-fab" @click="toggleChatbot">
      💬
    </button>
    
    <Chatbot :isOpen="isChatbotOpen" @close="isChatbotOpen = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Chatbot from './components/Chatbot.vue';

const isDarkMode = ref(true);
const isChatbotOpen = ref(false);

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
};

const toggleChatbot = () => {
  isChatbotOpen.value = !isChatbotOpen.value;
};
</script>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  background-color: var(--bg-color);
  color: var(--text-primary);
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  height: 70px;
  background-color: var(--surface-color);
  border-bottom: 1px solid var(--border-color);
  z-index: 10;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.theme-toggle {
  background: none;
  border: 1px solid var(--border-color);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  color: var(--text-primary);
  font-weight: 500;
}

.user-profile img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid var(--primary-color);
}

.main-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 250px;
  background-color: var(--surface-color);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.sidebar nav {
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  color: var(--text-secondary);
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background-color: rgba(99, 102, 241, 0.1);
  color: var(--primary-color);
}

.nav-item.router-link-active {
  background-color: var(--primary-color);
  color: white;
}

.sidebar-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.ai-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--secondary-color);
}

.status-dot {
  width: 8px;
  height: 8px;
  background-color: var(--secondary-color);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--secondary-color);
}

.content-area {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.chatbot-fab {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: white;
  font-size: 1.5rem;
  border: none;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  z-index: 1000;
}

.chatbot-fab:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
}
</style>
