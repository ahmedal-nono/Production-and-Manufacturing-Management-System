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
              <option value="Active">Active</option>
              <option value="Maintenance">Maintenance</option>
              <option value="Inactive">Inactive</option>
            </select>
          </div>
        </div>

        <div v-if="error" class="py-4 text-center text-red-500">{{ error }}</div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-center">
            <thead class="bg-blue-500 text-white">
              <tr>
                <th class="border border-gray-700 px-4 py-2">Line Name</th>
                <th class="border border-gray-700 px-4 py-2">Status</th>
                <th class="border border-gray-700 px-4 py-2">Capacity</th>
                <th class="border border-gray-700 px-4 py-2">Maintenance</th>
                <th class="border border-gray-700 px-4 py-2">Shift</th>
                <th class="border border-gray-700 px-4 py-2">OEE Target</th>
                <th class="border border-gray-700 px-4 py-2">Work Centers</th>
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
                v-if="loading"
                :rows="4"
                :cols="userRole === 'Production Manager' ? 8 : 7"
              />
              <tr
                v-for="line in filteredLines"
                v-show="!loading"
                :key="line.id"
                class="border-t hover:bg-gray-100"
              >
                <td class="border border-gray-700 px-4 py-2">{{ line.line_name }}</td>
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
                <td class="border border-gray-700 px-4 py-2">{{ line.capacity_limit }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ line.maintenance_schedule }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ line.preferred_shift }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ line.oee_target }}%</td>
                <td class="border border-gray-700 px-4 py-2">
                  {{ formatWorkCenters(line.work_centers) }}
                </td>
                <td
                  v-if="userRole === 'Production Manager'"
                  class="border border-gray-700 px-4 py-2"
                >
                  <button
                    @click="openEditPopup(line.id)"
                    class="cursor-pointer rounded bg-blue-600 px-3 py-1 text-white hover:bg-blue-500"
                  >
                    Edit
                  </button>
                  <button
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

    <!-- Add Production Line Popup -->
    <Popup
      :visible="showAddProductionLinesPopup"
      @update:visible="showAddProductionLinesPopup = $event"
    >
      <div class="p-5">
        <h2 class="mb-6 text-2xl font-bold">Create Production Line</h2>
        <form @submit.prevent="handleAddProductionLine" class="space-y-6">
          <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div>
              <label class="mb-1 block text-sm font-medium">Line Name*</label>
              <input
                v-model="form.line_name"
                type="text"
                placeholder="Electronics Assembly"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Status*</label>
              <select
                v-model="form.status"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              >
                <option value="Active">Active</option>
                <option value="Maintenance">Maintenance</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Capacity Limit*</label>
              <input
                v-model="form.capacity_limit"
                type="number"
                placeholder="50"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">OEE Target*</label>
              <input
                v-model="form.oee_target"
                type="number"
                placeholder="90"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Maintenance Schedule*</label>
              <select
                v-model="form.maintenance_schedule"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              >
                <option value="Weekly">Weekly</option>
                <option value="Bi-weekly">Bi-weekly</option>
                <option value="Monthly">Monthly</option>
              </select>
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Preferred Shift*</label>
              <select
                v-model="form.preferred_shift"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              >
                <option value="Morning">Morning</option>
                <option value="Afternoon">Afternoon</option>
                <option value="Evening">Evening</option>
                <option value="Night">Night</option>
              </select>
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Work Centers</label>
              <div v-if="workCentersLoading" class="text-sm text-gray-500">Loading work centers...</div>
              <select
                v-else
                v-model="form.work_centers"
                multiple
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                <option v-for="wc in workCenters" :key="wc.id" :value="wc.id">
                  {{ wc.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="pt-4">
            <button
              type="submit"
              class="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              :disabled="loading"
            >
              <span v-if="loading">Saving...</span>
              <span v-else>Save Configuration</span>
            </button>
          </div>
        </form>
      </div>
    </Popup>

    <!-- Edit Production Line Popup -->
    <Popup
      :visible="showEditProductionLinesPopup"
      @update:visible="showEditProductionLinesPopup = $event"
    >
      <div class="p-5">
        <h2 class="mb-6 text-2xl font-bold">Edit Production Line</h2>
        <form @submit.prevent="handleEditProductionLine" class="space-y-6">
          <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div>
              <label class="mb-1 block text-sm font-medium">Line Name*</label>
              <input
                v-model="editForm.line_name"
                type="text"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Status*</label>
              <select
                v-model="editForm.status"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              >
                <option value="Active">Active</option>
                <option value="Maintenance">Maintenance</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Capacity Limit*</label>
              <input
                v-model="editForm.capacity_limit"
                type="number"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">OEE Target*</label>
              <input
                v-model="editForm.oee_target"
                type="number"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Maintenance Schedule*</label>
              <select
                v-model="editForm.maintenance_schedule"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              >
                <option value="Weekly">Weekly</option>
                <option value="Bi-weekly">Bi-weekly</option>
                <option value="Monthly">Monthly</option>
              </select>
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Preferred Shift*</label>
              <select
                v-model="editForm.preferred_shift"
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                required
              >
                <option value="Morning">Morning</option>
                <option value="Afternoon">Afternoon</option>
                <option value="Evening">Evening</option>
                <option value="Night">Night</option>
              </select>
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Work Centers</label>
              <select
                v-model="editForm.work_centers"
                multiple
                class="w-full rounded-md border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                <option v-for="wc in workCenters" :key="wc.id" :value="wc.id">
                  {{ wc.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="showEditProductionLinesPopup = false"
              class="rounded-md bg-gray-500 px-4 py-2 text-white hover:bg-gray-600 focus:outline-none"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              :disabled="loading"
            >
              <span v-if="loading">Saving...</span>
              <span v-else>Save Changes</span>
            </button>
          </div>
        </form>
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

interface ProductionLine {
  id: number
  line_name: string
  capacity_limit: number
  maintenance_schedule: string
  preferred_shift: string
  status: string
  oee_target: number
  work_centers?: number[]
}

interface WorkCenter {
  id: number
  name: string
  code: string
  location: string
  status: string
  remarks: string
}

const api = axios.create({
  baseURL: `${baseApiUrl}/`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// State
const userStore = useUserStore()
const userRole = userStore.user?.role
const productionLines = ref<ProductionLine[]>([])
const workCenters = ref<WorkCenter[]>([])
const loading = ref(false)
const workCentersLoading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')
const statusFilter = ref('all')

// Popup states
const showAddProductionLinesPopup = ref(false)
const showEditProductionLinesPopup = ref(false)
const editingLineId = ref<number | null>(null)

// Forms
const form = ref({
  line_name: '',
  capacity_limit: 0,
  oee_target: 0,
  status: 'Active',
  maintenance_schedule: 'Weekly',
  preferred_shift: 'Morning',
  work_centers: [] as number[],
})

const editForm = ref({
  line_name: '',
  capacity_limit: 0,
  oee_target: 0,
  status: 'Active',
  maintenance_schedule: 'Weekly',
  preferred_shift: 'Morning',
  work_centers: [] as number[],
})

// Computed
const filteredLines = computed(() => {
  return productionLines.value.filter(line => {
    const matchesSearch = line.line_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus = statusFilter.value === 'all' || line.status.toLowerCase() === statusFilter.value.toLowerCase()
    return matchesSearch && matchesStatus
  })
})

// Methods
const formatWorkCenters = (workCenterIds: number[] | undefined) => {
  if (!workCenterIds || !workCenterIds.length) return '-'
  return workCenterIds.map(id => {
    const wc = workCenters.value.find(w => w.id === id)
    return wc ? wc.name : ''
  }).filter(Boolean).join(', ') || '-'
}

const resetForm = () => {
  form.value = {
    line_name: '',
    capacity_limit: 0,
    oee_target: 0,
    status: 'Active',
    maintenance_schedule: 'Weekly',
    preferred_shift: 'Morning',
    work_centers: [],
  }
}

const fetchProductionLines = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await api.get('production-lines/')
    productionLines.value = response.data
  } catch (err) {
    error.value = 'Failed to fetch production lines'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const fetchWorkCenters = async () => {
  try {
    workCentersLoading.value = true
    const response = await api.get('workcentre/workcenters')
    workCenters.value = response.data
  } catch (err) {
    console.error('Failed to fetch work centers', err)
  } finally {
    workCentersLoading.value = false
  }
}

const handleAddProductionLine = async () => {
  try {
    loading.value = true
    const response = await api.post('production-lines/', {
      line_name: form.value.line_name,
      capacity_limit: form.value.capacity_limit,
      oee_target: form.value.oee_target,
      status: form.value.status,
      maintenance_schedule: form.value.maintenance_schedule,
      preferred_shift: form.value.preferred_shift,
      work_centers: form.value.work_centers
    })
    productionLines.value.push(response.data)
    resetForm()
    showAddProductionLinesPopup.value = false
  } catch (err) {
    error.value = 'Failed to add production line'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const openEditPopup = (id: number) => {
  const line = productionLines.value.find(line => line.id === id)
  if (line) {
    editingLineId.value = id
    editForm.value = {
      line_name: line.line_name,
      capacity_limit: line.capacity_limit,
      oee_target: line.oee_target,
      status: line.status,
      maintenance_schedule: line.maintenance_schedule,
      preferred_shift: line.preferred_shift,
      work_centers: line.work_centers || [],
    }
    showEditProductionLinesPopup.value = true
  }
}

const handleEditProductionLine = async () => {
  if (!editingLineId.value) return

  try {
    loading.value = true
    const response = await api.put(`production-lines/${editingLineId.value}/`, {
      line_name: editForm.value.line_name,
      capacity_limit: editForm.value.capacity_limit,
      oee_target: editForm.value.oee_target,
      status: editForm.value.status,
      maintenance_schedule: editForm.value.maintenance_schedule,
      preferred_shift: editForm.value.preferred_shift,
      work_centers: editForm.value.work_centers
    })
    
    const index = productionLines.value.findIndex(line => line.id === editingLineId.value)
    if (index !== -1) {
      productionLines.value[index] = response.data
    }
    
    showEditProductionLinesPopup.value = false
    editingLineId.value = null
  } catch (err) {
    error.value = 'Failed to update production line'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const deleteProductionLine = async (id: number) => {
  if (!confirm('Are you sure you want to delete this production line?')) return

  const index = productionLines.value.findIndex((line) => line.id === id)
  if (index === -1) return
  const removed = productionLines.value[index]
  productionLines.value.splice(index, 1) // optimistic removal

  try {
    await api.delete(`production-lines/${id}/`)
  } catch (err) {
    productionLines.value.splice(index, 0, removed) // rollback on failure
    error.value = 'Failed to delete production line'
    console.error(err)
  }
}

const openAddPopup = () => {
  resetForm()
  showAddProductionLinesPopup.value = true
}

// Lifecycle
onMounted(async () => {
  await fetchProductionLines()
  await fetchWorkCenters()
})

// Props and Emits
defineProps<{
  showProductionLinesPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showProductionLinesPopup'])
</script>

<style>
button {
  cursor: pointer;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>