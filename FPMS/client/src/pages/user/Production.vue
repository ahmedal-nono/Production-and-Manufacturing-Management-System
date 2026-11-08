<template>
  <div class="m-2 flex h-max flex-col justify-center rounded-2xl bg-gray-200 p-4">
    <p class="flex justify-center text-xl font-bold">Production & Workflow Management</p>
    <div class="flex flex-row gap-10 py-4">
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="() => (showProductionPopup = true)"
      >
        <img src="@/assets/production.webp" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Production</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showWorkflowsPopup = true"
      >
        <img src="@/assets/workflows.webp" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Workflows</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="() => (showProductionLinesPopup = true)"
      >
        <img src="@/assets/production_line.webp" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Production Lines</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="() => (showBOMsPopup = true)"
      >
        <img src="@/assets/bom.webp" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">BOMs</p>
      </div>
    </div>
  </div>

  <Popup :visible="showProductionPopup" @update:visible="showProductionPopup = $event">
    <div class="m-2 flex h-max flex-col justify-center rounded-2xl p-4">
      <p class="flex justify-center text-xl font-bold">Production Management</p>
      <div class="flex flex-row gap-10 py-4">
        <div
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
          @click="() => (showProductionSchedulePopup = true)"
        >
          <img src="@/assets/production_schedule.webp" class="size-20" alt="" />
          <p class="pt-2 text-[13px] font-bold">Production Schedule</p>
        </div>
        <div
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
          @click="() => (showProductionOrdersPopup = true)"
        >
          <img src="@/assets/production_orders.webp" class="size-20" alt="" />
          <p class="pt-2 text-[13px] font-bold">Production Orders</p>
        </div>
        <div
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
          @click="() => (showProductsPopup = true)"
        >
          <img src="@/assets/products.webp" class="size-20" alt="" />
          <p class="pt-2 text-[13px] font-bold">Products</p>
        </div>
      </div>
    </div>
  </Popup>

  <ProductionSchedulePopup
    v-if="showProductionSchedulePopup"
    @update:showProductionSchedulePopup="(v: boolean) => (showProductionSchedulePopup = v)"
    :showProductionSchedulePopup
  ></ProductionSchedulePopup>

  <ProductionOrdersPopup
    v-if="showProductionOrdersPopup"
    @update:showProductionOrdersPopup="(v: boolean) => (showProductionOrdersPopup = v)"
    :showProductionOrdersPopup
  ></ProductionOrdersPopup>
  <ProductsPopup
    v-if="showProductsPopup"
    @update:showProductsPopup="(v: boolean) => (showProductsPopup = v)"
    :showProductsPopup
  ></ProductsPopup>
  <WorkflowPopup
    v-if="showWorkflowsPopup"
    @update:showWorkflowsPopup="(v: boolean) => (showWorkflowsPopup = v)"
    :showWorkflowsPopup
  ></WorkflowPopup>
  <ProductionLinesPopup
    v-if="showProductionLinesPopup"
    @update:showProductionLinesPopup="(v: boolean) => (showProductionLinesPopup = v)"
    :showProductionLinesPopup
  ></ProductionLinesPopup>
  <BOMsPopup
    v-if="showBOMsPopup"
    @update:showBOMsPopup="(v: boolean) => (showBOMsPopup = v)"
    :showBOMsPopup
  ></BOMsPopup>
</template>

<script setup lang="ts">
import { defineAsyncComponent, ref } from 'vue'
import Popup from '@/components/popup.vue'

// Popups are loaded and mounted only when the user opens them, so the
// production page no longer fires every popup's API calls on page load.
const ProductionSchedulePopup = defineAsyncComponent(
  () => import('@/components/ProductionSchedulePopup.vue'),
)
const ProductionOrdersPopup = defineAsyncComponent(
  () => import('@/components/ProductionOrdersPopup.vue'),
)
const ProductsPopup = defineAsyncComponent(() => import('@/components/ProductsPopup.vue'))
const WorkflowPopup = defineAsyncComponent(() => import('@/components/WorkflowPopup.vue'))
const ProductionLinesPopup = defineAsyncComponent(
  () => import('@/components/ProductionLinesPopup.vue'),
)
const BOMsPopup = defineAsyncComponent(() => import('@/components/BOMsPopup.vue'))

const showProductionPopup = ref(false)
const showProductionSchedulePopup = ref(false)
const showProductionOrdersPopup = ref(false)
const showProductsPopup = ref(false)
const showWorkflowsPopup = ref(false)
const showProductionLinesPopup = ref(false)
const showBOMsPopup = ref(false)

const submitOrder = () => {
  console.log('Order submitted')
}
</script>

<style>
button {
  cursor: pointer;
}
</style>
