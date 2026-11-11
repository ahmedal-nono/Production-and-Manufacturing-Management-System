<template>
  <Popup
    :visible="showQualityInspectionPopup"
    @update:visible="(value: boolean) => emitEvent('update:showQualityInspectionPopup', value)"
  >
    <div class="">
      <!-- Header -->
      <div class="mb-4 flex items-center justify-between">
        <h2 class="text-2xl font-bold">Inspections</h2>
      </div>

      <!-- Filters -->
      <div class="mb-4 flex flex-wrap items-center gap-4">
        <input
          v-model="search"
          type="text"
          placeholder="Search by title, product, or keyword"
          class="w-full flex-1 rounded border px-4 py-2 sm:w-auto"
        />
        <select v-model="statusFilter" class="rounded border px-4 py-2">
          <option>All Statuses</option>
          <option>Pending</option>
          <option>Approved</option>
          <option>Rework</option>
          <option>Rejected</option>
        </select>
      </div>

      <p v-if="listError" class="mb-3 rounded bg-red-50 p-2 text-sm text-red-600">
        {{ listError }}
      </p>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr>
              <th class="border border-gray-700 px-4 py-2">Work Order</th>
              <th class="border border-gray-700 px-4 py-2">Product Name</th>
              <th class="border border-gray-700 px-4 py-2">Due Date</th>
              <th class="border border-gray-700 px-4 py-2">Status</th>
              <th class="border border-gray-700 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <SkeletonRows v-if="listLoading" :rows="4" :cols="5" />
            <tr
              v-for="(item, index) in filteredInstructions"
              v-show="!listLoading"
              :key="index"
              class="border bg-white hover:bg-gray-50"
            >
              <td class="border border-gray-700 px-4 py-2">WO-{{ item.id }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ item.product }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ item.dueDate }}</td>
              <td class="border border-gray-700 px-4 py-2">
                <span
                  :class="
                    item.status === 'Approved'
                      ? 'bg-green-100 text-green-700'
                      : item.status === 'Rework'
                        ? 'bg-yellow-100 text-yellow-700'
                        : item.status === 'Rejected'
                          ? 'bg-red-100 text-red-700'
                          : 'bg-gray-200 text-gray-600'
                  "
                  class="rounded-full px-2 py-1 text-xs"
                >
                  {{ item.status }}
                </span>
              </td>
              <td class="space-x-2 border border-gray-700 px-4 py-2">
                <button
                  @click="openStartInspectionPopup(item)"
                  class="mt-4 w-full cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
                >
                  Start Inspection
                </button>
              </td>
            </tr>
            <tr v-if="!filteredInstructions.length">
              <td colspan="5" class="border border-gray-700 px-4 py-4 text-gray-500">
                No work orders found
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Popup>

  <Popup :visible="showStartInspectionPopup" @update:visible="showStartInspectionPopup = $event">
    <div class="">
      <!-- Header -->
      <h2 class="mb-4 text-xl font-semibold">Start Inspection</h2>

      <!-- Work Order Info -->
      <div class="mb-6 text-sm">
        <p><strong>Work Order:</strong> WO-{{ selectedInspection?.id }}</p>
        <p><strong>Product:</strong> {{ selectedInspection?.product }}</p>
        <p><strong>Production Line:</strong> {{ selectedInspection?.productionLine }}</p>
        <p><strong>Status:</strong> {{ selectedInspection?.status }}</p>
      </div>

      <!-- Job Cards Table -->
      <div class="mb-6">
        <h3 class="mb-2 text-lg font-semibold">Job Cards</h3>
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr>
              <th class="border border-gray-700 px-4 py-2">Checklist Item</th>
              <th class="border border-gray-700 px-4 py-2">Status (Pass/Fail)</th>
              <th class="border border-gray-700 px-4 py-2">Notes</th>
              <th class="border border-gray-700 px-4 py-2">Photo Upload</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in checklist" :key="item.jobCardId">
              <td class="border border-gray-700 px-4 py-2">{{ item.name }}</td>
              <td class="border border-gray-700 px-4 py-2">
                <label>
                  <input
                    type="radio"
                    :name="'status' + index"
                    value="pass"
                    v-model="item.state"
                    class="mr-1"
                  />
                  Pass
                </label>
                <label class="ml-4">
                  <input
                    type="radio"
                    :name="'status' + index"
                    value="fail"
                    v-model="item.state"
                    class="mr-1"
                  />
                  Fail
                </label>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input
                  type="text"
                  v-model="item.note"
                  class="w-full rounded border p-1"
                  placeholder="Enter notes"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input
                  type="file"
                  accept="image/*"
                  @change="handleChecklistUpload(index, $event)"
                  class="hidden"
                  :ref="'upload' + index"
                />
                <button
                  @click="($refs['upload' + index] as HTMLInputElement).click()"
                  class="rounded bg-blue-500 px-3 py-1 text-sm text-white hover:bg-blue-600"
                >
                  📷 {{ item.photo ? 'Change' : 'Upload' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Defect Logging -->
      <div class="mb-6">
        <h3 class="mb-2 text-lg font-semibold">Defect Logging</h3>
        <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
          <div>
            <label class="mb-1 block font-medium">Defect Type:</label>
            <select v-model="defect.type" class="w-full rounded border p-2">
              <option disabled value="">Select type</option>
              <option>Material Flaw</option>
              <option>Dimension Error</option>
              <option>Assembly Fault</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block font-medium">Severity:</label>
            <div class="mt-2 space-x-4">
              <label>
                <input type="radio" value="Critical" v-model="defect.severity" /> Critical
              </label>
              <label> <input type="radio" value="Major" v-model="defect.severity" /> Major </label>
              <label> <input type="radio" value="Minor" v-model="defect.severity" /> Minor </label>
            </div>
          </div>
          <div class="md:col-span-2">
            <label class="mb-1 block font-medium">Affected Component:</label>
            <input
              type="text"
              v-model="defect.component"
              class="w-full rounded border p-2"
              placeholder="Enter component"
            />
          </div>
          <div class="md:col-span-2">
            <label class="mb-1 block font-medium">Description:</label>
            <textarea
              v-model="defect.description"
              rows="3"
              class="w-full rounded border p-2"
              placeholder="Enter defect details"
            ></textarea>
          </div>
        </div>
      </div>

      <!-- Final Decision -->
      <div class="mb-4">
        <h3 class="mb-2 text-lg font-semibold">Final Decision</h3>
        <div class="space-x-3">
          <button
            @click="decision = 'approve'"
            :class="
              decision === 'approve'
                ? 'bg-green-700 ring-2 ring-green-300'
                : 'bg-green-500 hover:bg-green-600'
            "
            class="rounded px-4 py-2 text-white"
          >
            ✅ Approve
          </button>
          <button
            @click="decision = 'rework'"
            :class="
              decision === 'rework'
                ? 'bg-yellow-600 ring-2 ring-yellow-300'
                : 'bg-yellow-400 hover:bg-yellow-500'
            "
            class="rounded px-4 py-2 text-white"
          >
            🛠 Rework
          </button>
          <button
            @click="decision = 'reject'"
            :class="
              decision === 'reject'
                ? 'bg-red-700 ring-2 ring-red-300'
                : 'bg-red-500 hover:bg-red-600'
            "
            class="rounded px-4 py-2 text-white"
          >
            ❌ Reject
          </button>
        </div>
      </div>

      <p v-if="submitError" class="mb-2 rounded bg-red-50 p-2 text-sm text-red-600">
        {{ submitError }}
      </p>

      <!-- Actions -->
      <div class="mt-6 flex justify-between">
        <div class="space-x-2">
          <button
            @click="submitInspection"
            :disabled="submitting"
            class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {{ submitting ? 'Submitting...' : 'Submit Inspection' }}
          </button>
        </div>
      </div>
    </div>
  </Popup>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Popup from '@/components/popup.vue'
import SkeletonRows from '@/components/SkeletonRows.vue'
import { useReworkStore } from '@/stores/useRework'
import notificationStore from '@/stores/notificationStore'
import { baseApiUrl } from '@/api'

const API_BASE = baseApiUrl

const reworkStore = useReworkStore()

const showStartInspectionPopup = ref(false)

interface WorkOrderRow {
  id: number
  product: string
  productionLine: string
  dueDate: string
  status: string
}

interface ChecklistRow {
  jobCardId: number
  name: string
  state: '' | 'pass' | 'fail'
  note: string
  photo: File | null
}

const selectedInspection = ref<WorkOrderRow | null>(null)

const workOrderRows = ref<
  { id: number; name: string; due_date: string | null; production_line_name: string | null; latest_decision: string | null }[]
>([])
const listLoading = ref(false)
const listError = ref('')

const search = ref('')
const statusFilter = ref('All Statuses')

const statusLabel = (decision: string | null): string => {
  switch (decision) {
    case 'approve':
      return 'Approved'
    case 'rework':
      return 'Rework'
    case 'reject':
      return 'Rejected'
    default:
      return 'Pending'
  }
}

const instructions = computed(() =>
  workOrderRows.value.map((row) => ({
    id: row.id,
    product: row.name,
    productionLine: row.production_line_name || 'Unknown',
    dueDate: row.due_date ? String(row.due_date).split('T')[0] : '-',
    status: statusLabel(row.latest_decision),
  })),
)

const filteredInstructions = computed(() =>
  instructions.value.filter((item) => {
    const q = search.value.trim().toLowerCase()
    const matchSearch =
      !q ||
      item.product.toLowerCase().includes(q) ||
      String(item.id).includes(q) ||
      item.productionLine.toLowerCase().includes(q)
    const matchStatus =
      statusFilter.value === 'All Statuses' || item.status === statusFilter.value
    return matchSearch && matchStatus
  }),
)

const fetchWorkOrders = async () => {
  listError.value = ''
  listLoading.value = true
  try {
    const { data } = await axios.get(`${API_BASE}/workorders/`)
    workOrderRows.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error('Error fetching work orders:', error)
    listError.value = 'Failed to load work orders'
  } finally {
    listLoading.value = false
  }
}

const checklist = ref<ChecklistRow[]>([])

const defect = ref({
  type: '',
  severity: '',
  component: '',
  description: '',
})

const decision = ref<'' | 'approve' | 'rework' | 'reject'>('')
const submitting = ref(false)
const submitError = ref('')

const openStartInspectionPopup = async (inspection: WorkOrderRow) => {
  submitError.value = ''
  decision.value = ''
  defect.value = { type: '', severity: '', component: '', description: '' }
  checklist.value = []
  selectedInspection.value = inspection
  try {
    const { data } = await axios.get(`${API_BASE}/workorders/${inspection.id}/`)
    checklist.value = (data.job_cards || []).map(
      (card: { id: number; task_name: string }): ChecklistRow => ({
        jobCardId: card.id,
        name: card.task_name,
        state: '',
        note: '',
        photo: null,
      }),
    )
    showStartInspectionPopup.value = true
  } catch (error) {
    console.error('Error fetching work order details:', error)
    submitError.value = 'Failed to load job cards for this work order'
  }
}

const handleChecklistUpload = (index: number, event: Event) => {
  const target = event.target as HTMLInputElement | null
  if (target && target.files && target.files[0]) {
    checklist.value[index].photo = target.files[0]
  }
}

const submitInspection = async () => {
  if (!selectedInspection.value) {
    submitError.value = 'No work order selected'
    return
  }
  if (!decision.value) {
    submitError.value = 'Please select a final decision (Approve / Rework / Reject)'
    return
  }

  submitting.value = true
  submitError.value = ''

  try {
    const { data } = await axios.post(`${API_BASE}/inspections/`, {
      work_order: selectedInspection.value.id,
      defect_type: defect.value.type,
      severity: defect.value.severity.toLowerCase(),
      affected_component: defect.value.component,
      description: defect.value.description,
      final_decision: decision.value,
    })

    const serverItems: { id: number; job_card: { id: number } }[] = data.checklist_items || []

    for (const row of checklist.value) {
      const serverItem = serverItems.find((item) => item.job_card?.id === row.jobCardId)
      if (!serverItem) continue
      if (!row.state && !row.note && !row.photo) continue

      if (row.photo) {
        const formData = new FormData()
        if (row.state) formData.append('state', row.state)
        if (row.note) formData.append('note', row.note)
        formData.append('photo', row.photo)
        await axios.patch(`${API_BASE}/checklist/${serverItem.id}/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
      } else {
        const payload: Record<string, string> = {}
        if (row.state) payload.state = row.state
        if (row.note) payload.note = row.note
        await axios.patch(`${API_BASE}/checklist/${serverItem.id}/`, payload)
      }
    }

    if (decision.value === 'rework') {
      await reworkStore.fetchReworks()
    }

    notificationStore.addNotification(
      `Inspection submitted for WO-${selectedInspection.value.id}`,
      'success',
      'manager',
    )
    showStartInspectionPopup.value = false
    await fetchWorkOrders()
  } catch (error: any) {
    console.error('Error submitting inspection:', error)
    const data = error?.response?.data
    submitError.value =
      (typeof data === 'object' && data
        ? Object.values(data).flat().join(' ')
        : '') || 'Failed to submit inspection'
  } finally {
    submitting.value = false
  }
}

defineProps<{
  showQualityInspectionPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showQualityInspectionPopup'])

onMounted(() => {
  fetchWorkOrders()
})
</script>

<style>
button {
  cursor: pointer;
}
</style>
