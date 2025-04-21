<template>
  <div class="w-fit">
    <div class="flex h-[100dvh] flex-col overflow-y-auto bg-[#8497aa] p-1">
      <RouterLink
        v-for="(link, index) in links"
        :to="{ name: link.to }"
        :key="index"
        class="m-1 my-2 flex h-6/12 cursor-pointer flex-col items-center justify-center rounded-lg border bg-white px-1 py-1"
      >
        <img :src="link.img" alt="" class="size-8" />
        <p class="text-[10px] text-nowrap">{{ link.name }}</p>
      </RouterLink>
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
