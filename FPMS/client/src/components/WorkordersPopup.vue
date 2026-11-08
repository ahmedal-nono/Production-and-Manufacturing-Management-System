<template>
  <div>
    <Popup
      :visible="showWorkordersPopup"
      @update:visible="(value: boolean) => emitEvent('update:showWorkordersPopup', value)"
    >
      <div class="w-full max-w-6xl p-6">
        <!-- Header -->
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-2xl font-bold">Work Order Management</h2>
          <button
            @click="showCreateWorkOrderPopup = true"
            class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            + Create Work Order
          </button>
        </div>

        <!-- Filters -->
        <div class="mb-4 flex flex-wrap items-center gap-4">
          <input
            v-model="filters.search"
            type="text"
            placeholder="Search..."
            class="w-48 rounded border px-2 py-1"
          />
          <select v-model="filters.status" class="rounded border px-2 py-1">
            <option>All Statuses</option>
            <option>Active</option>
            <option>Completed</option>
            <option>Pending</option>
            <option>Inactive</option>
          </select>
          <select v-model="filters.priority" class="rounded border px-2 py-1">
            <option>All Priorities</option>
            <option>High</option>
            <option>Medium</option>
            <option>Low</option>
          </select>
          <input v-model="filters.date" type="date" class="rounded border px-2 py-1" />
        </div>

        <!-- Table -->
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr class="">
              <th class="border border-gray-700 px-4 py-2">Work Order ID</th>
              <th class="border border-gray-700 px-4 py-2">Name</th>
              <th class="border border-gray-700 px-4 py-2">Quantity</th>
              <th class="border border-gray-700 px-4 py-2">Due Date</th>
              <th class="border border-gray-700 px-4 py-2">Priority</th>
              <th class="border border-gray-700 px-4 py-2">Production Order</th>
              <th class="border border-gray-700 px-4 py-2">Status</th>
              <th class="border border-gray-700 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(order, index) in filteredOrders"
              :key="index"
              class="border-t bg-white hover:bg-gray-50"
            >
              <td class="border border-gray-700 px-4 py-2">{{ order.id }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ order.name }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ order.quantity_required }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ formatDate(order.due_date) }}</td>
              <td class="border border-gray-700 px-4 py-2">
                <span :class="getPriorityClass(order.priority)"> ● {{ order.priority }} </span>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                {{ getProductionOrderName(order.production_order) }}
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <span
                  :class="getStatusClass(order.status)"
                  class="rounded-full px-2 py-1 text-xs"
                  >{{ order.status || 'Active' }}</span
                >
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <button
                  @click="viewWorkOrder(order.id)"
                  class="m-1 rounded bg-gray-200 px-2 py-1 text-sm hover:bg-gray-300"
                >
                  View
                </button>
                <button
                  @click="editWorkOrder(order.id)"
                  class="m-1 rounded bg-gray-200 px-2 py-1 text-sm hover:bg-gray-300"
                >
                  Edit
                </button>
                <button
                  @click="deleteWorkOrder(order.id)"
                  class="m-1 rounded bg-red-200 px-2 py-1 text-sm hover:bg-red-300"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Popup>

    <Popup :visible="showCreateWorkOrderPopup" @update:visible="showCreateWorkOrderPopup = $event">
      <div class="p-6">
        <div class="mb-6 flex flex-row justify-center">
          <h2 class="w-full text-center text-2xl font-bold">Create New Work Order</h2>
        </div>

        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <!-- Left Section -->
          <div class="space-y-4 md:col-span-2">
            <div>
              <label class="font-semibold">Workorder Name</label>
              <input
                v-model="form.name"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="text"
              />
            </div>

            <div>
              <label class="font-semibold">Select Work Instruction</label>
              <select
                v-model="form.work_instruction"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option disabled value="">Select Work Instruction</option>
                <option
                  v-for="instruction in workInstructions"
                  :key="instruction.id"
                  :value="instruction.id"
                >
                  {{ instruction.title }}
                </option>
              </select>
            </div>

            <div>
              <label class="font-semibold">Assign to Production Line</label>
              <select
                v-model="form.production_line"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option disabled value="">Select Production Line</option>
                <option v-for="line in productionLines" :key="line.id" :value="line.id">
                  {{ line.line_name }}
                </option>
              </select>
            </div>

            <div>
              <label class="font-semibold">Link to Production Order (optional)</label>
              <select
                v-model="form.production_order"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option value="">No linked production order</option>
                <option
                  v-for="order in productionOrders"
                  :key="order.id"
                  :value="order.id"
                >
                  {{ order.order_name }}
                </option>
              </select>
            </div>

            <div>
              <label class="font-semibold">Quantity</label>
              <input
                v-model.number="form.quantity_required"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="number"
              />
            </div>

            <div>
              <label class="font-semibold">Due Date</label>
              <input
                v-model="form.due_date"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="datetime-local"
              />
            </div>

            <div>
              <label class="font-semibold">Priority</label>
              <select
                v-model="form.priority"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>

            <div class="flex gap-3">
              <button
                @click="createWorkOrder"
                class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
              >
                Create Work Order
              </button>
              <button
                @click="showCreateWorkOrderPopup = false"
                class="rounded bg-gray-500 px-4 py-2 text-white hover:bg-gray-600"
              >
                Cancel
              </button>
            </div>
          </div>

          <!-- Right Section -->
          <div class="h-full w-full rounded border bg-white p-4 text-xl">
            <h3 class="mb-2 font-semibold">Work Instruction Preview</h3>
            <p class="">Steps</p>
            <ul
              v-if="previewSteps.length"
              class="mb-4 list-decimal pl-5 text-sm text-gray-700"
            >
              <li v-for="(step, index) in previewSteps" :key="index">
                <input
                  class="m-1 w-full rounded border border-gray-300 px-2 py-1"
                  type="text"
                  readonly
                  :value="step"
                />
              </li>
            </ul>
            <p v-else class="mb-4 text-sm text-gray-500">
              Select a work instruction to preview its steps.
            </p>

            <p class="mb-1 font-medium">Tools required</p>
            <p class="mb-3 text-sm text-gray-700">{{ previewTools || '—' }}</p>

            <p class="mb-1 font-medium">Materials required</p>
            <p class="mb-3 text-sm text-gray-700">{{ previewMaterials || '—' }}</p>

            <p class="font-medium">Linked Production Order</p>
            <p class="text-sm text-gray-700">
              {{ getProductionOrderName(previewProductionOrder) }}
            </p>
          </div>
        </div>
      </div>
    </Popup>

    <Popup :visible="showEditWorkOrderPopup" @update:visible="showEditWorkOrderPopup = $event">
      <div class="p-6">
        <div class="mb-6 flex flex-row justify-center">
          <h2 class="w-full text-center text-2xl font-bold">Edit Work Order</h2>
        </div>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <!-- Left Section -->
          <div class="space-y-4 md:col-span-2">
            <div>
              <label class="font-semibold">Workorder Name</label>
              <input
                v-model="form.name"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="text"
              />
            </div>

            <div>
              <label class="font-semibold">Select Work Instruction</label>
              <select
                v-model="form.work_instruction"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option disabled value="">Select Work Instruction</option>
                <option value="1">Weld & Inspect</option>
                <option value="2">Electrical Assembly</option>
              </select>
            </div>

            <div>
              <label class="font-semibold">Assign to Production Line</label>
              <select
                v-model="form.production_line"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option disabled value="">Select Production Line</option>
                <option v-for="line in productionLines" :key="line.id" :value="line.id">
                  {{ line.line_name }}
                </option>
              </select>
            </div>

            <div>
              <label class="font-semibold">Link to Production Order (optional)</label>
              <select
                v-model="form.production_order"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option value="">No linked production order</option>
                <option
                  v-for="order in productionOrders"
                  :key="order.id"
                  :value="order.id"
                >
                  {{ order.order_name }}
                </option>
              </select>
            </div>

            <div>
              <label class="font-semibold">Quantity</label>
              <input
                v-model.number="form.quantity_required"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="number"
              />
            </div>

            <div>
              <label class="font-semibold">Due Date</label>
              <input
                v-model="form.due_date"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="datetime-local"
              />
            </div>

            <div>
              <label class="font-semibold">Priority</label>
              <select
                v-model="form.priority"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>

            <div class="flex gap-3">
              <button
                @click="updateWorkOrder"
                class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
              >
                Update Work Order
              </button>
              <button
                @click="showEditWorkOrderPopup = false"
                class="rounded bg-gray-500 px-4 py-2 text-white hover:bg-gray-600"
              >
                Cancel
              </button>
            </div>
          </div>

          <!-- Right Section -->
          <div class="h-full w-full rounded border bg-white p-4 text-xl">
            <h3 class="mb-2 font-semibold">Work Instruction Preview</h3>
            <p class="">Steps</p>
            <ul
              v-if="previewSteps.length"
              class="mb-4 list-decimal pl-5 text-sm text-gray-700"
            >
              <li v-for="(step, index) in previewSteps" :key="index">
                <input
                  class="m-1 w-full rounded border border-gray-300 px-2 py-1"
                  type="text"
                  readonly
                  :value="step"
                />
              </li>
            </ul>
            <p v-else class="mb-4 text-sm text-gray-500">
              Select a work instruction to preview its steps.
            </p>

            <p class="mb-1 font-medium">Tools required</p>
            <p class="mb-3 text-sm text-gray-700">{{ previewTools || '—' }}</p>

            <p class="mb-1 font-medium">Materials required</p>
            <p class="mb-3 text-sm text-gray-700">{{ previewMaterials || '—' }}</p>

            <p class="font-medium">Linked Production Order</p>
            <p class="text-sm text-gray-700">
              {{ getProductionOrderName(previewProductionOrder) }}
            </p>
          </div>
        </div>
      </div>
    </Popup>

    <Popup :visible="showViewWorkOrderPopup" @update:visible="showViewWorkOrderPopup = $event">
      <div class="p-6">
        <div class="mb-6 flex flex-row justify-center">
          <h2 class="w-full text-center text-2xl font-bold">View Work Order</h2>
        </div>

        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <!-- Left Section -->
          <div class="space-y-4 md:col-span-2">
            <div>
              <label class="font-semibold">Workorder Name</label>
              <input
                :value="currentWorkOrder?.name"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="text"
                readonly
              />
            </div>

            <div>
              <label class="font-semibold">Work Instruction ID</label>
              <input
                :value="currentWorkOrder?.work_instruction"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="text"
                readonly
              />
            </div>

            <div>
              <label class="font-semibold">Production Line ID</label>
              <input
                :value="currentWorkOrder?.production_line"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="text"
                readonly
              />
            </div>

            <div>
              <label class="font-semibold">Quantity</label>
              <input
                :value="currentWorkOrder?.quantity_required"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="text"
                readonly
              />
            </div>

            <div>
              <label class="font-semibold">Due Date</label>
              <input
                :value="formatDate(currentWorkOrder?.due_date)"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="text"
                readonly
              />
            </div>

            <div>
              <label class="font-semibold">Priority</label>
              <input
                :value="currentWorkOrder?.priority"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="text"
                readonly
              />
            </div>
          </div>

          <!-- Right Section -->
          <div class="h-full w-full rounded border bg-white p-4 text-xl">
            <h3 class="mb-2 font-semibold">Work Instruction Preview</h3>
            <p class="">Steps</p>
            <ul
              v-if="previewSteps.length"
              class="mb-4 list-decimal pl-5 text-sm text-gray-700"
            >
              <li v-for="(step, index) in previewSteps" :key="index">
                <input
                  class="m-1 w-full rounded border border-gray-300 px-2 py-1"
                  type="text"
                  readonly
                  :value="step"
                />
              </li>
            </ul>
            <p v-else class="mb-4 text-sm text-gray-500">
              Select a work instruction to preview its steps.
            </p>

            <p class="mb-1 font-medium">Tools required</p>
            <p class="mb-3 text-sm text-gray-700">{{ previewTools || '—' }}</p>

            <p class="mb-1 font-medium">Materials required</p>
            <p class="mb-3 text-sm text-gray-700">{{ previewMaterials || '—' }}</p>

            <p class="font-medium">Linked Production Order</p>
            <p class="text-sm text-gray-700">
              {{ getProductionOrderName(previewProductionOrder) }}
            </p>
          </div>
        </div>
      </div>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue'
import axios from 'axios'
import Popup from '@/components/popup.vue'
import { baseApiUrl } from '@/api'

// API configuration
const API_BASE_URL = baseApiUrl
const PRODUCTION_LINES_ENDPOINT = `${API_BASE_URL}/production-lines/`
const WORK_ORDERS_ENDPOINT = `${API_BASE_URL}/work_orders/`

// Popup visibility states
const showCreateWorkOrderPopup = ref(false)
const showEditWorkOrderPopup = ref(false)
const showViewWorkOrderPopup = ref(false)

defineProps<{
  showWorkordersPopup: boolean
}>()

const emitEvent = defineEmits([
  'close',
  'submit',
  'update:showWorkordersPopup',
  'update:showCreateWorkOrderPopup',
])

// Filters
const filters = reactive({
  search: '',
  status: 'All Statuses',
  priority: 'All Priorities',
  date: '',
})

// Work orders data
const orders = ref<WorkOrder[]>([])
const productionLines = ref<ProductionLine[]>([])
const productionOrders = ref<ProductionOrder[]>([])
const currentWorkOrder = ref<WorkOrder | null>(null)

// Form data
const form = reactive({
  id: null as number | null,
  name: '',
  quantity_required: 0,
  due_date: '',
  priority: 'Medium',
  work_instruction: '',
  production_line: '',
  production_order: '',
})

// Type definitions
interface WorkOrder {
  id: number
  name: string
  quantity_required: number
  due_date: string
  priority: string
  work_instruction: number
  production_line: number
  production_order?: number | null
  status?: string
}

interface ProductionOrder {
  id: number
  order_name: string
}

interface ProductionLine {
  id: number
  line_name: string // Changed from 'name' to 'line_name'
  capacity_limit: number
  maintenance_schedule: string
  preferred_shift: string
  status: string
  oee_target: number
}

const activeProductionLines = computed(() => {
  return productionLines.value.filter((line) => line.status === 'Active')
})

// Fetch all work orders
const fetchWorkOrders = async () => {
  try {
    const response = await axios.get(WORK_ORDERS_ENDPOINT)
    orders.value = response.data
  } catch (error) {
    console.error('Error fetching work orders:', error)
  }
}

// Create a new work order
const createWorkOrder = async () => {
  try {
    const payload = {
      name: form.name,
      quantity_required: form.quantity_required,
      due_date: form.due_date,
      priority: form.priority,
      work_instruction: parseInt(form.work_instruction as string),
      production_line: parseInt(form.production_line as string),
      production_order: form.production_order
        ? parseInt(form.production_order as string)
        : null,
    }

    const response = await axios.post(WORK_ORDERS_ENDPOINT, payload)
    orders.value.push(response.data)
    showCreateWorkOrderPopup.value = false
    resetForm()
  } catch (error) {
    console.error('Error creating work order:', error)
  }
}

// View a work order
const viewWorkOrder = async (id: number) => {
  try {
    const response = await axios.get(`${WORK_ORDERS_ENDPOINT}${id}/`)
    currentWorkOrder.value = response.data
    showViewWorkOrderPopup.value = true
  } catch (error) {
    console.error('Error fetching work order:', error)
  }
}

// Edit a work order
const editWorkOrder = async (id: number) => {
  try {
    const response = await axios.get(`${WORK_ORDERS_ENDPOINT}${id}/`)
    const order = response.data

    // Populate form with existing data
    form.id = order.id
    form.name = order.name
    form.quantity_required = order.quantity_required
    form.due_date = order.due_date.slice(0, 16) // Convert to datetime-local format
    form.priority = order.priority
    form.work_instruction = order.work_instruction.toString()
    form.production_line = order.production_line.toString()
    form.production_order = order.production_order
      ? order.production_order.toString()
      : ''

    showEditWorkOrderPopup.value = true
  } catch (error) {
    console.error('Error fetching work order for edit:', error)
  }
}

// Update a work order
const updateWorkOrder = async () => {
  if (!form.id) return

  try {
    const payload = {
      name: form.name,
      quantity_required: form.quantity_required,
      due_date: form.due_date,
      priority: form.priority,
      work_instruction: parseInt(form.work_instruction as string),
      production_line: parseInt(form.production_line as string),
      production_order: form.production_order
        ? parseInt(form.production_order as string)
        : null,
    }

    const response = await axios.put(`${WORK_ORDERS_ENDPOINT}${form.id}/`, payload)

    // Update the order in the list
    const index = orders.value.findIndex((order) => order.id === form.id)
    if (index !== -1) {
      orders.value[index] = response.data
    }

    showEditWorkOrderPopup.value = false
    resetForm()
  } catch (error) {
    console.error('Error updating work order:', error)
  }
}

// Delete a work order
const deleteWorkOrder = async (id: number) => {
  if (confirm('Are you sure you want to delete this work order?')) {
    try {
      await axios.delete(`${WORK_ORDERS_ENDPOINT}${id}/`)
      orders.value = orders.value.filter((order) => order.id !== id)
    } catch (error) {
      console.error('Error deleting work order:', error)
    }
  }
}

// Reset form
const resetForm = () => {
  form.id = null
  form.name = ''
  form.quantity_required = 0
  form.due_date = ''
  form.priority = 'Medium'
  form.work_instruction = ''
  form.production_line = ''
  form.production_order = ''
}

// Format date for display
const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString()
}

// Filter work orders
const filteredOrders = computed(() => {
  const searchLower = filters.search.toLowerCase()
  return orders.value.filter((order) => {
    const matchesSearch =
      order.id.toString().includes(searchLower) || order.name.toLowerCase().includes(searchLower)

    const matchesStatus =
      filters.status === 'All Statuses' || (order.status ? order.status === filters.status : true)

    const matchesPriority =
      filters.priority === 'All Priorities' || order.priority === filters.priority

    return matchesSearch && matchesStatus && matchesPriority
  })
})

// Priority and status styling
const getPriorityClass = (priority: string) => {
  switch (priority) {
    case 'High':
      return 'text-red-600'
    case 'Medium':
      return 'text-yellow-600'
    case 'Low':
      return 'text-blue-600'
    default:
      return 'text-gray-600'
  }
}

const getStatusClass = (status?: string) => {
  switch (status) {
    case 'Active':
      return 'bg-green-200 text-green-700'
    case 'Completed':
      return 'bg-blue-200 text-blue-700'
    case 'Pending':
      return 'bg-yellow-200 text-yellow-700'
    case 'Inactive':
      return 'bg-red-200 text-red-700'
    default:
      return 'bg-gray-200 text-gray-700'
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

const PRODUCTION_ORDERS_ENDPOINT = `${API_BASE_URL}/production-orders/`

const fetchProductionOrders = async () => {
  try {
    const response = await axios.get(PRODUCTION_ORDERS_ENDPOINT)
    productionOrders.value = response.data
  } catch (error) {
    console.error('Error fetching production orders:', error)
  }
}

const getProductionOrderName = (id?: number | null) => {
  if (!id) return '—'
  const order = productionOrders.value.find((o) => o.id === id)
  return order ? order.order_name : `#${id}`
}

// Which work instruction to preview: the viewed order when the view popup
// is open, otherwise the instruction selected in the create/edit form.
const previewInstructionId = computed(() => {
  if (showViewWorkOrderPopup.value && currentWorkOrder.value) {
    return currentWorkOrder.value.work_instruction
  }
  return form.work_instruction
})

const previewProductionOrder = computed(() => {
  if (showViewWorkOrderPopup.value && currentWorkOrder.value) {
    return currentWorkOrder.value.production_order
  }
  return form.production_order ? parseInt(form.production_order as string) : null
})

const findInstruction = (id?: number | string) => {
  if (id === undefined || id === null || id === '') return null
  const numericId = typeof id === 'string' ? parseInt(id) : id
  return workInstructions.value.find((instruction) => instruction.id === numericId) ?? null
}

const previewInstruction = computed(() => findInstruction(previewInstructionId.value))

const previewSteps = computed(() => {
  const steps = previewInstruction.value?.task_steps
  if (!steps) return []
  return steps
    .split('\n')
    .map((step) => step.trim())
    .filter((step) => step.length > 0)
})

const previewTools = computed(() => previewInstruction.value?.tools_required ?? '')
const previewMaterials = computed(() => previewInstruction.value?.materials_required ?? '')

const WORK_INSTRUCTIONS_ENDPOINT = `${API_BASE_URL}/work_instructions/`

// Add this interface
interface WorkInstruction {
  id: number
  title: string
  task_steps?: string
  tools_required?: string
  materials_required?: string
}

// Add this reactive property
const workInstructions = ref<WorkInstruction[]>([])

// Add this fetch function
const fetchWorkInstructions = async () => {
  try {
    const response = await axios.get(WORK_INSTRUCTIONS_ENDPOINT)
    workInstructions.value = response.data
  } catch (error) {
    console.error('Error fetching work instructions:', error)
  }
}

// Load all reference data once, in parallel.
onMounted(() => {
  fetchWorkOrders()
  fetchProductionLines()
  fetchWorkInstructions()
  fetchProductionOrders()
})
</script>

<style>
button {
  cursor: pointer;
}
</style>
