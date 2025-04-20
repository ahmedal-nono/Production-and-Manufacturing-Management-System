<template>
  <div>
    <Popup
      :visible="showProductionSchedulePopup"
      @update:visible="(value: boolean) => emitEvent('update:showProductionSchedulePopup', value)"
    >
      <div>
        <h2 class="mb-4 text-xl font-semibold">Production Orders</h2>

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

        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr>
              <th class="border px-4 py-2">Order ID</th>
              <th class="border px-4 py-2">Product</th>
              <th class="border px-4 py-2">Quantity</th>
              <th class="border px-4 py-2">Status</th>
              <th class="border px-4 py-2">Start Date</th>
              <th class="border px-4 py-2">End Date</th>
              <th class="border px-4 py-2">Line</th>
              <th class="border px-4 py-2">Priority</th>
              <th class="border px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in filteredOrders" :key="order.id">
              <td @click="showProductInfoPopup = true" class="border px-4 py-2">
                {{ order.id }}
              </td>
              <td class="border px-4 py-2">{{ order.product }}</td>
              <td class="border px-4 py-2">{{ order.quantity }}</td>
              <td class="border px-4 py-2">
                <span
                  @click="showProductInfoPopup = true"
                  class="rounded px-2 py-1"
                  :class="getStatusClass(order.status)"
                >
                  {{ order.status }}
                </span>
              </td>
              <td class="border px-4 py-2">
                <input
                  type="date"
                  :value="order.startDate"
                  disabled
                  class="w-full rounded border p-1"
                />
              </td>
              <td class="border px-4 py-2">
                <input
                  type="date"
                  :value="order.endDate"
                  disabled
                  class="w-full rounded border p-1"
                />
              </td>
              <td class="border px-4 py-2">{{ order.productionLine }}</td>
              <td class="border px-4 py-2">
                <span :class="getPriorityClass(order.priority)"> ● {{ order.priority }} </span>
              </td>
              <td class="space-x-1 border px-4 py-2">
                <button
                  @click="
                    () => {
                      currentProduction = order
                      showReschedulePopup = true
                    }
                  "
                  class="rounded bg-blue-600 px-2 py-1 text-white"
                >
                  Reschedule
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Popup>

    <!-- Reschedule Popup -->
    <Popup :visible="showReschedulePopup" @update:visible="showReschedulePopup = $event">
      <div>
        <h2 class="mb-1 text-xl font-bold">
          Reschedule Order: <span class="font-bold">{{ currentProduction?.id }}</span>
          <p class="mt-2 mb-1 text-sm text-gray-600">
            Current Schedule: <span class="font-medium">{{ currentProduction?.endDate }}</span>
          </p>
          <p class="mb-4 text-sm text-gray-600">
            Production Line:
            <span class="font-medium">{{ currentProduction?.productionLine }}</span>
          </p>
        </h2>
        <div>
          <label class="mb-1 block text-sm">New Start Time</label>
          <input v-model="newStartTime" type="date" class="rounded border p-2" />
          <label class="mt-2 mb-1 block text-sm">New End Time</label>
          <input v-model="newEndTime" type="date" class="rounded border p-2" />
        </div>
        <div class="mt-2 mb-4">
          <label class="mb-1 text-sm">Reason for Reschedule</label>
          <select v-model="reason" class="w-full rounded border p-2">
            <option value="" disabled>Select a reason</option>
            <option v-for="r in reasons" :key="r" :value="r">{{ r }}</option>
          </select>
        </div>
        <div class="mb-4">
          <label class="mb-1 text-sm">Additional Notes</label>
          <input v-model="note" type="text" class="w-full rounded border p-2" />
        </div>
        <button
          @click="() => submitReschedule(currentProduction.id)"
          class="mt-4 w-full rounded-lg bg-blue-600 p-1.5 text-white"
        >
          Reschedule
        </button>
      </div>
    </Popup>

    <!-- Product Info Popup -->
    <Popup :visible="showProductInfoPopup" @update:visible="showProductInfoPopup = $event">
      <div class="rounded-lg bg-gray-100 p-4 shadow">
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
        <div class="my-4 h-2 w-full rounded bg-gray-300">
          <div class="h-full bg-blue-600" :style="{ width: props.progress + '%' }"></div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div
            v-for="(stage, index) in props.stages"
            :key="index"
            class="rounded border bg-white p-3"
          >
            <h3 class="font-semibold">{{ stage.name }}</h3>
            <p class="text-sm">Status: {{ stage.status }}</p>
            <p class="text-sm">Assigned to: {{ stage.team }}</p>
          </div>
        </div>
      </div>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { useOrdersStore } from '@/stores/useOrders'
import { computed, ref } from 'vue'
import Popup from '@/components/popup.vue'

// const { orders, deleteOrder, updateOrderDates }
const ordersStore = useOrdersStore()

const showReschedulePopup = ref(false)
const showProductInfoPopup = ref(false)

const selectedStatus = ref('All Statuses')
const selectedLine = ref('All Lines')
const searchQuery = ref('')
const currentProduction = {}

const filteredOrders = computed(() => {
  return ordersStore.orders.filter((order) => {
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
  showProductionSchedulePopup: boolean
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

const emitEvent = defineEmits([
  'close',
  'submit',
  'update:showProductionSchedulePopup',
  'update-dates',
])

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

const submitReschedule = (id) => {
  console.log({ id })

  const success = ordersStore.updateOrderDates(id, newStartTime.value, newEndTime.value)
}

const stages = ref([
  { name: 'Material Preparation', status: 'Queued', team: 'Team A' },
  { name: 'Assembly Process', status: 'In Progress', team: 'Team B' },
])
</script>

<style>
button {
  cursor: pointer;
}
</style>
