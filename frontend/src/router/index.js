import { createRouter, createWebHistory } from 'vue-router';

// Lazy loading views
const Dashboard = () => import('../views/Dashboard.vue');
const Tools = () => import('../views/Tools.vue');
const Finance = () => import('../views/Finance.vue');

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', component: Dashboard, name: 'Dashboard' },
  { path: '/tools', component: Tools, name: 'Tools' },
  { path: '/finance', component: Finance, name: 'Finance' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
