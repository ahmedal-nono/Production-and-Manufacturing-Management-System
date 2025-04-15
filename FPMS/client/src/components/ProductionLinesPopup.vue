<template>
  <div>
    <Popup
      :visible="showProductionLinesPopup"
      @update:visible="(value: boolean) => emitEvent('update:showProductionLinesPopup', value)"
    >
      <div class="p-5 font-sans">
        <div class="mb-5 flex flex-wrap items-center justify-between gap-4">
          <h1 class="text-2xl font-bold">Production Lines</h1>
          <div class="flex gap-4">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search production lines..."
              class="min-w-[250px] rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              @input="filterLines"
            />
            <select
              v-model="statusFilter"
              @change="filterLines"
              class="rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            >
              <option value="all">All Statuses</option>
              <option value="active">Active</option>
              <option value="maintenance">Maintenance</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-center">
            <thead class="bg-blue-500 text-white">
              <tr class="">
                <th class="border border-gray-700 px-4 py-2">Line Name</th>
                <th class="border border-gray-700 px-4 py-2">Status</th>
                <th class="border border-gray-700 px-4 py-2">Current Output</th>
                <th class="border border-gray-700 px-4 py-2">Capacity Utilization</th>
                <th class="border border-gray-700 px-4 py-2">OEE</th>
                <th class="border border-gray-700 px-4 py-2">Workcenters</th>
                <th class="border border-gray-700 px-4 py-2">Assigned Workflows</th>
                <th class="border border-gray-700 px-4 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="line in filteredLines" :key="line.name" class="border-t hover:bg-gray-100">
                <td class="border border-gray-700 px-4 py-2">{{ line.name }}</td>
                <td class="border border-gray-700 px-4 py-2">
                  <span
                    :class="[
                      'rounded-full px-2 py-1 text-xs font-semibold',
                      line.status === 'Active'
                        ? 'bg-green-100 text-green-800'
                        : line.status === 'Maintenance'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-red-100 text-red-800',
                    ]"
                  >
                    {{ line.status }}
                  </span>
                </td>
                <td class="border border-gray-700 px-4 py-2">
                  {{ line.currentOutput }}/{{ line.capacity }} units
                </td>
                <td class="border border-gray-700 px-4 py-2">{{ line.utilization }}%</td>
                <td class="border border-gray-700 px-4 py-2">{{ line.oee ?? '-' }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ line.workcenters }}</td>
                <td class="border border-gray-700 px-4 py-2">
                  <span v-if="line.workflows?.length">
                    {{ line.workflows.join(', ') }}
                  </span>
                  <span v-else class="text-gray-400">-</span>
                </td>
                <td class="border border-gray-700 px-4 py-2">
                  <button
                    @click="showEditProductionLinesPopup = true"
                    class="cursor-pointer rounded bg-blue-600 px-3 py-1 text-white hover:bg-blue-500"
                  >
                    Edit
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <button
          @click="showAddProductionLinesPopup = true"
          class="mt-4 inline-flex items-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-500 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none"
        >
          + Add New Line
        </button>
      </div>
    </Popup>

    <Popup
      :visible="showAddProductionLinesPopup"
      @update:visible="showAddProductionLinesPopup = $event"
    >
      <div class="">
        <h2 class="mb-6 text-2xl font-bold">Create Production Line</h2>

        <form @submit.prevent="handleProductionLineFormSubmit" class="space-y-6">
          <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div>
              <label class="mb-1 block text-sm font-medium">Line Name</label>
              <input
                v-model="form.lineName"
                type="text"
                placeholder="Enter line name"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Maintenance Schedule</label>
              <input
                v-model="form.maintenanceSchedule"
                type="date"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Capacity Limit (units/hour)</label>
              <input
                v-model="form.capacityLimit"
                type="number"
                placeholder="Enter capacity"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Preferred Shift Pattern</label>
              <select
                v-model="selectedShiftPattern"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                <option value="" disabled selected>Select Shift Pattern</option>
                <option value="8-hour shifts (3 shifts)">8-hour shifts (3 shifts)</option>
                <option value="10-hour shifts (2 shifts)">10-hour shifts (2 shifts)</option>
                <option value="12-hour shifts (2 shifts)">12-hour shifts (2 shifts)</option>
                <option value="Day/Night rotation">Day/Night rotation</option>
                <option value="Continental shift">Continental shift</option>
              </select>
            </div>
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium">Workcenters</label>
            <div class="space-y-3">
              <div
                v-for="(workcenter, index) in form.workcenters"
                :key="index"
                class="flex items-center gap-3"
              >
                <input
                  v-model="workcenter.name"
                  type="text"
                  placeholder="Workcenter name"
                  class="flex-1 rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  required
                />
              </div>
              <button
                type="button"
                @click="addWorkcenter"
                class="mt-2 text-sm font-medium text-blue-600 hover:text-blue-800"
              >
                + Add Workcenter
              </button>
            </div>
          </div>

          <div class="pt-4">
            <button
              type="submit"
              class="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            >
              Save Configuration
            </button>
          </div>
        </form>
      </div>
    </Popup>

    <Popup
      :visible="showEditProductionLinesPopup"
      @update:visible="showEditProductionLinesPopup = $event"
    >
      <div class="">
        <h2 class="mb-6 text-2xl font-bold">Edit Production Line</h2>

        <form @submit.prevent="handleProductionLineFormSubmit" class="space-y-6">
          <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
            <!-- Line Name -->
            <div>
              <label class="mb-1 block text-sm font-medium">Line Name</label>
              <input
                v-model="form.lineName"
                type="text"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>

            <!-- Status Dropdown -->
            <div>
              <label class="mb-1 block text-sm font-medium">Status</label>
              <select
                v-model="form.status"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                <option value="Active">Active</option>
                <option value="Maintenance">Maintenance</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>

            <!-- Capacity -->
            <div>
              <label class="mb-1 block text-sm font-medium">Capacity (units/hr)</label>
              <input
                v-model="form.capacity"
                type="number"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>

            <!-- OEE Target -->
            <div>
              <label class="mb-1 block text-sm font-medium">OEE Target (%)</label>
              <input
                v-model="form.oeeTarget"
                type="number"
                min="0"
                max="100"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
            </div>
          </div>

          <!-- Assign Workflows Section -->
          <div>
            <div class="mb-2 flex items-center justify-between">
              <h3 class="text-lg font-medium">Assign Workflows</h3>
              <div class="relative">
                <input
                  v-model="workflowSearch"
                  type="text"
                  placeholder="Search workflows..."
                  class="rounded-md border border-gray-300 py-2 pr-4 pl-8 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
                <svg
                  class="absolute top-2.5 left-2.5 h-4 w-4 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
              </div>
            </div>

            <div class="space-y-3 rounded-md border p-4">
              <div
                v-for="workflow in filteredWorkflows"
                :key="workflow.id"
                class="flex items-center"
              >
                <input
                  :id="'workflow-' + workflow.id"
                  v-model="form.assignedWorkflows"
                  type="checkbox"
                  :value="workflow.id"
                  class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <label :for="'workflow-' + workflow.id" class="ml-2 text-sm">
                  {{ workflow.name }}
                </label>
              </div>

              <div v-if="filteredWorkflows.length === 0" class="text-sm text-gray-500">
                No workflows found
              </div>
            </div>
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="submit"
              class="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            >
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Popup from '@/components/popup.vue'

const showAddProductionLinesPopup = ref(false)
const showEditProductionLinesPopup = ref(false)

defineProps<{
  showProductionLinesPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showProductionLinesPopup'])

interface ProductionLine {
  name: string
  status: 'Active' | 'Maintenance' | 'Inactive'
  currentOutput: number
  capacity: number
  utilization: number
  oee: number | null
  workcenters: number
  workflows: string[]
}

const allLines: ProductionLine[] = [
  {
    name: 'Line A',
    status: 'Active',
    currentOutput: 850,
    capacity: 1000,
    utilization: 85,
    oee: 88,
    workcenters: 5,
    workflows: ['Workflow X', 'Workflow Y'],
  },
  {
    name: 'Line B',
    status: 'Maintenance',
    currentOutput: 0,
    capacity: 1200,
    utilization: 0,
    oee: null,
    workcenters: 6,
    workflows: ['Workflow Z'],
  },
  {
    name: 'Line C',
    status: 'Inactive',
    currentOutput: 0,
    capacity: 800,
    utilization: 0,
    oee: null,
    workcenters: 4,
    workflows: [],
  },
]

const filterLines = () => {
  filteredLines.value = allLines.filter((line) => {
    const matchesSearch = line.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus =
      statusFilter.value === 'all' || line.status.toLowerCase() === statusFilter.value
    return matchesSearch && matchesStatus
  })
}

const filteredLines = ref(allLines)

interface Workcenter {
  name: string
}

interface ProductionLineForm {
  lineName: string
  maintenanceSchedule: string
  capacityLimit: string
  shiftPattern: string
  workcenters: Workcenter[]
}

const productionLineForm = ref<ProductionLineForm>({
  lineName: '',
  status: 'Active', // Default status
  capacity: 0, // Default capacity
  oeeTarget: 0, // Default OEE target
  assignedWorkflows: [], // Default empty workflows
  maintenanceSchedule: '',
  capacityLimit: '',
  shiftPattern: '',
  workcenters: [{ name: '' }],
})

const addWorkcenter = () => {
  form.value.workcenters.push({ name: '' })
}

const selectedShiftPattern = ref('')

interface Workflow {
  id: string
  name: string
}

interface ProductionLineForm {
  lineName: string
  status: string
  capacity: number
  oeeTarget: number
  assignedWorkflows: string[]
}

// Sample data - replace with your actual data
const sampleWorkflows: Workflow[] = [
  { id: '1', name: 'Workflow X' },
  { id: '2', name: 'Workflow Y' },
  { id: '3', name: 'Workflow Z' },
]

const form = ref<
  ProductionLineForm & {
    bomName: string
    productCode: string
    components: {
      name: string
      partNumber: string
      quantity: number
      unit: string
      unitCost: number
    }[]
  }
>({
  lineName: 'Line A',
  status: 'Active',
  capacity: 1000,
  oeeTarget: 85,
  assignedWorkflows: ['1'], // Default to Workflow X selected
  maintenanceSchedule: '', // Add default value for maintenanceSchedule
  capacityLimit: '', // Add default value for capacityLimit
  shiftPattern: '', // Add default value for shiftPattern
  workcenters: [{ name: '' }], // Add default value for workcenters
  bomName: '', // Add default value for bomName
  productCode: '', // Add default value for productCode
  components: [], // Initialize components as an empty array
})

const workflowSearch = ref('')

const filteredWorkflows = computed(() => {
  return sampleWorkflows.filter((workflow) =>
    workflow.name.toLowerCase().includes(workflowSearch.value.toLowerCase()),
  )
})

const handleProductionLineFormSubmit = () => {
  // Handle form submission
  console.log('Form submitted:', productionLineForm.value)
  // You would typically call an API here to update the production line
}

const searchQuery = ref('')
const statusFilter = ref('all')
</script>

<style>
button {
  cursor: pointer;
}
</style>
