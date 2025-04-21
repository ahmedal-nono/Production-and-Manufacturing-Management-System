import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// Define routes
const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/pages/admin/SystemAdministraion.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/Login.vue'),
    meta: { layout: 'auth', requiresAuth: false },
  },
  {
    path: '/workcenters',
    name: 'workcenters',
    component: () => import('@/pages/user/WorkcentersWorkstationsManagement.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/production',
    name: 'production',
    component: () => import('@/pages/user/Production.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/workorders',
    name: 'workorders',
    component: () => import('@/pages/user/Workorders.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/quality',
    name: 'quality',
    component: () => import('@/pages/user/QualityManagement.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/reports',
    name: 'reports',
    component: () => import('@/pages/user/Reports.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/:catchAll(.*)',
    name: 'not-found',
    component: () => import('@/pages/Login.vue'),
    meta: { layout: 'auth' },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Role-based redirection map
const roleRoutes = {
  'Quality Control Manager': 'quality',
  'Quality Control Inspector': 'reports',
  'Production Manager': 'workcenters',
  'Production Planner': 'production',
  Admin: 'home',
  '404': 'not-found',
}

const allowedRoutesByRole = [
  {
    role: 'Admin',
    names: ['home'],
  },
  {
    role: 'Quality Control Manager',
    names: ['quality', 'reports'],
  },
  {
    role: 'Quality Control Inspector',
    names: ['reports'],
  },
  {
    role: 'Production Manager',
    names: ['quality', 'workorders', 'reports', 'workcenters', 'production'],
  },
  {
    role: 'Production Planner',
    names: ['production'],
  },
]

// Navigation guard
router.beforeEach((to, from, next) => {
  const { isAuthenticated, user } = useUserStore()
  const isAuth = isAuthenticated
  const role = (user?.role || '404') as keyof typeof roleRoutes

  // If route requires auth and not logged in
  // console.log('user?.role', user?.role)
  // console.log('isAuth', isAuth)
  // console.log('to.name', to.name)
  // console.log('role', role)
  // console.log("to.name !== 'login' && !isAuth", to.name !== 'login' && !isAuth)

  if (to.name !== 'login' && !isAuth) {
    return next({ name: 'login' })
  }

  // If trying to go to login while already logged in
  if (to.name === 'login' && isAuth) {
    const targetRoute = roleRoutes[role]
    return next({ name: targetRoute })
  }

  // If user is not allowed to access the route
  const allowedRoutes = allowedRoutesByRole.find((r) => r.role === role)?.names || []
  // console.log('allowedRoutes', allowedRoutes, !allowedRoutes.includes(to.name as string))

  if (allowedRoutes && allowedRoutes.length > 0 && !allowedRoutes.includes(to.name as string)) {
    // console.log(
    //   '!allowedRoutes.includes(to.name as string)',
    //   !allowedRoutes.includes(to.name as string),
    // )
    const fallback = roleRoutes[role]
    // console.log('fallback', fallback)
    return next({ name: fallback })
  } else next()
})

export default router
