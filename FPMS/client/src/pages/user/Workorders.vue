<template>
  <div class="m-2 flex h-max flex-col justify-center rounded-2xl bg-gray-200 p-4">
    <p class="flex justify-center text-xl font-bold">Workorders / Instructions</p>
    <div class="flex flex-row gap-10 py-4">
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showWorkordersPopup = true"
      >
        <img src="@/assets/workorders.webp" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Workorders</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showJobCardsPopup = true"
      >
        <img src="@/assets/job_cards.webp" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Job Cards</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showWorkinstructionPopup = true"
      >
        <img src="@/assets/work_instructions.webp" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Work Instructions</p>
      </div>
    </div>
  </div>
  <WorkordersPopup
    v-if="showWorkordersPopup"
    @update:showWorkordersPopup="(v: boolean) => (showWorkordersPopup = v)"
    :showWorkordersPopup
  ></WorkordersPopup>
  <JobCardsPopup
    v-if="showJobCardsPopup"
    @update:showJobCardsPopup="(v: boolean) => (showJobCardsPopup = v)"
    :showJobCardsPopup
  >
  </JobCardsPopup>
  <WorkinstructionPopup
    v-if="showWorkinstructionPopup"
    @update:showWorkinstructionPopup="(v: boolean) => (showWorkinstructionPopup = v)"
    :showWorkinstructionPopup
  >
  </WorkinstructionPopup>
</template>

<script setup lang="ts">
import { defineAsyncComponent, ref } from 'vue'

const WorkordersPopup = defineAsyncComponent(
  () => import('@/components/WorkordersPopup.vue'),
)
const JobCardsPopup = defineAsyncComponent(() => import('@/components/JobCardsPopup.vue'))
const WorkinstructionPopup = defineAsyncComponent(
  () => import('@/components/WorkinstructionPopup.vue'),
)
const showWorkordersPopup = ref(false)
const showJobCardsPopup = ref(false)
const showWorkinstructionPopup = ref(false)
</script>

<style>
button {
  cursor: pointer;
}
</style>
