import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
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
  },
  {
    path: '/interviews',
    name: 'Interviews',
    component: () => import('../views/Interviews.vue')
  },
  {
    path: '/my-interviews',
    name: 'MyInterviews',
    component: () => import('../views/MyInterviews.vue')
  },
  {
    path: '/offers',
    name: 'Offers',
    component: () => import('../views/Offers.vue')
  },
  {
    path: '/my-offers',
    name: 'MyOffers',
    component: () => import('../views/MyOffers.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
