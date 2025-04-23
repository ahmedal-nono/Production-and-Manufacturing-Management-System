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
          type="text"
          placeholder="Search by title, product, or keyword"
          class="w-full flex-1 rounded border px-4 py-2 sm:w-auto"
        />
        <select class="rounded border px-4 py-2">
          <option>All Statuses</option>
        </select>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr>
              <th class="border border-gray-700 px-4 py-2">Workflow ID</th>
              <th class="border border-gray-700 px-4 py-2">Product Name</th>
              <th class="border border-gray-700 px-4 py-2">Due Date</th>
              <th class="border border-gray-700 px-4 py-2">Status</th>
              <th class="border border-gray-700 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, index) in instructions"
              :key="index"
              class="border bg-white hover:bg-gray-50"
            >
              <td class="border border-gray-700 px-4 py-2">{{ item.id }}</td>
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
                          : item.status === 'Ready for Inspection'
                            ? 'bg-yellow-200 text-yellow-800'
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
        <p><strong>Workflow ID:</strong> {{ selectedInspection?.id }}</p>
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
            <tr v-for="(item, index) in checklist" :key="index">
              <td class="border border-gray-700 px-4 py-2">{{ item.name }}</td>
              <td class="border border-gray-700 px-4 py-2">
                <label>
                  <input
                    type="radio"
                    :name="'status' + index"
                    value="Pass"
                    v-model="item.status"
                    class="mr-1"
                  />
                  Pass
                </label>
                <label class="ml-4">
                  <input
                    type="radio"
                    :name="'status' + index"
                    value="Fail"
                    v-model="item.status"
                    class="mr-1"
                  />
                  Fail
                </label>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input
                  type="text"
                  v-model="item.notes"
                  class="w-full rounded border p-1"
                  placeholder="Enter notes"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input
                  type="file"
                  @change="handleChecklistUpload(index, $event)"
                  class="hidden"
                  :ref="'upload' + index"
                />
                <button
                  @click="($refs['upload' + index] as HTMLInputElement).click()"
                  class="rounded bg-blue-500 px-3 py-1 text-sm text-white hover:bg-blue-600"
                >
                  📷 Upload
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
            @click="handleApprove"
            class="rounded bg-green-500 px-4 py-2 text-white hover:bg-green-600"
          >
            ✅ Approve
          </button>
          <button
            @click="handleRework"
            class="rounded bg-yellow-400 px-4 py-2 text-white hover:bg-yellow-500"
          >
            🛠 Rework
          </button>
          <button
            @click="handleReject"
            class="rounded bg-red-500 px-4 py-2 text-white hover:bg-red-600"
          >
            ❌ Reject
          </button>
        </div>
      </div>

      <!-- Actions -->
      <div class="mt-6 flex justify-between">
        <div class="space-x-2">
          <button
            @click="submitInspection"
            class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            Submit Inspection
          </button>
        </div>
      </div>
    </div>
  </Popup>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import Popup from '@/components/popup.vue'
import { useWorkflowsStore } from '@/stores/useWorkflows'
import { useProductionLinesStore } from '@/stores/useProductionLines'
import { useReworkStore } from '@/stores/useRework'

const workflowsStore = useWorkflowsStore()
const productionLinesStore = useProductionLinesStore()
const reworkStore = useReworkStore()

const showStartInspectionPopup = ref(false)
const selectedInspection = ref<null | {
  id: string
  product: string
  productionLine: string
  dueDate: string
  status: string
}>(null)

const instructions = computed(() =>
  workflowsStore.workflows.map((workflow) => ({
    id: workflow.id,
    product: workflow.product,
    productionLine:
      productionLinesStore.getProductionLineById(workflow.productionLineId)?.name || 'Unknown',
    dueDate: '2023-10-01', // Placeholder, replace with actual data if available
    status: workflow.status || 'Pending', // Default status
  })),
)

const openStartInspectionPopup = (inspection: any) => {
  selectedInspection.value = inspection
  showStartInspectionPopup.value = true
}

const updateWorkflowStatus = (workflowId: string, status: string) => {
  workflowsStore.editWorkflow(workflowId, { status })
}

const handleApprove = () => {
  if (selectedInspection.value) {
    selectedInspection.value.status = 'Approved'
    console.log('Inspection Approved')
  }
}

const handleRework = () => {
  if (selectedInspection.value) {
    selectedInspection.value.status = 'Rework'
    console.log('Inspection marked for Rework')
  }
}

const handleReject = () => {
  if (selectedInspection.value) {
    selectedInspection.value.status = 'Rejected'
    console.log('Inspection Rejected')
  }
}

const startNewInspection = (inspectionId: string) => {
  const inspection = instructions.value.find((item) => item.id === inspectionId)
  if (inspection) {
    inspection.status = 'Ready for Inspection'
    console.log('New inspection started:', inspection)
  }
}

const submitInspection = () => {
  if (selectedInspection.value) {
    console.log('Submitting inspection for:', selectedInspection.value)

    // Update workflow status
    updateWorkflowStatus(selectedInspection.value.id, selectedInspection.value.status)

    if (selectedInspection.value.status === 'Rework') {
      const existingRework = reworkStore.getReworkByWorkOrder(selectedInspection.value.id)
      const defectType =
        defect.value.severity === 'Critical'
          ? 'Critical Defect'
          : defect.value.severity === 'Major'
            ? 'Major Defect'
            : 'Minor Defect'

      if (existingRework) {
        console.log('Updating existing rework:', existingRework)
        // Update existing rework
        reworkStore.updateRework(existingRework.id, {
          defectLevel: defect.value.severity || 'Minor',
          defectType: defectType,
          affectedComponent: defect.value.component || 'N/A',
          description: defect.value.description || 'No description provided',
        })
      } else {
        console.log('Creating new rework for:', selectedInspection.value)
        // Create new rework
        reworkStore.createRework({
          id: `RW-${Date.now()}`,
          workOrder: selectedInspection.value.id,
          product: selectedInspection.value.product,
          defectLevel: defect.value.severity || 'Minor',
          defectType: defectType,
          affectedComponent: defect.value.component || 'N/A',
          description: defect.value.description || 'No description provided',
          assignedTo: null,
          dueDate: new Date().toISOString().split('T')[0], // Default to today's date
          status: 'Open',
        })
      }
    }

    console.log(`Inspection submitted with status: ${selectedInspection.value.status}`)
    showStartInspectionPopup.value = false
  } else {
    console.error('No inspection selected for submission.')
  }
}

watch(
  () => selectedInspection.value?.status,
  (newStatus) => {
    console.log('Inspection status updated:', newStatus)
    if (newStatus === 'Rework') {
      submitInspection()
    }
  },
)

defineProps<{
  showQualityInspectionPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showQualityInspectionPopup'])

const checklist = ref<{ name: string; status: string; notes: string; photo: File | null }[]>([
  { name: 'Jobcard 1', status: '', notes: '', photo: null },
  { name: 'Jobcard 2', status: '', notes: '', photo: null },
  { name: 'Jobcard 3', status: '', notes: '', photo: null },
])

const defect = ref({
  type: '',
  severity: '',
  component: 'Gasket-45B-SE',
  description: '',
})

const handleChecklistUpload = (index: number, event: Event) => {
  const target = event.target as HTMLInputElement | null
  if (target && target.files) {
    const file = target.files[0]
    checklist.value[index].photo = file
  }
}
</script>

<style>
button {
  cursor: pointer;
}
</style>
