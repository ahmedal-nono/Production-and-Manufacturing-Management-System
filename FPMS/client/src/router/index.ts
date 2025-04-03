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
      path: '/wrkcntr',
      name: 'wrkcntr',
      component: () => import('@/pages/user/WorkcentersWorkstationsManagement.vue'),
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
