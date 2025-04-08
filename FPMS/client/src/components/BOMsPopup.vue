x§
<template>
  <div>
    <Popup
      :visible="showBOMsPopup"
      @update:visible="(value: boolean) => emit('update:showBOMsPopup', value)"
    >
      <div class="rounded-lg bg-white p-4">
        <h1 class="mb-6 text-4xl font-extrabold">Existing BOMs</h1>
        <div class="mb-4 flex flex-wrap items-center justify-between gap-4">
          <div class="relative max-w-md flex-1">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search BOMs..."
              class="w-full rounded-lg border border-gray-300 py-2 pr-4 pl-10 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
            <svg
              class="absolute top-2.5 left-3 h-5 w-5 text-gray-400"
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

          <div class="flex items-center gap-3">
            <select
              v-model="statusFilter"
              class="rounded-lg border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            >
              <option value="all">All Statuses</option>
              <option value="Approved">Approved</option>
              <option value="Draft">Draft</option>
              <option value="Pending">Pending</option>
            </select>

            <select
              v-model="timeFilter"
              class="rounded-lg border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            >
              <option value="all">All Time</option>
              <option value="30">Last 30 Days</option>
              <option value="60">Last 60 Days</option>
              <option value="90">Last 90 Days</option>
            </select>

            <button
              @click="showAddBOMsPopup = true"
              class="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            >
              + New BOM
            </button>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full border text-left">
            <thead>
              <tr class="">
                <th class="p-2">BOM Name</th>
                <th class="p-2">Product Code</th>
                <th class="p-2">Version</th>
                <th class="p-2">Status</th>
                <th class="p-2">Last Updated</th>
                <th class="p-2">Created By</th>
                <th class="p-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="bom in filteredBOMs" :key="bom.id" class="border-t hover:bg-gray-100">
                <td class="p-2">{{ bom.name }}</td>
                <td class="p-2">{{ bom.productCode }}</td>
                <td class="p-2">{{ bom.version }}</td>
                <td class="p-2">
                  <span
                    :class="[
                      'rounded-full px-2 py-1 text-xs font-semibold',
                      bom.status === 'Approved'
                        ? 'bg-green-100 text-green-800'
                        : bom.status === 'Draft'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-blue-100 text-blue-800',
                    ]"
                  >
                    {{ bom.status }}
                  </span>
                </td>
                <td class="p-2">{{ bom.lastUpdated }}</td>
                <td class="p-2">{{ bom.createdBy }}</td>
                <td class="space-x-2 p-2">
                  <button
                    @click="showEditBOMsPopup = true"
                    class="mt-4 cursor-pointer rounded-lg bg-gray-200 p-1.5"
                  >
                    Edit
                  </button>
                  <button
                    @click="viewBOM(bom.id)"
                    class="mt-4 cursor-pointer rounded-lg bg-gray-200 p-1.5"
                  >
                    View
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </Popup>

    <Popup :visible="showAddBOMsPopup" @update:visible="showAddBOMsPopup = $event">
      <div class="">
        <h1 class="mb-6 text-2xl font-bold">Create New Bill of Materials</h1>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Basic Information Section -->
          <div>
            <h2 class="mb-4 text-xl font-semibold">BOM Information</h2>
            <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">BOM Name</label>
                <input
                  v-model="form.bomName"
                  type="text"
                  placeholder="Enter BOM name"
                  class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  required
                />
              </div>

              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">Product Code</label>
                <select
                  v-model="form.productCode"
                  class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  required
                >
                  <option value="" disabled selected>Select Product</option>
                  <option v-for="product in products" :key="product.sku" :value="product.sku">
                    {{ product.name }} ({{ product.sku }})
                  </option>
                </select>
              </div>

              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">Initial Status</label>
                <select
                  v-model="form.status"
                  class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                >
                  <option value="Draft">Draft</option>
                  <option value="Pending Review">Pending Review</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Components & Materials Section -->
          <div>
            <h2 class="mb-4 text-xl font-semibold">Components & Materials</h2>
            <table class="w-full border">
              <thead>
                <tr class="bg-gray-100">
                  <th class="p-2 text-left">Component</th>
                  <th class="p-2 text-left">Part Number</th>
                  <th class="p-2 text-left">Quantity</th>
                  <th class="p-2 text-left">Unit</th>
                  <th class="p-2 text-left">Unit Cost</th>
                  <th class="p-2 text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(component, index) in form.components" :key="index" class="border-t">
                  <td class="p-2">
                    <input
                      v-model="component.name"
                      type="text"
                      placeholder="Component name"
                      class="w-full rounded border border-gray-300 px-2 py-1 focus:ring-1 focus:ring-blue-500 focus:outline-none"
                    />
                  </td>
                  <td class="p-2">
                    <input
                      v-model="component.partNumber"
                      type="text"
                      placeholder="Part number"
                      class="w-full rounded border border-gray-300 px-2 py-1 focus:ring-1 focus:ring-blue-500 focus:outline-none"
                    />
                  </td>
                  <td class="p-2">
                    <div class="flex items-center">
                      <input
                        v-model="component.quantity"
                        type="number"
                        min="0"
                        class="w-full rounded border border-gray-300 px-2 py-1 focus:ring-1 focus:ring-blue-500 focus:outline-none"
                      />
                      <button
                        type="button"
                        @click="adjustQuantity(index, 1)"
                        class="ml-1 px-1 text-gray-600 hover:text-gray-900"
                      >
                        ↑
                      </button>
                    </div>
                  </td>
                  <td class="p-2">
                    <select
                      v-model="component.unit"
                      class="w-full rounded border border-gray-300 px-2 py-1 focus:ring-1 focus:ring-blue-500 focus:outline-none"
                    >
                      <option value="pc">pc</option>
                      <option value="kg">kg</option>
                      <option value="m">m</option>
                      <option value="l">l</option>
                    </select>
                  </td>
                  <td class="p-2">
                    <input
                      v-model="component.unitCost"
                      type="number"
                      min="0"
                      step="0.01"
                      class="w-full rounded border border-gray-300 px-2 py-1 focus:ring-1 focus:ring-blue-500 focus:outline-none"
                    />
                  </td>
                  <td class="p-2">
                    <button
                      type="button"
                      @click="removeComponent(index)"
                      class="text-sm text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <button
              type="button"
              @click="addComponent"
              class="mt-2 text-sm font-medium text-blue-600 hover:text-blue-800"
            >
              + Add Component
            </button>
          </div>

          <!-- Total Cost -->
          <div class="border-t pt-4">
            <p class="text-lg font-semibold">Total Estimated Cost: ${{ totalCost.toFixed(2) }}</p>
          </div>

          <!-- Form Actions -->
          <div class="flex justify-end space-x-3">
            <button
              type="submit"
              class="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            >
              Create BOM
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

const showEditBOMsPopup = ref(false)
const showAddBOMsPopup = ref(false)

const props = defineProps<{
  showBOMsPopup: boolean
}>()
const products = ref([
  {
    name: 'Product A',
    sku: 'SKU001',
    category: 'Category 1',
    bom: 'BOM name',
    workflow: 'Workflow name',
    variantAvailable: true,
  },
  {
    name: 'Product B',
    sku: 'SKU002',
    category: 'Category 2',
    bom: 'BOM name',
    workflow: 'Workflow name',
    variantAvailable: false,
  },
])

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

interface ProductionLineForm {
  lineName: string
  status: string
  capacity: number
  oeeTarget: number
  assignedWorkflows: string[]
}

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

interface BOM {
  id: string
  name: string
  productCode: string
  version: string
  status: 'Approved' | 'Draft' | 'Pending'
  lastUpdated: string
  createdBy: string
}

const searchQuery = ref('')
const statusFilter = ref('all')
const timeFilter = ref('all')

const boms: BOM[] = [
  {
    id: '1',
    name: 'Motor Assembly',
    productCode: 'PROD-002',
    version: 'v2.1',
    status: 'Approved',
    lastUpdated: '2024-03-15',
    createdBy: 'John Doe',
  },
  {
    id: '2',
    name: 'Car Assembly',
    productCode: 'PROD-003',
    version: 'v1.0',
    status: 'Draft',
    lastUpdated: '2024-03-16',
    createdBy: 'Jane Smith',
  },
  // Add more BOMs as needed
]

const filteredBOMs = computed(() => {
  return boms.filter((bom) => {
    // Search filter
    const matchesSearch =
      bom.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      bom.productCode.toLowerCase().includes(searchQuery.value.toLowerCase())

    // Status filter
    const matchesStatus = statusFilter.value === 'all' || bom.status === statusFilter.value

    // Time filter (simplified example)
    const matchesTime =
      timeFilter.value === 'all' ||
      (timeFilter.value === '30' && bom.lastUpdated >= getDateDaysAgo(30))

    return matchesSearch && matchesStatus && matchesTime
  })
})

function getDateDaysAgo(days: number): string {
  const date = new Date()
  date.setDate(date.getDate() - days)
  return date.toISOString().split('T')[0]
}

function viewBOM(id: string) {
  console.log('View BOM:', id)
  // Implement view functionality
}

function openCreateBOM() {
  console.log('Open create BOM dialog')
  // Implement create BOM functionality
}

const bomForm = ref({
  bomName: '',
  productCode: '',
  status: 'Draft',
  components: [
    {
      name: '',
      partNumber: '',
      quantity: 1,
      unit: 'pc',
      unitCost: 0,
    },
  ],
})

const addComponent = () => {
  form.value.components.push({
    name: '',
    partNumber: '',
    quantity: 1,
    unit: 'pc',
    unitCost: 0,
  })
}

const removeComponent = (index: number) => {
  if (form.value.components.length > 1) {
    form.value.components.splice(index, 1)
  }
}

const adjustQuantity = (index: number, amount: number) => {
  form.value.components[index].quantity += amount
  if (form.value.components[index].quantity < 0) {
    form.value.components[index].quantity = 0
  }
}

const totalCost = computed(() => {
  return form.value.components.reduce((total, component) => {
    return total + component.quantity * component.unitCost
  }, 0)
})

const handleSubmit = () => {
  // Handle form submission
  console.log('BOM submitted:', bomForm.value)
  // You would typically call an API here to create the BOM
}

const emit = defineEmits(['close', 'submit', 'update:showBOMsPopup'])
</script>

<style scoped>
th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
</style>
