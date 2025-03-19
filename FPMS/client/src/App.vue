<template>
  <div class="flex flex-row">
    <sideBar class="" />
    <RouterView />
    <RouterLink :to="{ name: 'home' }">Home</RouterLink>
    <RouterLink :to="{ name: 'about' }">About</RouterLink>
    <navBar class="" />
  </div>
</template>

<script setup lang="ts">
import sideBar from "./components/sideBar.vue";
import navBar from "./components/navBar.vue";
</script>

<style></style>
