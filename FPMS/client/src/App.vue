<template>
  <div v-if="isLoginRoute">
    <RouterView />
  </div>
  <div v-else class="flex flex-row">
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
import { useRoute } from 'vue-router'

const route = useRoute()
const isLoginRoute = computed(() => route.name === 'login')

const userStore = useUserStore()
</script>
