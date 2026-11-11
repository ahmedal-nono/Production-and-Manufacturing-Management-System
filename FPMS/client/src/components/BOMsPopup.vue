<template>
  <div>
    <Popup
      :visible="showBOMsPopup"
      @update:visible="(value: boolean) => emitEvent('update:showBOMsPopup', value)"
    >
      <div>
        <h1 class="mb-6 text-4xl font-extrabold">Existing BOMs</h1>
        <div class="overflow-x-auto">
          <table class="w-full text-center">
            <thead class="bg-blue-500 text-white">
              <tr>
                <th class="border border-gray-700 px-4 py-2">BOM Name</th>
                <th class="border border-gray-700 px-4 py-2">Product Code</th>
                <th class="border border-gray-700 px-4 py-2">Version</th>
                <th class="border border-gray-700 px-4 py-2">Status</th>
                <th
                  v-if="userRole === 'Production Manager'"
                  class="border border-gray-700 px-4 py-2"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              <SkeletonRows
                v-if="bomsLoading"
                :rows="4"
                :cols="userRole === 'Production Manager' ? 5 : 4"
              />
              <tr v-for="bom in filteredBOMs" :key="bom.id" class="border-t">
                <td class="border border-gray-700 px-4 py-2">{{ bom.name }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ bom.productCode }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ bom.version }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ bom.status }}</td>
                <td
                  v-if="userRole === 'Production Manager'"
                  class="border border-gray-700 px-4 py-2"
                >
                  <button
                    v-if="userRole === 'Production Manager'"
                    @click="() => viewBOM(bom.id)"
                    class="mr-2 rounded bg-blue-600 px-3 py-1 text-white hover:bg-blue-500"
                  >
                    View
                  </button>
                  <button
                    v-if="userRole === 'Production Manager'"
                    @click="() => editBOM(bom.id)"
                    class="mr-2 rounded bg-green-600 px-3 py-1 text-white hover:bg-green-500"
                  >
                    Edit
                  </button>
                  <button
                    v-if="userRole === 'Production Manager'"
                    @click="() => deleteBOM(bom.id)"
                    class="rounded bg-red-600 px-3 py-1 text-white hover:bg-red-500"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <button
        v-if="userRole === 'Production Manager'"
        @click="() => createBOM()"
        class="mt-4 rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
      >
        + New BOM
      </button>
    </Popup>

    <Popup :visible="showAddBOMsPopup" @update:visible="showAddBOMsPopup = $event">
      <div class="">
        <h1 class="mb-6 text-2xl font-bold">Create New Bill of Materials</h1>
        <form @submit.prevent="saveBOM" class="space-y-6">
          <div>
            <h2 class="mb-4 text-xl font-semibold">BOM Information</h2>
            <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">BOM Name</label>
                <input
                  v-model="bomForm.bomName"
                  type="text"
                  placeholder="Enter BOM name"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  required
                />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">Product Code</label>
                <select
                  v-model="bomForm.productCode"
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
                  v-model="bomForm.status"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                >
                  <option value="Draft">Draft</option>
                  <option value="Approved">Approved</option>
                </select>
              </div>
            </div>
          </div>
          <div>
            <h2 class="mb-4 text-xl font-semibold">Components & Materials</h2>
            <table class="w-full text-center">
              <thead class="bg-blue-500 text-white">
                <tr>
                  <th class="border border-gray-700 px-4 py-2">Component</th>
                  <th class="border border-gray-700 px-4 py-2">Part Number</th>
                  <th class="border border-gray-700 px-4 py-2">Quantity</th>
                  <th class="border border-gray-700 px-4 py-2">Unit</th>
                  <th class="border border-gray-700 px-4 py-2">Unit Cost</th>
                  <th class="border border-gray-700 px-4 py-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(component, index) in bomForm.components" :key="index" class="border-t">
                  <td class="border border-gray-700 px-4 py-2">
                    <input
                      v-model="component.name"
                      type="text"
                      placeholder="Component name"
                      class="w-full rounded border border-gray-300 px-2 py-1"
                      required
                    />
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    <input
                      v-model="component.partNumber"
                      type="text"
                      placeholder="Part number"
                      class="w-full rounded border border-gray-300 px-2 py-1"
                      required
                    />
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    <div class="flex items-center">
                      <input
                        v-model="component.quantity"
                        type="number"
                        min="1"
                        required
                        class="w-full rounded border border-gray-300 px-2 py-1"
                      />
                      <button
                        type="button"
                        @click="() => adjustQuantity(index, 1)"
                        class="ml-1 px-1 text-gray-600 hover:text-gray-900"
                      >
                        ↑
                      </button>
                    </div>
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    <select
                      v-model="component.unit"
                      class="w-full rounded border border-gray-300 px-2 py-1"
                      required
                    >
                      <option value="pc">pc</option>
                      <option value="kg">kg</option>
                      <option value="m">m</option>
                      <option value="l">l</option>
                    </select>
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    <input
                      v-model="component.unitCost"
                      type="number"
                      min="0.01"
                      step="0.01"
                      class="w-full rounded border border-gray-300 px-2 py-1"
                      required
                    />
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    <button
                      type="button"
                      @click="() => removeComponent(index)"
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
          <div class="border-t pt-4">
            <p class="text-lg font-semibold">Total Estimated Cost: ${{ totalCost.toFixed(2) }}</p>
          </div>
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
          <h1 class="text-2xl font-bold text-blue-500">{{ bomForm.bomName }}</h1>
          <div class="flex justify-between">
            <p class="mt-2 mb-6 w-fit rounded-2xl border bg-blue-100 p-2 text-sm text-blue-500">
              Current Version {{ bomForm.version || 'v1.0' }}
            </p>
            <p class="flex justify-end">{{ bomForm.status }}</p>
          </div>
        </div>

        <form @submit.prevent="saveBOM" class="space-y-6">
          <div>
            <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">BOM Name</label>
                <input
                  v-model="bomForm.bomName"
                  type="text"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  required
                />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">Product Code</label>
                <input
                  v-model="bomForm.productCode"
                  type="text"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  required
                />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">Base Quantity</label>
                <input
                  v-model="bomForm.baseQuantity"
                  type="number"
                  min="1"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  required
                />
              </div>
            </div>
          </div>

          <div>
            <h2 class="mb-4 text-xl font-semibold">Component Structure</h2>
            <table class="w-full text-center">
              <thead class="bg-blue-500 text-white">
                <tr>
                  <th class="border border-gray-700 px-4 py-2">Level</th>
                  <th class="border border-gray-700 px-4 py-2">Component</th>
                  <th class="border border-gray-700 px-4 py-2">Part Number</th>
                  <th class="border border-gray-700 px-4 py-2">Quantity</th>
                  <th class="border border-gray-700 px-4 py-2">Unit</th>
                  <th class="border border-gray-700 px-4 py-2">Unit Cost</th>
                  <th class="border border-gray-700 px-4 py-2">Total Cost</th>
                  <th class="border border-gray-700 px-4 py-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(component, index) in bomForm.components"
                  :key="index"
                  class="border-t hover:bg-gray-100"
                >
                  <td class="border border-gray-700 px-4 py-2">{{ index + 1 }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ component.name }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ component.partNumber }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ component.quantity }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ component.unit }}</td>
                  <td class="border border-gray-700 px-4 py-2">
                    ${{ component.unitCost.toFixed(2) }}
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    ${{ (component.quantity * component.unitCost).toFixed(2) }}
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    <button
                      type="button"
                      @click="() => removeComponent(index)"
                      class="text-sm text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <h2 class="mb-4 text-xl font-semibold">Add New Component</h2>
          <div class="grid grid-cols-5 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Component</label>
              <input
                v-model="newComponent.name"
                type="text"
                placeholder="Enter component name"
                class="w-full rounded-md border border-gray-300 px-3 py-2"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Part Number</label>
              <input
                v-model="newComponent.partNumber"
                type="text"
                placeholder="Enter part number"
                class="w-full rounded-md border border-gray-300 px-3 py-2"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Quantity</label>
              <input
                v-model="newComponent.quantity"
                type="number"
                min="1"
                class="w-full rounded-md border border-gray-300 px-3 py-2"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Unit</label>
              <select
                v-model="newComponent.unit"
                class="w-full rounded-md border border-gray-300 px-3 py-2"
                required
              >
                <option value="pc">pc</option>
                <option value="kg">kg</option>
                <option value="m">m</option>
                <option value="l">l</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Unit Cost</label>
              <input
                v-model="newComponent.unitCost"
                type="number"
                min="0.01"
                step="0.01"
                class="w-full rounded-md border border-gray-300 px-3 py-2"
                required
              />
            </div>
          </div>
          <div class="mt-4 flex justify-end space-x-3">
            <button
              type="button"
              @click="addNewComponent"
              class="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
            >
              Add to BOM
            </button>
            <button
              type="button"
              @click="resetNewComponent"
              class="rounded-md bg-gray-300 px-4 py-2 hover:bg-gray-400"
            >
              Cancel
            </button>
          </div>

          <div class="mt-6 flex justify-end space-x-3">
            <button
              type="submit"
              class="rounded-md bg-green-600 px-4 py-2 text-white hover:bg-green-700"
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
          <h1 class="text-2xl font-bold text-blue-500">{{ bomForm.bomName }}</h1>
          <div class="flex justify-between">
            <p class="mt-2 mb-6 w-fit rounded-2xl border bg-blue-100 p-2 text-sm text-blue-500">
              Current Version {{ bomForm.version || 'v1.0' }}
            </p>
            <p class="flex justify-end">{{ bomForm.status }}</p>
          </div>
        </div>

        <form class="space-y-6">
          <div>
            <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">BOM Name</label>
                <input
                  v-model="bomForm.bomName"
                  type="text"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  disabled
                />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">Product Code</label>
                <input
                  v-model="bomForm.productCode"
                  type="text"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  disabled
                />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-gray-700">Base Quantity</label>
                <input
                  v-model="bomForm.baseQuantity"
                  type="number"
                  class="w-full rounded-md border border-gray-300 px-3 py-2"
                  disabled
                />
              </div>
            </div>
          </div>

          <div>
            <h2 class="mb-4 text-xl font-semibold">Component Structure</h2>
            <table class="w-full text-center">
              <thead class="bg-blue-500 text-white">
                <tr>
                  <th class="border border-gray-700 px-4 py-2">Level</th>
                  <th class="border border-gray-700 px-4 py-2">Component</th>
                  <th class="border border-gray-700 px-4 py-2">Part Number</th>
                  <th class="border border-gray-700 px-4 py-2">Quantity</th>
                  <th class="border border-gray-700 px-4 py-2">Unit</th>
                  <th class="border border-gray-700 px-4 py-2">Unit Cost</th>
                  <th class="border border-gray-700 px-4 py-2">Total Cost</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(component, index) in bomForm.components"
                  :key="index"
                  class="border-t hover:bg-gray-100"
                >
                  <td class="border border-gray-700 px-4 py-2">{{ index + 1 }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ component.name }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ component.partNumber }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ component.quantity }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ component.unit }}</td>
                  <td class="border border-gray-700 px-4 py-2">
                    ${{ component.unitCost.toFixed(2) }}
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    ${{ (component.quantity * component.unitCost).toFixed(2) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="border-t pt-4 text-right">
            <p class="text-lg font-semibold">Total Estimated Cost: ${{ totalCost.toFixed(2) }}</p>
          </div>
        </form>
      </div>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Popup from '@/components/popup.vue'
import SkeletonRows from '@/components/SkeletonRows.vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { baseApiUrl } from '@/api'

const API_BASE_URL = `${baseApiUrl}/boms/`
const userStore = useUserStore()
const userRole = userStore.user?.role

defineProps<{
  showBOMsPopup: boolean
}>()
const emitEvent = defineEmits(['update:showBOMsPopup']) // State for BOMs and UI
const boms = ref<any[]>([])
const bomsLoading = ref(false)
const products = ref<any[]>([]) // Define products as a reactive property
const showEditBOMsPopup = ref(false)
const showAddBOMsPopup = ref(false)
const showViewBOMsPopup = ref(false)
const searchQuery = ref('')
const statusFilter = ref('all')

// BOM Form data
const bomForm = ref({
  id: null as number | null,
  bomName: '',
  productCode: '',
  status: 'Draft',
  components: [] as Array<{
    id?: number
    name: string
    partNumber: string
    quantity: number
    unit: string
    unitCost: number
  }>,
  baseQuantity: 1,
  version: '',
  versionOption: 'update',
})

// Fetch products data
async function fetchProducts() {
  try {
    const response = await axios.get(`${baseApiUrl}/products/`)
    products.value = response.data
  } catch (error) {
    console.error('Error fetching products:', error)
  }
}

// Call fetchProducts on component mount
onMounted(() => {
  fetchBOMs()
  fetchProducts()
})

const newComponent = ref({
  name: '',
  partNumber: '',
  quantity: 1,
  unit: 'pc',
  unitCost: 0,
})

// Computed properties
const filteredBOMs = computed(() => {
  return boms.value.filter((bom) => {
    const matchesSearch =
      bom.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      bom.product_code.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesStatus = statusFilter.value === 'all' || bom.status === statusFilter.value

    return matchesSearch && matchesStatus
  })
})

const totalCost = computed(() => {
  return bomForm.value.components.reduce((total, component) => {
    return total + component.quantity * component.unitCost
  }, 0)
})

// API functions
async function fetchBOMs() {
  bomsLoading.value = true
  try {
    const response = await axios.get(API_BASE_URL)
    boms.value = response.data.map((bom: any) => ({
      ...bom,
      productCode: bom.product_code,
    }))
  } catch (error) {
    console.error('Error fetching BOMs:', error)
  } finally {
    bomsLoading.value = false
  }
}

async function fetchBOMById(id: number) {
  try {
    const response = await axios.get(`${API_BASE_URL}${id}/`)
    return response.data
  } catch (error) {
    console.error(`Error fetching BOM with ID ${id}:`, error)
    throw error
  }
}

async function saveBOM() {
  const bomData = {
    name: bomForm.value.bomName,
    product_code: bomForm.value.productCode,
    status: bomForm.value.status,
    components: bomForm.value.components.map((comp) => ({
      name: comp.name,
      part_number: comp.partNumber,
      quantity: comp.quantity,
      unit: comp.unit,
      unit_cost: comp.unitCost.toString(),
    })),
    version: bomForm.value.id ? bomForm.value.version : generateNewVersion(), // Use existing version or generate a new one
  }

  try {
    if (bomForm.value.id) {
      // Update existing BOM
      const response = await axios.put(`${API_BASE_URL}${bomForm.value.id}/`, bomData)
      const updatedBOM = {
        ...response.data,
        productCode: response.data.product_code,
      }
      const index = boms.value.findIndex((bom) => bom.id === bomForm.value.id)
      if (index !== -1) {
        boms.value[index] = updatedBOM // Update the BOM in the list
      }
    } else {
      // Create new BOM
      const response = await axios.post(API_BASE_URL, bomData)
      boms.value.push({
        ...response.data,
        productCode: response.data.product_code,
      }) // Add the new BOM to the list
    }
    resetForm()
  } catch (error) {
    console.error('Error saving BOM:', error)
  }
}

async function deleteBOM(id: number) {
  if (confirm('Are you sure you want to delete this BOM?')) {
    const index = boms.value.findIndex((bom) => bom.id === id)
    if (index === -1) return
    const removed = boms.value[index]
    boms.value.splice(index, 1) // optimistic removal
    try {
      await axios.delete(`${API_BASE_URL}${id}/`)
    } catch (error) {
      boms.value.splice(index, 0, removed) // rollback on failure
      console.error(`Error deleting BOM with ID ${id}:`, error)
    }
  }
}

// Component functions
function closeBOMsPopup() {
  emitEvent('update:showBOMsPopup', false)
}

async function editBOM(id: number) {
  try {
    const bom = await fetchBOMById(id)
    bomForm.value = {
      id: bom.id,
      bomName: bom.name,
      productCode: bom.product_code,
      status: bom.status,
      components: bom.components.map((comp: any) => ({
        id: comp.id,
        name: comp.name,
        partNumber: comp.part_number,
        quantity: comp.quantity,
        unit: comp.unit,
        unitCost: parseFloat(comp.unit_cost),
      })),
      baseQuantity: 1,
      version: bom.version || 'v1.0',
      versionOption: 'update',
    }
    showEditBOMsPopup.value = true
  } catch (error) {
    console.error('Error loading BOM for editing:', error)
  }
}

async function viewBOM(id: number) {
  try {
    const bom = await fetchBOMById(id)
    bomForm.value = {
      id: bom.id,
      bomName: bom.name,
      productCode: bom.product_code,
      status: bom.status,
      components: bom.components.map((comp: any) => ({
        id: comp.id,
        name: comp.name,
        partNumber: comp.part_number,
        quantity: comp.quantity,
        unit: comp.unit,
        unitCost: parseFloat(comp.unit_cost),
      })),
      baseQuantity: 1,
      version: bom.version || 'v1.0',
      versionOption: 'update',
    }
    showViewBOMsPopup.value = true
  } catch (error) {
    console.error('Error loading BOM for viewing:', error)
  }
}

function createBOM() {
  resetForm()
  showAddBOMsPopup.value = true
}

function addComponent() {
  bomForm.value.components.push({
    name: '',
    partNumber: '',
    quantity: 1,
    unit: 'pc',
    unitCost: 0,
  })
}

function addNewComponent() {
  bomForm.value.components.push({ ...newComponent.value })
  resetNewComponent()
}

function resetNewComponent() {
  newComponent.value = { name: '', partNumber: '', quantity: 1, unit: 'pc', unitCost: 0 }
}

function removeComponent(index: number) {
  bomForm.value.components.splice(index, 1)
}

function adjustQuantity(index: number, amount: number) {
  const component = bomForm.value.components[index]
  component.quantity = Math.max(0, component.quantity + amount)
}

function resetForm() {
  bomForm.value = {
    id: null,
    bomName: '',
    productCode: '',
    status: 'Draft',
    components: [],
    baseQuantity: 1,
    version: '',
    versionOption: 'update',
  }
  showAddBOMsPopup.value = false
  showEditBOMsPopup.value = false
  showViewBOMsPopup.value = false
}

function generateNewVersion() {
  const currentVersion = bomForm.value.version || 'v1.0'
  const versionNumber = parseFloat(currentVersion.slice(1)) || 1.0
  return `v${(versionNumber + 0.1).toFixed(1)}`
}
</script>

<style>
button {
  cursor: pointer;
}
</style>
