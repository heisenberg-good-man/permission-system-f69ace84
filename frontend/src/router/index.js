import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/jobs'
  },
  {
    path: '/jobs',
    name: 'Jobs',
    component: () => import('../views/Jobs.vue')
  },
  {
    path: '/jobs/:id',
    name: 'JobDetail',
    component: () => import('../views/JobDetail.vue')
  },
  {
    path: '/job-manage',
    name: 'JobManage',
    component: () => import('../views/JobManage.vue')
  },
  {
    path: '/applications',
    name: 'Applications',
    component: () => import('../views/Applications.vue')
  },
  {
    path: '/my-applications',
    name: 'MyApplications',
    component: () => import('../views/MyApplications.vue')
  },
  {
    path: '/communication/:id',
    name: 'Communication',
    component: () => import('../views/Communication.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
