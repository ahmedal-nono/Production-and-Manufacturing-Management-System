<template>
  <div class="w-fit">
    <div class="flex h-[100dvh] flex-col overflow-y-auto bg-[#8497aa] p-1">
      <template v-for="(link, index) in links" :key="index">
        <RouterLink
        v-if="allowedLinks.some((l) => l.to === link.to)"
        :to="{ name: link.to }"
          class="m-1 my-2 flex h-6/12 cursor-pointer flex-col items-center justify-center rounded-lg border bg-white px-1 py-1"
        >
          <img :src="link.img" alt="" class="size-8" />
          <p class="text-[10px] text-nowrap">{{ link.name }}</p>
        </RouterLink>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import systemImg from '@/assets/system_admin.png'
import wrkcntr from '@/assets/wokrcenters.png'
import production from '@/assets/production.png'
import workorder from '@/assets/workorder.png'
import quality from '@/assets/quality.png'
import reports from '@/assets/reports.png'
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'

const roleRoutes = {
  'Quality Control Manager': { name: 'quality' },
  'Quality Control Inspector': { name: 'reports' },
  Admin: { name: 'home' },
  'Production Planner': { name: 'production' },
  'Production Manager': { name: 'workcenters' },
  '404': { name: 'not-found' },
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
const { user } = useUserStore()
const allowedLinks = computed(() => {
  const userRole = user?.role || ''
  const allowedRoutes = allowedRoutesByRole.find((r) => r.role === userRole)?.names || []
  return links
    .filter((link) => allowedRoutes.includes(link.to))
    .map((link) => ({
      to: link.to,
    }))
})

const links = [
  {
    img: systemImg,
    name: 'System Admin',
    to: 'home',
  },
  {
    img: wrkcntr,
    name: 'Workcenters',
    to: 'workcenters',
  },
  {
    img: production,
    name: 'Production',
    to: 'production',
  },
  {
    img: workorder,
    name: 'Workorders / Instructions',
    to: 'workorders',
  },
  {
    img: quality,
    name: 'Quality Management',
    to: 'quality',
  },
  {
    img: reports,
    name: 'Reports',
    to: 'reports',
  },
]
</script>

<style>
button {
  cursor: pointer;
}
</style>
