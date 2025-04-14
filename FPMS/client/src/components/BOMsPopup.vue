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
              class="w-full rounded-lg border border-gray-300 py-2 pr-4 pl-10"
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
            <select v-model="statusFilter" class="rounded-lg border border-gray-300 px-3 py-2">
              <option value="all">All Statuses</option>
              <option value="Approved">Approved</option>
              <option value="Draft">Draft</option>
              <option value="Pending">Pending</option>
            </select>

            <select v-model="timeFilter" class="rounded-lg border border-gray-300 px-3 py-2">
              <option value="all">All Time</option>
              <option value="30">Last 30 Days</option>
              <option value="60">Last 60 Days</option>
              <option value="90">Last 90 Days</option>
            </select>

            <button
              @click="showAddBOMsPopup = true"
              class="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
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
                    @click="showViewBOMsPopup = true"
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
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  required
                />
              </div>

              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">Product Code</label>
                <select
                  v-model="form.productCode"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
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
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
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
                      class="w-full rounded border border-gray-300 px-2 py-1"
                    />
                  </td>
                  <td class="p-2">
                    <input
                      v-model="component.partNumber"
                      type="text"
                      placeholder="Part number"
                      class="w-full rounded border border-gray-300 px-2 py-1"
                    />
                  </td>
                  <td class="p-2">
                    <div class="flex items-center">
                      <input
                        v-model="component.quantity"
                        type="number"
                        min="0"
                        class="w-full rounded border border-gray-300 px-2 py-1"
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
                      class="w-full rounded border border-gray-300 px-2 py-1"
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
                      class="w-full rounded border border-gray-300 px-2 py-1"
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
              class="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
            >
              Create BOM
            </button>
          </div>
        </form>
      </div>
    </Popup>

    <Popup :visible="showEditBOMsPopup" @update:visible="showEditBOMsPopup = $event">
      <div>
        <div class="flex flex-col">
          <h1 class="text-2xl font-bold text-blue-500">{{ boms[0].name }}</h1>
          <div class="flex justify-between">
            <p class="mt-2 mb-6 w-fit rounded-2xl border bg-blue-100 p-2 text-sm text-blue-500">
              Current Version v2.1
            </p>
            <p class="flex justify-end">Approved</p>
          </div>
        </div>

        <form @submit.prevent="handleUpdate" class="space-y-6">
          <!-- BOM Information -->
          <div>
            <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">BOM Name</label>
                <input
                  v-model="form.bomName"
                  type="text"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  required
                />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">Product Code</label>
                <input
                  v-model="form.productCode"
                  type="text"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  required
                />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">Base Quantity</label>
                <input
                  v-model="form.baseQuantity"
                  type="number"
                  min="1"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  required
                />
              </div>
            </div>
          </div>

          <!-- Components Table -->
          <div>
            <h2 class="mb-4 text-xl font-semibold">Component Structure</h2>
            <table class="w-full border text-sm">
              <thead class="bg-gray-100">
                <tr>
                  <th class="p-2 text-left">Level</th>
                  <th class="p-2 text-left">Component</th>
                  <th class="p-2 text-left">Part Number</th>
                  <th class="p-2 text-left">Quantity</th>
                  <th class="p-2 text-left">Unit</th>
                  <th class="p-2 text-left">Unit Cost</th>
                  <th class="p-2 text-left">Total Cost</th>
                  <th class="p-2 text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(component, index) in components" :key="index" class="border-t">
                  <td class="p-2">
                    {{ component.level }}
                  </td>
                  <td class="p-2">
                    {{ component.name }}
                  </td>
                  <td class="p-2">
                    {{ component.part }}
                  </td>
                  <td class="p-2">
                    {{ component.quantity }}
                  </td>
                  <td class="p-2">
                    {{ component.unit }}
                  </td>
                  <td class="p-2">${{ component.unitCost.toFixed(2) }}</td>
                  <td class="p-2">${{ (component.quantity * component.unitCost).toFixed(2) }}</td>
                  <td class="p-2">
                    <button
                      type="button"
                      @click="editComponent(index)"
                      class="cursor-pointer rounded bg-blue-600 px-4 py-2 text-sm text-white"
                    >
                      Edit
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Total -->
          <div class="border-t pt-4 text-right">
            <p class="text-lg font-semibold">Total Estimated Cost: ${{ totalCost.toFixed(2) }}</p>
          </div>

          <!-- Version Management -->
          <div class="rounded-md bg-yellow-100 p-4">
            <h4 class="font-bold">Version Management</h4>
            <div class="mt-2 space-y-2">
              <label class="flex items-center space-x-2">
                <input
                  type="radio"
                  value="update"
                  v-model="form.versionOption"
                  class="text-blue-600"
                  name="version"
                />
                <span>Update current version (v2.1)</span>
              </label>
              <label class="flex items-center space-x-2">
                <input
                  type="radio"
                  value="new"
                  v-model="form.versionOption"
                  class="text-blue-600"
                  name="version"
                />
                <span>Create new version (v2.2)</span>
              </label>
            </div>
          </div>
          <h1 class="mb-4 text-2xl font-bold">Add New Component</h1>
          <div class="mt-4 grid grid-cols-3 gap-4 text-sm">
            <div>
              <label class="mr-2 font-semibold">Component/Material</label>
              <input type="text" class="mt-2 w-full rounded border border-gray-300 px-2 py-1" />
            </div>
            <div>
              <label class="mr-2 font-semibold">Quantity</label>
              <input type="number" class="mt-2 w-full rounded border border-gray-300 px-2 py-1" />
            </div>
            <div>
              <label class="mr-2 font-semibold">Unit of Measure</label>
              <select class="mt-2 w-full rounded border border-gray-300 px-2 py-1">
                <option>pc</option>
                <option>kg</option>
              </select>
            </div>
            <button class="rounded bg-blue-600 px-4 py-2 text-white">Add to BOM</button>
            <button class="rounded bg-gray-300 px-4 py-2">Cancel</button>
          </div>
          <!-- Action Buttons -->
          <div class="flex justify-end gap-4 pt-4">
            <button
              type="submit"
              class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
            >
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </Popup>
    <Popup :visible="showViewBOMsPopup" @update:visible="showViewBOMsPopup = $event">
      <div>
        <div class="flex flex-col">
          <h1 class="text-2xl font-bold text-blue-500">{{ boms[0].name }}</h1>
          <div class="flex justify-between">
            <p class="mt-2 mb-6 w-fit rounded-2xl border bg-blue-100 p-2 text-sm text-blue-500">
              Current Version v2.1
            </p>
            <p class="flex justify-end">Approved</p>
          </div>
        </div>

        <form @submit.prevent="handleUpdate" class="space-y-6">
          <!-- BOM Information -->
          <div>
            <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">BOM Name</label>
                <input
                  v-model="form.bomName"
                  type="text"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  required
                />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">Product Code</label>
                <input
                  v-model="form.productCode"
                  type="text"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  required
                />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">Base Quantity</label>
                <input
                  v-model="form.baseQuantity"
                  type="number"
                  min="1"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  required
                />
              </div>
            </div>
          </div>

          <!-- Components Table -->
          <div>
            <h2 class="mb-4 text-xl font-semibold">Component Structure</h2>
            <table class="w-full border text-sm">
              <thead class="bg-gray-100">
                <tr>
                  <th class="p-2 text-left">Level</th>
                  <th class="p-2 text-left">Component</th>
                  <th class="p-2 text-left">Part Number</th>
                  <th class="p-2 text-left">Quantity</th>
                  <th class="p-2 text-left">Unit</th>
                  <th class="p-2 text-left">Unit Cost</th>
                  <th class="p-2 text-left">Total Cost</th>
                  <th class="p-2 text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(component, index) in components" :key="index" class="border-t">
                  <td class="p-2">
                    {{ component.level }}
                  </td>
                  <td class="p-2">
                    {{ component.name }}
                  </td>
                  <td class="p-2">
                    {{ component.part }}
                  </td>
                  <td class="p-2">
                    {{ component.quantity }}
                  </td>
                  <td class="p-2">
                    {{ component.unit }}
                  </td>
                  <td class="p-2">${{ component.unitCost.toFixed(2) }}</td>
                  <td class="p-2">${{ (component.quantity * component.unitCost).toFixed(2) }}</td>
                  <td class="p-2">
                    <button
                      type="button"
                      @click="editComponent(index)"
                      class="cursor-pointer rounded bg-blue-600 px-4 py-2 text-sm text-white"
                    >
                      Edit
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Total -->
          <div class="border-t pt-4 text-right">
            <p class="text-lg font-semibold">Total Estimated Cost: ${{ totalCost.toFixed(2) }}</p>
          </div>

          <!-- Version Management -->
          <div class="rounded-md bg-yellow-100 p-4">
            <h4 class="font-bold">Version Management</h4>
            <div class="mt-2 space-y-2">
              <label class="flex items-center space-x-2">
                <input
                  type="radio"
                  value="update"
                  v-model="form.versionOption"
                  class="text-blue-600"
                  name="version"
                />
                <span>Update current version (v2.1)</span>
              </label>
              <label class="flex items-center space-x-2">
                <input
                  type="radio"
                  value="new"
                  v-model="form.versionOption"
                  class="text-blue-600"
                  name="version"
                />
                <span>Create new version (v2.2)</span>
              </label>
            </div>
          </div>
          <h1 class="mb-4 text-2xl font-bold">Add New Component</h1>
          <div class="mt-4 grid grid-cols-3 gap-4 text-sm">
            <div>
              <label class="mr-2 font-semibold">Component/Material</label>
              <input type="text" class="mt-2 w-full rounded border border-gray-300 px-2 py-1" />
            </div>
            <div>
              <label class="mr-2 font-semibold">Quantity</label>
              <input type="number" class="mt-2 w-full rounded border border-gray-300 px-2 py-1" />
            </div>
            <div>
              <label class="mr-2 font-semibold">Unit of Measure</label>
              <select class="mt-2 w-full rounded border border-gray-300 px-2 py-1">
                <option>pc</option>
                <option>kg</option>
              </select>
            </div>
            <button class="rounded bg-blue-600 px-4 py-2 text-white">Add to BOM</button>
            <button class="rounded bg-gray-300 px-4 py-2">Cancel</button>
          </div>
          <!-- Action Buttons -->
          <div class="flex justify-end gap-4 pt-4">
            <button
              type="submit"
              class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
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

const showEditBOMsPopup = ref(false)
const showAddBOMsPopup = ref(false)
const showViewBOMsPopup = ref(false)

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
  versionOption?: string // Add versionOption property
}

interface ProductionLineForm {
  lineName: string
  status: string
  capacity: number
  oeeTarget: number
  assignedWorkflows: string[]
  versionOption?: string // Add versionOption property
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
  versionOption: 'update', // Add default value for versionOption
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

const emit = defineEmits(['close', 'submit', 'update:showBOMsPopup', 'update:showEditBOMsPopup'])

const components = ref([
  {
    level: '1',
    name: 'Main Motor Assembly',
    part: 'MOT-100',
    quantity: 1,
    unit: 'pc',
    unitCost: 150,
    totalCost: 150,
  },
  {
    level: '1.1',
    name: 'Gearbox Assembly',
    part: 'GBR-200',
    quantity: 1,
    unit: 'pc',
    unitCost: 75,
    totalCost: 75,
  },
  {
    level: '1.1.1',
    name: 'Steel Gear',
    part: 'GR-001',
    quantity: 4,
    unit: 'pc',
    unitCost: 10,
    totalCost: 40,
  },
])

const selectedComponent = ref<null | number>(null)
const material = ref('')
const quantity = ref(1)
const unit = ref('pc')

function editComponent(index: number) {
  selectedComponent.value = index
  const comp = components.value[index]
  material.value = comp.name
  quantity.value = comp.quantity
  unit.value = comp.unit
}

function addOrUpdateComponent() {
  if (selectedComponent.value !== null) {
    // Update existing
    const idx = selectedComponent.value
    const existing = components.value[idx]
    existing.name = material.value
    existing.quantity = quantity.value
    existing.unit = unit.value
    existing.totalCost = existing.unitCost * quantity.value
    selectedComponent.value = null
  } else {
    // Add new (you can extend this)
    components.value.push({
      level: '1.X',
      name: material.value,
      part: 'NEW-XXX',
      quantity: quantity.value,
      unit: unit.value,
      unitCost: 0,
      totalCost: 0,
    })
  }
  material.value = ''
  quantity.value = 1
  unit.value = 'pc'
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
