<template>
  <div class="m-2 flex h-max flex-col justify-center rounded-2xl bg-gray-200 p-4">
    <p class="flex justify-center text-xl font-bold">Production & Workflow Management</p>
    <div class="flex flex-row gap-10 py-4">
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showProductionPopup = true"
      >
        <img src="@/assets/production.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Production</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showWorkflowsPopup = true"
      >
        <img src="@/assets/workflows.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Workflows</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showProductionLinesPopup = true"
      >
        <img src="@/assets/production_line.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Production Lines</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showBOMsPopup = true"
      >
        <img src="@/assets/bom.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">BOMs</p>
      </div>
    </div>
  </div>

  <Popup :visible="showProductionPopup" @update:visible="showProductionPopup = $event">
    <div class="m-2 flex h-max flex-col justify-center rounded-2xl bg-gray-200 p-4">
      <p class="flex justify-center text-xl font-bold">Production Management</p>
      <div class="flex flex-row gap-10 py-4">
        <div
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
          @click="showProductionSchedulePopup = true"
        >
          <img src="@/assets/production_schedule.png" class="size-20" alt="" />
          <p class="pt-2 text-[13px] font-bold">Production Schedule</p>
        </div>
        <div
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
          @click="showProductionOrdersPopup = true"
        >
          <img src="@/assets/production_orders.png" class="size-20" alt="" />
          <p class="pt-2 text-[13px] font-bold">Production Orders</p>
        </div>
        <div
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
          @click="showProductsPopup = true"
        >
          <img src="@/assets/products.png" class="size-20" alt="" />
          <p class="pt-2 text-[13px] font-bold">Products</p>
        </div>
      </div>
    </div>
  </Popup>

  <ProductionSchedulePopup
    @update:showProductionSchedulePopup="(v) => (showProductionSchedulePopup = v)"
    :showProductionSchedulePopup
    orderId="1234"
    schedule="2024-03-15 to 2024-03-20"
    line="Line 1"
    :quantity="500"
    status="On Track"
    :progress="75"
    :stages="[
      { name: 'Material Preparation', status: 'Queued', team: 'Team A' },
      { name: 'Assembly Process', status: 'In Progress', team: 'Team B' },
    ]"
    @close="showProductionSchedulePopup = false"
    @submit="submitOrder"
  ></ProductionSchedulePopup>
  <ProductionOrdersPopup
    @update:showProductionOrdersPopup="(v) => (showProductionOrdersPopup = v)"
    :showProductionOrdersPopup
  ></ProductionOrdersPopup>
  <ProductsPopup
    @update:showProductsPopup="(v) => (showProductsPopup = v)"
    :showProductsPopup
  ></ProductsPopup>
  <WorkflowPopup
    @update:showWorkflowsPopup="(v) => (showWorkflowsPopup = v)"
    :showWorkflowsPopup
  ></WorkflowPopup>
  <ProductionLinesPopup
    @update:showProductionLinesPopup="(v) => (showProductionLinesPopup = v)"
    :showProductionLinesPopup
  ></ProductionLinesPopup>
  <BOMsPopup @update:showBOMsPopup="(v) => (showBOMsPopup = v)" :showBOMsPopup></BOMsPopup>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Popup from '@/components/popup.vue'
import ProductionSchedulePopup from '@/components/ProductionSchedulePopup.vue'
import ProductionOrdersPopup from '@/components/ProductionOrdersPopup.vue'
import ProductsPopup from '@/components/ProductsPopup.vue'
import WorkflowPopup from '@/components/WorkflowPopup.vue'
import ProductionLinesPopup from '@/components/ProductionLinesPopup.vue'
import BOMsPopup from '@/components/BOMsPopup.vue'

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

<style scoped>
th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
</style>
