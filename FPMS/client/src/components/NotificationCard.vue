<template>
  <div
    class="flex flex-col space-y-4 rounded-lg border-l-8 p-4"
    :class="isRead ? 'border-gray-500 bg-gray-100' : 'border-blue-500 bg-blue-50'"
  >
    <div class="flex justify-between">
      <p class="text-lg font-bold">{{ title }}</p>
      <p class="text-sm font-light text-gray-400">{{ time }}</p>
    </div>
    <div class="flex justify-start">
      <p class="text-gray-500">{{ body }}</p>
    </div>
    <div class="flex justify-around gap-5">
      <button
        v-if="!isRead"
        class="w-full rounded-lg bg-green-600 p-2 text-white"
        @click.stop="markAsRead()"
      >
        Mark As Read
      </button>
      <button class="w-full rounded-lg bg-blue-600 p-2 text-white">View Details</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import notificationStore from '@/stores/notificationStore'

let {
  isRead = false,
  time = '',
  title = '',
  body = '',
  id = '',
} = defineProps<{
  isRead: boolean
  time: string
  title: string
  body: string
  id: string // Added id for identifying notifications
}>()

const markAsRead = () => {
  isRead = true
  notificationStore.markNotificationAsRead(id) // Update the notification store
}
</script>

<style>
button {
  cursor: pointer;
}
</style>
