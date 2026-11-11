<template>
  <div>
    <!-- Production Orders Popup -->
    <Popup
      :visible="props.showProductionSchedulePopup"
      @update:visible="(value: boolean) => emit('update:showProductionSchedulePopup', value)"
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
            <option>Pending</option>
            <option>In Progress</option>
            <option>Completed</option>
            <option>Cancelled</option>
          </select>
          <select v-model="selectedLine" class="rounded border p-2">
            <option>All Lines</option>
            <option v-for="line in productionLines" :key="line" :value="line">
              {{ line }}
            </option>
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
              <th v-if="userRole === 'Production Manager'" class="border px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <SkeletonRows
              v-if="ordersLoading"
              :rows="4"
              :cols="userRole === 'Production Manager' ? 9 : 8"
            />
            <tr
              v-for="order in filteredOrders"
              v-show="!ordersLoading"
              :key="order.id"
            >
              <td @click="showProductInfo(order)" class="border px-4 py-2 cursor-pointer">
                {{ order.id }}
              </td>
              <td class="border px-4 py-2">{{ getProductName(order.product) }}</td>
              <td class="border px-4 py-2">{{ order.quantity }}</td>
              <td class="border px-4 py-2">
                <span
                  class="rounded px-2 py-1"
                  :class="getStatusClass(order.status)"
                >
                  {{ order.status }}
                </span>
              </td>
              <td class="border px-4 py-2">
                <input
                  type="date"
                  :value="formatDateForInput(order.start_date)"
                  disabled
                  class="w-full rounded border p-1"
                />
              </td>
              <td class="border px-4 py-2">
                <input
                  type="date"
                  :value="formatDateForInput(order.end_date)"
                  disabled
                  class="w-full rounded border p-1"
                />
              </td>
              <td class="border px-4 py-2">Line {{ order.production_line }}</td>
              <td class="border px-4 py-2">
                <span :class="getPriorityClass(order.priority)"> ● {{ order.priority }} </span>
              </td>
              <td v-if="userRole === 'Production Manager'" class="space-x-1 border px-4 py-2">
                <button
                  @click="openReschedulePopup(order)"
                  class="rounded bg-blue-600 px-2 py-1 text-white hover:bg-blue-700"
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
          Reschedule Order: <span class="font-bold">{{ currentOrder?.id }}</span>
          <p class="mt-2 mb-1 text-sm text-gray-600">
            Current Schedule: <span class="font-medium">{{ formatDate(currentOrder?.end_date ?? '') }}</span>
          </p>
          <p class="mb-4 text-sm text-gray-600">
            Production Line:
            <span class="font-medium">Line {{ currentOrder?.production_line }}</span>
          </p>
        </h2>
        <div>
          <label class="mb-1 block text-sm">New Start Time</label>
          <input v-model="newStartTime" type="datetime-local" class="rounded border p-2 w-full" />
          <label class="mt-2 mb-1 block text-sm">New End Time</label>
          <input v-model="newEndTime" type="datetime-local" class="rounded border p-2 w-full" />
        </div>
        <div class="mt-2 mb-4">
          <label class="mb-1 text-sm">Reason for Reschedule</label>
          <select v-model="reason" class="w-full rounded border p-2">
            <option value="">Select a reason</option>
            <option v-for="r in reasons" :key="r" :value="r">{{ r }}</option>
          </select>
        </div>
        <div class="mb-4">
          <label class="mb-1 text-sm">Additional Notes</label>
          <input v-model="note" type="text" class="w-full rounded border p-2" />
        </div>
        <div class="flex space-x-2">
          <button
            @click="submitReschedule"
            class="mt-4 w-full rounded-lg bg-blue-600 p-1.5 text-white hover:bg-blue-700"
          >
            Reschedule
          </button>
          <button
            @click="showReschedulePopup = false"
            class="mt-4 w-full rounded-lg bg-gray-500 p-1.5 text-white hover:bg-gray-600"
          >
            Cancel
          </button>
        </div>
      </div>
    </Popup>

    <!-- Product Info Popup -->
    <Popup :visible="showProductInfoPopup" @update:visible="showProductInfoPopup = $event">
      <div class="rounded-lg bg-gray-100 p-4 shadow">
        <h2 class="text-lg font-semibold">Order #{{ selectedProductInfo?.orderId }} - {{ selectedProductInfo?.productName }}</h2>
        <span
          :class="getStatusClass(selectedProductInfo?.status || '')"
          class="rounded px-2 py-1 text-sm font-medium"
        >
          {{ selectedProductInfo?.status }}
        </span>
        <p class="text-sm text-gray-600">Production Line: {{ selectedProductInfo?.line }}</p>
        <p class="text-sm text-gray-600">Quantity: {{ selectedProductInfo?.quantity }} units</p>
        <div class="my-4 h-2 w-full rounded bg-gray-300">
          <div class="h-full bg-blue-600" :style="{ width: selectedProductInfo?.progress + '%' }"></div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div
            v-for="(stage, index) in selectedProductInfo?.stages"
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
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Popup from '@/components/popup.vue'
import SkeletonRows from '@/components/SkeletonRows.vue'
import { useUserStore } from '@/stores/user'
import { baseApiUrl } from '@/api'

const API_BASE_URL = `${baseApiUrl}/`

interface ProductionOrder {
  id: number
  order_name: string
  product: number
  quantity: number
  status: string
  start_date: string
  end_date: string
  production_line: number
  priority: string
}

interface Product {
  id: number
  name: string
  sku: string
  category: string
  specifications: string
}

interface RescheduleRecord {
  id: number
  production_order: number
  new_start_time: string
  new_end_time: string
  reason_for_rescheduling: string
  notes: string
}

interface ProductInfo {
  orderId: number
  productName: string
  status: string
  line: string
  quantity: number
  progress: number
  stages: {
    name: string
    status: string
    team: string
  }[]
}

const props = defineProps<{
  showProductionSchedulePopup: boolean
}>()

const emit = defineEmits(['update:showProductionSchedulePopup'])

const userStore = useUserStore()
const userRole = userStore.user?.role

// Data
const orders = ref<ProductionOrder[]>([])
const products = ref<Product[]>([])
const productionLines = ref<string[]>(['1', '2', '3'])
const rescheduleRecords = ref<RescheduleRecord[]>([])
const selectedProductInfo = ref<ProductInfo | null>(null)

// UI State
const showReschedulePopup = ref(false)
const showProductInfoPopup = ref(false)
const currentOrder = ref<ProductionOrder | null>(null)
const isLoading = ref(false)
const ordersLoading = ref(false)

// Filters
const selectedStatus = ref('All Statuses')
const selectedLine = ref('All Lines')
const searchQuery = ref('')

// Reschedule Form
const newStartTime = ref('')
const newEndTime = ref('')
const reason = ref('')
const note = ref('')
const reasons = [
  'Machine Breakdown',
  'Material Shortage',
  'Staff Unavailable',
  'Power Outage',
  'Other',
]

// Computed
const filteredOrders = computed(() => {
  return orders.value.filter((order) => {
    const matchesStatus = selectedStatus.value === 'All Statuses' || order.status === selectedStatus.value
    const matchesLine = selectedLine.value === 'All Lines' || order.production_line.toString() === selectedLine.value
    const matchesSearch = order.order_name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                         getProductName(order.product).toLowerCase().includes(searchQuery.value.toLowerCase())
    
    return matchesStatus && matchesLine && matchesSearch
  })
})

// Methods
const getStatusClass = (status: string) => {
  switch (status) {
    case 'Completed':
      return 'bg-green-200 text-green-700'
    case 'In Progress':
      return 'bg-blue-200 text-blue-700'
    case 'Cancelled':
      return 'bg-red-200 text-red-700'
    default: // Pending
      return 'bg-yellow-200 text-yellow-700'
  }
}

const getPriorityClass = (priority: string) => {
  return priority === 'High' ? 'text-red-600' : 'text-blue-600'
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}

const formatDateForInput = (dateString: string) => {
  if (!dateString) return ''
  return dateString.split('T')[0]
}

const getProductName = (productId: number) => {
  const product = products.value.find(p => p.id === productId)
  return product ? product.name : 'Unknown Product'
}

const showProductInfo = (order: ProductionOrder) => {
  selectedProductInfo.value = {
    orderId: order.id,
    productName: getProductName(order.product),
    status: order.status,
    line: `Line ${order.production_line}`,
    quantity: order.quantity,
    progress: calculateProgress(order),
    stages: [
      { name: 'Material Preparation', status: 'Completed', team: 'Team A' },
      { name: 'Assembly Process', status: order.status === 'Completed' ? 'Completed' : 'In Progress', team: 'Team B' }
    ]
  }
  showProductInfoPopup.value = true
}

const calculateProgress = (order: ProductionOrder) => {
  switch (order.status) {
    case 'Pending': return 20
    case 'In Progress': return 60
    case 'Completed': return 100
    case 'Cancelled': return 0
    default: return 0
  }
}

const openReschedulePopup = (order: ProductionOrder) => {
  currentOrder.value = order
  newStartTime.value = order.start_date.slice(0, 16)
  newEndTime.value = order.end_date.slice(0, 16)
  reason.value = ''
  note.value = ''
  showReschedulePopup.value = true
}

const submitReschedule = async () => {
  if (!currentOrder.value) return

  try {
    isLoading.value = true
    
    // Update production order dates
    const updatedOrder = {
      ...currentOrder.value,
      start_date: newStartTime.value,
      end_date: newEndTime.value
    }

    await axios.put(`${API_BASE_URL}production-orders/${currentOrder.value.id}/`, updatedOrder)

    // Create reschedule record
    const rescheduleData = {
      production_order: currentOrder.value.id,
      new_start_time: newStartTime.value,
      new_end_time: newEndTime.value,
      reason_for_rescheduling: reason.value,
      notes: note.value
    }

    await axios.post(`${API_BASE_URL}rescheduling/`, rescheduleData)

    // Refresh data
    await fetchOrders()
    await fetchRescheduleRecords()
    
    showReschedulePopup.value = false
  } catch (error) {
    console.error('Error rescheduling order:', error)
  } finally {
    isLoading.value = false
  }
}

// API Calls
const fetchOrders = async () => {
  ordersLoading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}production-orders/`)
    orders.value = response.data
  } catch (error) {
    console.error('Error fetching production orders:', error)
  } finally {
    ordersLoading.value = false
  }
}

const fetchProducts = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}products/`)
    products.value = response.data
  } catch (error) {
    console.error('Error fetching products:', error)
  }
}

const fetchRescheduleRecords = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}rescheduling/`)
    rescheduleRecords.value = response.data
  } catch (error) {
    console.error('Error fetching reschedule records:', error)
  }
}

// Initialize
onMounted(() => {
  fetchOrders()
  fetchProducts()
  fetchRescheduleRecords()
})
</script>

<style>
button {
  cursor: pointer;
}
</style>