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
        @click="showProductionOrdersPopup = true"
      >
        <img src="@/assets/workflows.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Workflows</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showProductionOrdersPopup = true"
      >
        <img src="@/assets/production_line.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Production Lines</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showProductionOrdersPopup = true"
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

  <Popup
    :visible="showProductionSchedulePopup"
    @update:visible="showProductionSchedulePopup = $event"
  >
    <div class="rounded-lg bg-white p-4 shadow-md">
      <h2 class="mb-4 text-xl font-semibold">Production Orders</h2>

      <!-- Filters -->
      <div class="mb-4 flex gap-2">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search orders..."
          class="w-full rounded border p-2"
        />
        <select v-model="selectedStatus" class="rounded border p-2">
          <option>All Statuses</option>
          <option>On Track</option>
          <option>Delayed</option>
        </select>
        <select v-model="selectedLine" class="rounded border p-2">
          <option>All Lines</option>
          <option>Line 1</option>
          <option>Line 2</option>
        </select>
      </div>

      <!-- Table -->
      <table class="w-full border-collapse border">
        <thead class="bg-gray-100">
          <tr>
            <th class="border p-2">Order ID</th>
            <th class="border p-2">Product</th>
            <th class="border p-2">Quantity</th>
            <th class="border p-2">Status</th>
            <th class="border p-2">Start Date</th>
            <th class="border p-2">End Date</th>
            <th class="border p-2">Production Line</th>
            <th class="border p-2">Priority</th>
            <th class="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in filteredOrders" :key="order.id" class="text-center">
            <td @click="showProductInfoPopup = true" class="border p-2">{{ order.id }}</td>
            <td class="border p-2">{{ order.product }}</td>
            <td class="border p-2">{{ order.quantity }}</td>
            <td class="border p-2">
              <span
                @click="showProductInfoPopup = true"
                class="rounded px-2 py-1"
                :class="getStatusClass(order.status)"
              >
                {{ order.status }}
              </span>
            </td>
            <td class="border p-2">
              <input type="date" v-model="order.startDate" class="w-full rounded border p-1" />
            </td>
            <td class="border p-2">
              <input type="date" v-model="order.endDate" class="w-full rounded border p-1" />
            </td>
            <td class="border p-2">{{ order.productionLine }}</td>
            <td class="border p-2">
              <span :class="getPriorityClass(order.priority)"> ● {{ order.priority }} </span>
            </td>
            <td class="border p-2">
              <button
                @click="showReschedulePopup = true"
                class="mt-4 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
              >
                Reschedule
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </Popup>

  <Popup :visible="showReschedulePopup" @update:visible="showReschedulePopup = $event">
    <div>
      <h2 class="mb-1 text-xl font-bold">
        Reschedule Order: <span class="font-bold">{{ props.orderId }}</span>
        <p class="mt-2 mb-1 text-sm text-gray-600">
          Current Schedule: <span class="font-medium">{{ props.schedule }}</span>
        </p>
        <p class="mb-4 text-sm text-gray-600">
          Production Line: <span class="font-medium">{{ props.line }}</span>
        </p>
      </h2>
      <div class="">
        <div class="flex flex-col justify-between">
          <label class="mb-1 block text-sm">New Start Time </label>
          <input v-model="newStartTime" type="datetime-local" class="rounded border p-2" />
        </div>
        <div class="flex flex-col justify-between">
          <label class="mt-2 mb-1 text-sm">New End Time </label>
          <input v-model="newEndTime" type="datetime-local" class="rounded border p-2" />
        </div>
      </div>
      <div class="mt-2 mb-4 flex flex-col justify-between">
        <label class="mb-1 text-sm">Reason for Reschedule </label>
        <select v-model="reason" class="rounded border p-2">
          <option value="" disabled>Select a reason</option>
          <option v-for="r in reasons" :key="r" :value="r">{{ r }}</option>
        </select>
      </div>
      <div class="mb-4">
        <label class="mb-1 text-sm">Additional Notes</label>
        <input
          v-model="note"
          type="text"
          class="w-full rounded border p-2"
          placeholder="Add any notes..."
        />
      </div>

      <!-- Buttons -->

      <button
        @click="submitReschedule"
        class="mt-4 w-full cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
      >
        Reschedule
      </button>
    </div>
  </Popup>

  <Popup :visible="showProductInfoPopup" @update:visible="showProductInfoPopup = $event">
    <div class="rounded-lg bg-gray-100 p-4 shadow">
      <div class="mb-4">
        <h2 class="text-lg font-semibold">Order #{{ props.orderId }} - Product A</h2>
        <span
          :class="
            props.status === 'On Track' ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'
          "
          class="rounded px-2 py-1 text-sm font-medium"
        >
          {{ props.status }}
        </span>
        <p class="text-sm text-gray-600">Production Line: {{ props.line }}</p>
        <p class="text-sm text-gray-600">Quantity: {{ props.quantity }} units</p>
      </div>

      <!-- Progress Bar -->
      <div class="mb-4 h-2 w-full overflow-hidden rounded bg-gray-300">
        <div class="h-full bg-blue-600" :style="{ width: props.progress + '%' }"></div>
      </div>

      <!-- Stages -->
      <div class="grid grid-cols-2 gap-4">
        <div v-for="(stage, index) in stages" :key="index" class="rounded border bg-white p-3">
          <h3 class="font-semibold">{{ stage.name }}</h3>
          <p class="text-sm text-gray-700">Status: {{ stage.status }}</p>
          <p class="text-sm text-gray-700">Assigned to: {{ stage.team }}</p>
        </div>
      </div>
    </div>
  </Popup>

  <Popup :visible="showProductionOrdersPopup" @update:visible="showProductionOrdersPopup = $event">
  </Popup>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Popup from '@/components/popup.vue'

const showProductionPopup = ref(false)
const showProductionSchedulePopup = ref(false)
const showProductionOrdersPopup = ref(false)
const showReschedulePopup = ref(false)
const showProductsPopup = ref(false)
const showProductInfoPopup = ref(false)

interface Order {
  id: string
  product: string
  quantity: number
  status: 'On Track' | 'Delayed'
  startDate: string
  endDate: string
  productionLine: string
  priority: 'High' | 'Low'
}

const orders = ref<Order[]>([
  {
    id: '#1234',
    product: 'Product A',
    quantity: 500,
    status: 'On Track',
    startDate: '2024-03-15',
    endDate: '2024-03-20',
    productionLine: 'Line 1',
    priority: 'High',
  },
  {
    id: '#1235',
    product: 'Product B',
    quantity: 1000,
    status: 'Delayed',
    startDate: '2024-03-18',
    endDate: '2024-03-22',
    productionLine: 'Line 2',
    priority: 'Low',
  },
])

const searchQuery = ref('')
const selectedStatus = ref('All Statuses')
const selectedLine = ref('All Lines')

const filteredOrders = computed(() => {
  return orders.value.filter((order) => {
    return (
      (selectedStatus.value === 'All Statuses' || order.status === selectedStatus.value) &&
      (selectedLine.value === 'All Lines' || order.productionLine === selectedLine.value) &&
      order.product.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })
})

const getStatusClass = (status: string) => {
  return status === 'On Track' ? 'bg-green-200 text-green-700' : 'bg-red-200 text-red-700'
}

const getPriorityClass = (priority: string) => {
  return priority === 'High' ? 'text-red-600' : 'text-blue-600'
}

const props = defineProps<{
  orderId: string
  schedule: string
  line: string
  quantity: number
  status: 'On Track' | 'Delayed'
  progress: number
  stages: {
    name: string
    status: string
    team: string
  }[]
}>()

const emit = defineEmits(['close', 'submit'])

const newStartTime = ref<string>('')
const newEndTime = ref<string>('')
const reason = ref<string>('')
const note = ref<string>('')

const reasons = [
  'Machine Breakdown',
  'Material Shortage',
  'Staff Unavailable',
  'Power Outage',
  'Other',
]

const submitReschedule = () => {
  const payload = {
    orderId: props.orderId,
    newStartTime: newStartTime.value,
    newEndTime: newEndTime.value,
    reason: reason.value,
    note: note.value,
  }
  emit('submit', payload)
}
const stages = ref([
  { name: 'Material Preparation', status: 'Queued', team: 'Team A' },
  { name: 'Assembly Process', status: 'In Progress', team: 'Team B' },
])
</script>

<style scoped>
th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
</style>
