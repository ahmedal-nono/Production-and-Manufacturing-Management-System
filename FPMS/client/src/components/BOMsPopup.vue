<template>
  <div>
    <Popup
      :visible="showBOMsPopup"
      @update:visible="(value: boolean) => emit('update:showBOMsPopup', value)"
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
                <th class="border border-gray-700 px-4 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="bom in filteredBOMs" :key="bom.id" class="border-t hover:bg-gray-100">
                <td class="border border-gray-700 px-4 py-2">{{ bom.name }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ bom.productCode }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ bom.version }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ bom.status }}</td>
                <td class="border border-gray-700 px-4 py-2">
                  <button
                    @click="viewBOM(bom.id)"
                    class="mr-2 rounded bg-blue-600 px-3 py-1 text-white hover:bg-blue-500"
                  >
                    View
                  </button>
                  <button
                    @click="editBOM(bom.id)"
                    class="mr-2 rounded bg-green-600 px-3 py-1 text-white hover:bg-green-500"
                  >
                    Edit
                  </button>
                  <button
                    @click="deleteBOM(bom.id)"
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
        @click="createBOM()"
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
                  <option value="Pending Review">Pending Review</option>
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
                    />
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    <input
                      v-model="component.partNumber"
                      type="text"
                      placeholder="Part number"
                      class="w-full rounded border border-gray-300 px-2 py-1"
                    />
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
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
                  <td class="border border-gray-700 px-4 py-2">
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
                  <td class="border border-gray-700 px-4 py-2">
                    <input
                      v-model="component.unitCost"
                      type="number"
                      min="0"
                      step="0.01"
                      class="w-full rounded border border-gray-300 px-2 py-1"
                    />
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
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
          <!-- BOM Information -->
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

          <!-- Component Structure -->
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
                      @click="removeComponent(index)"
                      class="text-sm text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Add New Component -->
          <h2 class="mb-4 text-xl font-semibold">Add New Component</h2>
          <div class="grid grid-cols-5 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Component</label>
              <input
                v-model="newComponent.name"
                type="text"
                placeholder="Enter component name"
                class="w-full rounded-md border border-gray-300 px-3 py-2"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Part Number</label>
              <input
                v-model="newComponent.partNumber"
                type="text"
                placeholder="Enter part number"
                class="w-full rounded-md border border-gray-300 px-3 py-2"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Quantity</label>
              <input
                v-model="newComponent.quantity"
                type="number"
                min="1"
                class="w-full rounded-md border border-gray-300 px-3 py-2"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Unit</label>
              <select
                v-model="newComponent.unit"
                class="w-full rounded-md border border-gray-300 px-3 py-2"
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
                min="0"
                step="0.01"
                class="w-full rounded-md border border-gray-300 px-3 py-2"
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

          <!-- Save Changes -->
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
          <!-- BOM Information -->
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

          <!-- Component Structure -->
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

          <!-- Total -->
          <div class="border-t pt-4 text-right">
            <p class="text-lg font-semibold">Total Estimated Cost: ${{ totalCost.toFixed(2) }}</p>
          </div>
        </form>
      </div>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Popup from '@/components/popup.vue'
import { useBOMsStore } from '@/stores/useBOMs'
import { useOrdersStore } from '@/stores/useOrders'

const bomsStore = useBOMsStore()
const ordersStore = useOrdersStore()

const showEditBOMsPopup = ref(false)
const showAddBOMsPopup = ref(false)
const showViewBOMsPopup = ref(false)

const props = defineProps<{
  showBOMsPopup: boolean
}>()

const searchQuery = ref('')
const statusFilter = ref('all')

const filteredBOMs = computed(() => {
  return bomsStore.boms.filter((bom) => {
    const matchesSearch =
      bom.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      bom.productCode.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesStatus = statusFilter.value === 'all' || bom.status === statusFilter.value

    return matchesSearch && matchesStatus
  })
})

const bomForm = ref({
  id: '',
  bomName: '',
  productCode: '',
  status: 'Draft',
  components: [],
  baseQuantity: 1,
  version: '',
  versionOption: 'update',
})

const newComponent = ref({
  name: '',
  partNumber: '',
  quantity: 1,
  unit: 'pc',
  unitCost: 0,
})

const editingBOMId = ref<string | null>(null)

const products = computed(() => {
  return ordersStore.orders.map((order) => ({
    name: order.product,
    sku: order.id,
  }))
})

function saveBOM() {
  const data = {
    id: editingBOMId.value || bomsStore.getLastAndUniqueId,
    name: bomForm.value.bomName,
    productCode: bomForm.value.productCode,
    status: bomForm.value.status,
    components: bomForm.value.components,
    baseQuantity: bomForm.value.baseQuantity,
    version: bomForm.value.versionOption === 'new' ? generateNewVersion() : bomForm.value.version,
  }

  if (editingBOMId.value) {
    bomsStore.editBOM(editingBOMId.value, data)
  } else {
    bomsStore.createBOM(data)
  }

  resetForm()
}

function editBOM(id: string) {
  const bom = bomsStore.getBOMById(id)
  if (bom) {
    editingBOMId.value = bom.id
    bomForm.value = {
      id: bom.id,
      bomName: bom.name,
      productCode: bom.productCode,
      status: bom.status,
      components: [...bom.components],
      baseQuantity: bom.baseQuantity || 1,
      version: bom.version || 'v1.0',
      versionOption: 'update',
    }
    showEditBOMsPopup.value = true // Ensure the popup is opened
  } else {
    console.error(`BOM with ID ${id} not found.`)
  }
}

function viewBOM(id: string) {
  const bom = bomsStore.getBOMById(id)
  if (bom) {
    bomForm.value = {
      id: bom.id,
      bomName: bom.name,
      productCode: bom.productCode,
      status: bom.status,
      components: [...bom.components],
      baseQuantity: bom.baseQuantity || 1,
      version: bom.version || 'v1.0',
    }
    showViewBOMsPopup.value = true
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

function deleteBOM(id: string) {
  if (confirm('Are you sure you want to delete this BOM?')) {
    bomsStore.deleteBOM(id) // Call the deleteBOM action from the store
    //alert('BOM deleted successfully!')
  }
}

const totalCost = computed(() => {
  return bomForm.value.components.reduce((total, component) => {
    return total + component.quantity * component.unitCost
  }, 0)
})

function resetForm() {
  editingBOMId.value = null
  bomForm.value = {
    id: '',
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

const emit = defineEmits(['update:showBOMsPopup'])
</script>

<style>
button {
  cursor: pointer;
}
</style>
