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
            />
            <select
              v-model="statusFilter"
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
                <th
                  v-if="userRole === 'Production Manager'"
                  class="border border-gray-700 px-4 py-2"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="line in filteredLines" :key="line.id" class="border-t hover:bg-gray-100">
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
                  <span v-if="Array.isArray(line.workflows) && line.workflows.length">
                    {{ line.workflows.join(', ') }}
                  </span>
                  <span v-else class="text-gray-400">-</span>
                </td>
                <td v-if="userRole === 'Production Manager'" class="border border-gray-700 px-4 py-2">
                  <button
                    v-if="userRole === 'Production Manager'"
                    @click="openEditPopup(line.id)"
                    class="cursor-pointer rounded bg-blue-600 px-3 py-1 text-white hover:bg-blue-500"
                  >
                    Edit
                  </button>
                  <button
                    v-if="userRole === 'Production Manager'"
                    @click="deleteProductionLine(line.id)"
                    class="ml-2 cursor-pointer rounded bg-red-600 px-3 py-1 text-white hover:bg-red-500"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <button
          v-if="userRole === 'Production Manager'"
          @click="openAddPopup"
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
      <div>
        <h2 class="mb-6 text-2xl font-bold">Create Production Line</h2>
        <form @submit.prevent="handleAddProductionLine" class="space-y-6">
          <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div>
              <label class="mb-1 block text-sm font-medium">Line Name</label>
              <input
                v-model="form.name"
                type="text"
                placeholder="Enter line name"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
                minlength="5"
              />
            </div>

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

            <div>
              <label class="mb-1 block text-sm font-medium">Current Output (units)</label>
              <input
                v-model="form.currentOutput"
                type="number"
                placeholder="Enter current output"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
                min="1"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Capacity (units/hour)</label>
              <input
                v-model="form.capacity"
                type="number"
                placeholder="Enter capacity"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
                min="1"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Capacity Utilization (%)</label>
              <input
                v-model="form.utilization"
                type="number"
                placeholder="Enter utilization"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
                min="0"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">OEE (%)</label>
              <input
                v-model="form.oee"
                type="number"
                placeholder="Enter OEE"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                min="0"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Workcenters</label>
              <input
                v-model="form.workcenters"
                type="number"
                placeholder="Enter number of workcenters"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
                min="1"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Assigned Workflows</label>
              <input
                v-model="form.workflows"
                type="text"
                placeholder="Enter workflows (comma-separated)"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
                pattern="^[a-zA-Z0-9, ]+$"
                minlength="5"
              />
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
      <div>
        <h2 class="mb-6 text-2xl font-bold">Edit Production Line</h2>
        <form @submit.prevent="handleEditProductionLine" class="space-y-6">
          <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div>
              <label class="mb-1 block text-sm font-medium">Line Name</label>
              <input
                v-model="form.name"
                type="text"
                placeholder="Enter line name"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
                minlength="5"
              />
            </div>

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

            <div>
              <label class="mb-1 block text-sm font-medium">Current Output (units)</label>
              <input
                v-model="form.currentOutput"
                type="number"
                placeholder="Enter current output"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
                min="1"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Capacity (units/hour)</label>
              <input
                v-model="form.capacity"
                type="number"
                placeholder="Enter capacity"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
                min="1"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Capacity Utilization (%)</label>
              <input
                v-model="form.utilization"
                type="number"
                placeholder="Enter utilization"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
                min="0"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">OEE (%)</label>
              <input
                v-model="form.oee"
                type="number"
                placeholder="Enter OEE"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                min="0"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Workcenters</label>
              <input
                v-model="form.workcenters"
                type="number"
                placeholder="Enter number of workcenters"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
                min="1"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Assigned Workflows</label>
              <input
                v-model="form.workflows"
                type="text"
                placeholder="Enter workflows (comma-separated)"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
                pattern="^[a-zA-Z0-9, ]+$"
                minlength="5"
              />
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
import { useProductionLinesStore } from '@/stores/useProductionLines'
import Popup from '@/components/popup.vue'
import { useOrdersStore } from '@/stores/useOrders'
import { useUserStore } from '@/stores/user'

const ordersStore = useOrdersStore()
const userStore = useUserStore()
const userRole = userStore.user?.role

const showAddProductionLinesPopup = ref(false)
const showEditProductionLinesPopup = ref(false)
const editingLineId = ref<string | null>(null)

defineProps<{
  showProductionLinesPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showProductionLinesPopup'])

const productionLinesStore = useProductionLinesStore()

const searchQuery = ref('')
const statusFilter = ref('all')

const filteredLines = computed(() => {
  return productionLinesStore.productionLines.filter((line) => {
    const matchesSearch = line.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus =
      statusFilter.value === 'all' || line.status.toLowerCase() === statusFilter.value
    return matchesSearch && matchesStatus
  })
})

const form = ref({
  name: '',
  status: 'Active',
  currentOutput: 0,
  capacity: 0,
  utilization: 0,
  oee: null,
  workcenters: 0,
  workflows: [] as string[],
})

const resetForm = () => {
  form.value = {
    name: '',
    status: 'Active',
    currentOutput: 0,
    capacity: 0,
    utilization: 0,
    oee: null,
    workcenters: 0,
    workflows: [],
  }
}

const handleAddProductionLine = () => {
  const newLine = {
    id: productionLinesStore.getNextId, // Correctly call getNextId as a function
    name: form.value.name,
    status: form.value.status,
    currentOutput: form.value.currentOutput || 0,
    capacity: form.value.capacity,
    utilization: form.value.utilization || 0,
    oee: form.value.oee || null,
    workcenters: form.value.workcenters,
    workflows: form.value.workflows
      ? form.value.workflows.split(',').map((workflow) => workflow.trim())
      : [], // Handle empty workflows gracefully
  }

  productionLinesStore.addProductionLine(newLine) // Add the new production line to the store
  resetForm() // Reset the form after adding
  showAddProductionLinesPopup.value = false // Close the popup
  //alert('Production Line added successfully!')
}

const handleEditProductionLine = () => {
  if (!editingLineId.value) {
    alert('No production line selected for editing.')
    return
  }

  if (!form.value.name || form.value.name.length < 3) {
    alert('Line Name is required and must be at least 3 characters long.')
    return
  }

  const updatedLine = {
    name: form.value.name,
    status: form.value.status,
    currentOutput: form.value.currentOutput,
    capacity: form.value.capacity,
    utilization: form.value.utilization,
    oee: form.value.oee,
    workcenters: form.value.workcenters,
    workflows: form.value.workflows.split(',').map((workflow) => workflow.trim()),
  }

  productionLinesStore.editProductionLine(editingLineId.value, updatedLine)
  resetForm()
  showEditProductionLinesPopup.value = false
  editingLineId.value = null
  alert('Production Line updated successfully!')
}

const deleteProductionLine = (lineId: string) => {
  if (confirm('Are you sure you want to delete this production line?')) {
    productionLinesStore.deleteProductionLine(lineId)
    //alert('Production Line deleted successfully!')
  }
}

const openAddPopup = () => {
  resetForm()
  showAddProductionLinesPopup.value = true
}

const openEditPopup = (lineId: string) => {
  const line = productionLinesStore.getProductionLineById(lineId)
  if (line) {
    form.value = {
      ...line,
      workflows: Array.isArray(line.workflows) ? line.workflows.join(', ') : '',
    }
    editingLineId.value = lineId
    showEditProductionLinesPopup.value = true
  }
}
</script>

<style>
button {
  cursor: pointer;
}
</style>
