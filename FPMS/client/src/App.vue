<template>
  <div v-if="isNotLoggedIn" class="flex flex-row">
    <RouterView />
  </div>
  <div v-else>
    <sideBar class="" />
    <navBar class="">
      <RouterView />
    </navBar>
  </div>
</template>

<script setup lang="ts">
import sideBar from '@/components/sideBar.vue'
import navBar from '@/components/navBar.vue'
import router from './router'
import { useUserStore } from './stores/user'
import { computed } from 'vue'

const isNotLoggedIn = computed(() => {
  const x = router.currentRoute.value.name === 'login' && !userStore.isAuthenticated
  if (!x) router.push({ name: 'home' })
  return x
})

const userStore = useUserStore()
</script>
