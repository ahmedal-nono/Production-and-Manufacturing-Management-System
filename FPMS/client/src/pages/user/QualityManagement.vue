<template>
  <div class="m-2 flex h-max flex-col justify-center rounded-2xl bg-gray-200 p-4">
    <p class="flex justify-center text-xl font-bold">Quality Management</p>
    <div class="flex flex-row gap-10 py-4">
      <div
        v-if="userRole === 'Production Manager'"
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showQualityInspectionPopup = true"
      >
        <img src="@/assets/quality_inspection.webp" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Quality Inspection</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showReworkPopup = true"
      >
        <img src="@/assets/rework.webp" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Rework</p>
      </div>
    </div>
  </div>
  <QualityInspectionPopup
    v-if="showQualityInspectionPopup"
    @update:showQualityInspectionPopup="(v: boolean) => (showQualityInspectionPopup = v)"
    :showQualityInspectionPopup
  >
  </QualityInspectionPopup>
  <ReworkPopup
    v-if="showReworkPopup"
    @update:showReworkPopup="(v: boolean) => (showReworkPopup = v)"
    :showReworkPopup
  >
  </ReworkPopup>
</template>

<script setup lang="ts">
import { defineAsyncComponent, ref } from 'vue'
import { useUserStore } from '@/stores/user'

const QualityInspectionPopup = defineAsyncComponent(
  () => import('@/components/QualityInspectionPopup.vue'),
)
const ReworkPopup = defineAsyncComponent(() => import('@/components/ReworkPopup.vue'))

const userStore = useUserStore()
const userRole = userStore.user?.role

const showQualityInspectionPopup = ref(false)
const showReworkPopup = ref(false)
</script>

<style>
button {
  cursor: pointer;
}
</style>
