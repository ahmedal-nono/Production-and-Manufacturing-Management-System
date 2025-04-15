<template>
  <div class="m-2 flex h-max flex-col justify-center rounded-2xl bg-gray-200 p-4">
    <p class="flex justify-center text-xl font-bold">Workorders / Instructions</p>
    <div class="flex flex-row gap-10 py-4">
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showWorkordersPopup = true"
      >
        <img src="@/assets/workorders.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Workorders</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showJobCardsPopup = true"
      >
        <img src="@/assets/job_cards.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Job Cards</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showWorkinstructionPopup = true"
      >
        <img src="@/assets/work_instructions.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Work Instructions</p>
      </div>
    </div>
  </div>
  <WorkordersPopup
    @update:showWorkordersPopup="(v) => (showWorkordersPopup = v)"
    :showWorkordersPopup
  ></WorkordersPopup>
  <JobCardsPopup @update:showJobCardsPopup="(v) => (showJobCardsPopup = v)" :showJobCardsPopup>
  </JobCardsPopup>
  <WorkinstructionPopup
    @update:showWorkinstructionPopup="(v) => (showWorkinstructionPopup = v)"
    :showWorkinstructionPopup
  >
  </WorkinstructionPopup>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import WorkordersPopup from '@/components/WorkordersPopup.vue'
import JobCardsPopup from '@/components/JobCardsPopup.vue'
import WorkinstructionPopup from '@/components/WorkinstructionPopup.vue'
const showWorkordersPopup = ref(false)
const showJobCardsPopup = ref(false)
const showWorkinstructionPopup = ref(false)
</script>

<style>
button {
  cursor: pointer;
}
</style>
