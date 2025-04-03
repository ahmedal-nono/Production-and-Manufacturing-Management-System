<template>
  <div v-if="router.currentRoute.value.name !== 'login'" class="flex flex-row">
    <sideBar class="" />
    <navBar class="">
      <RouterView />
    </navBar>
  </div>
  <div v-else>
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import sideBar from '@/components/sideBar.vue'
import navBar from '@/components/navBar.vue'
import router from './router'
</script>
