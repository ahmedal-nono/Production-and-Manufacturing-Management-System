<template>
  <div class="w-fit p-1">
    <div class="flex h-[99dvh] flex-col overflow-y-auto rounded-xl bg-[#5477AD] p-1">
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

const links = [
  {
    img: systemImg,
    name: 'System Admin',
    to: 'home',
  },
  {
    img: systemImg,
    name: 'Workcenters',
    to: 'wrkcntr',
  },
  {
    img: systemImg,
    name: 'Production',
    to: 'wrkcntr',
  },
  {
    img: systemImg,
    name: 'BOM',
    to: 'wrkcntr',
  },
  {
    img: systemImg,
    name: 'Workorders / Instructions',
    to: 'wrkcntr',
  },
  {
    img: systemImg,
    name: 'Quality Management',
    to: 'wrkcntr',
  },
  {
    img: systemImg,
    name: 'Reports',
    to: 'wrkcntr',
  },
]
</script>
