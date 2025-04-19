<template>
  <Popup
    :visible="showJobCardsPopup"
    @update:visible="(value: boolean) => emitEvent('update:showJobCardsPopup', value)"
  >
    <div class="p-6">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <h1 class="text-2xl font-bold">Job Cards</h1>
        <span class="flex items-center gap-1 text-sm text-gray-600">
          <span class="h-2 w-2 rounded-full bg-green-500"></span> 
          Synced {{ lastSynced }}
        </span>
      </div>

      <!-- Search and Filters -->
      <div class="mb-6 flex flex-wrap gap-4">
        <input
          v-model="filters.search"
          type="text"
          placeholder="Search job cards..."
          class="w-full max-w-md rounded border px-3 py-2 text-sm"
        />

        <select v-model="filters.status" class="rounded border px-3 py-2 text-sm">
          <option value="">All Statuses</option>
          <option v-for="status in statusOptions" :key="status" :value="status">
            {{ status }}
          </option>
        </select>

        <select v-model="filters.priority" class="rounded border px-3 py-2 text-sm">
          <option value="">All Priorities</option>
          <option>High</option>
          <option>Medium</option>
          <option>Low</option>
        </select>

        <select v-model="filters.line" class="rounded border px-3 py-2 text-sm">
          <option value="">All Production Lines</option>
          <option v-for="line in productionLines" :key="line.id" :value="line.id">
            {{ line.line_name }}
          </option>
        </select>

        <input v-model="filters.fromDate" type="date" class="rounded border px-3 py-2 text-sm" />
        <input v-model="filters.toDate" type="date" class="rounded border px-3 py-2 text-sm" />
      </div>

      <!-- Job Cards Grid -->
      <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        <!-- Job Card -->
        <div
          class="w-full rounded-lg border bg-white p-4 shadow-sm"
          v-for="card in filteredJobCards"
          :key="card.id"
        >
          <div class="mb-2 flex items-center justify-between">
            <h2 class="font-semibold">JC-{{ card.id }}</h2>
            <span 
              class="rounded-full px-3 py-1 text-xs font-medium"
              :class="getStatusClass(card.status)"
            >
              {{ card.status }}
            </span>
          </div>

          <div class="mb-3 space-y-1 text-sm">
            <p><strong>Task:</strong> {{ card.task_name }}</p>
            <p><strong>Work Order:</strong> WO-{{ card.work_order }}</p>
            <p><strong>Assigned To:</strong> {{ getEmployeeName(card.assigned_to) }}</p>
            <p class="flex items-center gap-2">
              <strong>Priority:</strong>
              <span
                :class="{
                  'h-3 w-3 rounded-full bg-red-500': card.priority === 'High',
                  'h-3 w-3 rounded-full bg-yellow-500': card.priority === 'Medium',
                  'h-3 w-3 rounded-full bg-green-500': card.priority === 'Low',
                }"
              ></span>
              {{ card.priority }}
            </p>
            <p><strong>Tools:</strong> {{ card.required_tools }}</p>
            <p><strong>Materials:</strong> {{ card.required_materials }}</p>
          </div>

          <div class="flex gap-2">
            <button 
              @click="viewJobCardDetails(card.id)"
              class="rounded bg-blue-600 px-3 py-1 text-sm text-white hover:bg-blue-500"
            >
              View Details
            </button>
            <button 
              @click="showUpdateStatusModal(card)"
              class="rounded bg-green-600 px-3 py-1 text-sm text-white hover:bg-green-500"
            >
              Update Status
            </button>
          </div>
        </div>
      </div>
    </div>
  </Popup>

  <!-- Job Card Details Modal -->
  <JobCardDetailsModal 
    v-if="selectedJobCard"
    :jobCard="selectedJobCard"
    :visible="showDetailsModal"
    @close="showDetailsModal = false"
  />

  <!-- Update Status Modal -->
  <UpdateStatusModal
    v-if="statusUpdateCard"
    :jobCard="statusUpdateCard"
    :visible="showStatusModal"
    @close="showStatusModal = false"
    @status-updated="handleStatusUpdate"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Popup from '@/components/popup.vue'
import JobCardDetailsModal from './JobCardDetailsModal.vue'
import UpdateStatusModal from './UpdateStatusModal.vue'

const API_BASE_URL = 'http://localhost:8000/api'
const JOB_CARDS_ENDPOINT = `${API_BASE_URL}/job_cards/`
const PRODUCTION_LINES_ENDPOINT = `${API_BASE_URL}/production-lines/`
const EMPLOYEES_ENDPOINT = `${API_BASE_URL}/employees/`

defineProps<{
  showJobCardsPopup: boolean
}>()

const emitEvent = defineEmits(['update:showJobCardsPopup'])

// Data
const jobCards = ref<any[]>([])
const productionLines = ref<any[]>([])
const employees = ref<any[]>([])
const lastSynced = ref<string>('just now')
const selectedJobCard = ref<any>(null)
const statusUpdateCard = ref<any>(null)

// UI States
const showDetailsModal = ref(false)
const showStatusModal = ref(false)

// Filters
const filters = ref({
  search: '',
  status: '',
  priority: '',
  line: '',
  fromDate: '',
  toDate: '',
})

// Options
const statusOptions = ref([
  'Not Started',
  'In Progress',
  'Completed',
  'On Hold',
  'Cancelled'
])

// Fetch data
const fetchJobCards = async () => {
  try {
    const response = await axios.get(JOB_CARDS_ENDPOINT)
    jobCards.value = response.data
    lastSynced.value = new Date().toLocaleTimeString()
  } catch (error) {
    console.error('Error fetching job cards:', error)
  }
}

const fetchProductionLines = async () => {
  try {
    const response = await axios.get(PRODUCTION_LINES_ENDPOINT)
    productionLines.value = response.data
  } catch (error) {
    console.error('Error fetching production lines:', error)
  }
}

const fetchEmployees = async () => {
  try {
    const response = await axios.get(EMPLOYEES_ENDPOINT)
    employees.value = response.data
  } catch (error) {
    console.error('Error fetching employees:', error)
  }
}

// Computed
const filteredJobCards = computed(() => {
  return jobCards.value.filter((card) => {
    const matchSearch =
      filters.value.search === '' ||
      card.task_name.toLowerCase().includes(filters.value.search.toLowerCase()) ||
      getEmployeeName(card.assigned_to).toLowerCase().includes(filters.value.search.toLowerCase())

    const matchStatus =
      filters.value.status === '' || card.status === filters.value.status

    const matchPriority =
      filters.value.priority === '' || card.priority === filters.value.priority

    const matchLine =
      filters.value.line === '' || card.production_line === filters.value.line

    return matchSearch && matchStatus && matchPriority && matchLine
  })
})

// Helpers
const getEmployeeName = (employeeId: number) => {
  const employee = employees.value.find(e => e.id === employeeId)
  return employee ? `${employee.first_name} ${employee.last_name}` : 'Unassigned'
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'Not Started': return 'bg-gray-200 text-gray-800'
    case 'In Progress': return 'bg-blue-200 text-blue-800'
    case 'Completed': return 'bg-green-200 text-green-800'
    case 'On Hold': return 'bg-yellow-200 text-yellow-800'
    case 'Cancelled': return 'bg-red-200 text-red-800'
    default: return 'bg-gray-200 text-gray-800'
  }
}

// Actions
const viewJobCardDetails = async (id: number) => {
  try {
    const response = await axios.get(`${JOB_CARDS_ENDPOINT}${id}/`)
    selectedJobCard.value = response.data
    showDetailsModal.value = true
  } catch (error) {
    console.error('Error fetching job card details:', error)
  }
}

const showUpdateStatusModal = (card: any) => {
  statusUpdateCard.value = card
  showStatusModal.value = true
}

const handleStatusUpdate = (updatedCard: any) => {
  const index = jobCards.value.findIndex(c => c.id === updatedCard.id)
  if (index !== -1) {
    jobCards.value[index] = updatedCard
  }
  showStatusModal.value = false
}

// Initialize
onMounted(() => {
  fetchJobCards()
  fetchProductionLines()
  fetchEmployees()
})
</script>

<style>
button {
  cursor: pointer;
}
</style>