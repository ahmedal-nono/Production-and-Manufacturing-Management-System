<template>
  <div class="m-2 flex h-max flex-col justify-center rounded-2xl bg-gray-200 p-4">
    <p class="flex justify-center text-xl font-bold">Reports and Analytics</p>
    <div class="flex flex-row gap-10 py-4">
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showReportedIssuesPopup = true"
      >
        <img src="@/assets/reported_issues.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Reported Issues</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showAnalyticsPopup = true"
      >
        <img src="@/assets/analytics.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Analytics</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const showReportedIssuesPopup = ref(false)
const showAnalyticsPopup = ref(false)
</script>

<style scoped></style>
