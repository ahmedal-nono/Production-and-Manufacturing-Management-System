import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/pages/admin/SystemAdministraion.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/Login.vue'),
    },
    {
      path: '/workcenters',
      name: 'workcenters',
      component: () => import('@/pages/user/WorkcentersWorkstationsManagement.vue'),
    },
    {
      path: '/production',
      name: 'production',
      component: () => import('@/pages/user/Production.vue'),
    },
    {
      path: '/workorders',
      name: 'workorders',
      component: () => import('@/pages/user/Workorders.vue'),
    },
    {
      path: '/quality',
      name: 'quality',
      component: () => import('@/pages/user/QualityManagement.vue'),
    },
    {
      path: '/reports',
      name: 'reports',
      component: () => import('@/pages/user/Reports.vue'),
    },
  ],
})

// router.beforeEach((to, from, next) => {
//   const userStore = useUserStore() // Move inside beforeEach
//   if (!userStore.isAuthenticated && to.path !== '/login') {
//     return next('/login')
//   }
//   next()
// })

export default router
