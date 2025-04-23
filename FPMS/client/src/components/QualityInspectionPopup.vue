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
            <tr class="">
              <th class="border border-gray-700 px-4 py-2">Work Order ID</th>
              <th class="border border-gray-700 px-4 py-2">Product Name</th>
              <th class="border border-gray-700 px-4 py-2">Quantity</th>
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
              <td class="border border-gray-700 px-4 py-2">{{ item.quantity }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ item.dueDate }}</td>
              <td class="border border-gray-700 px-4 py-2">
                <span
                  :class="
                    item.status === 'Active'
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-200 text-gray-600'
                  "
                  class="rounded-full px-2 py-1 text-xs"
                >
                  {{ item.status }}
                </span>
              </td>
              <td class="space-x-2 border border-gray-700 px-4 py-2">
                <button
                  @click="startInspection(item.id)"
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
    <div class="mt-2 flex flex-row justify-center space-x-4">
      <button class="w-2/12 rounded-lg bg-blue-600 p-1.5 text-white">Prev</button>
      <p class="mt-2">Page 1 of 5</p>
      <button class="w-2/12 rounded-lg bg-blue-600 p-1.5 text-white">Next</button>
    </div>
  </Popup>

  <Popup :visible="showStartInspectionPopup" @update:visible="showStartInspectionPopup = $event">
    <div class="">
      <!-- Header -->
      <h2 class="mb-4 text-xl font-semibold">Start Inspection</h2>

      <!-- Work Order Info -->
      <div class="mb-6 text-sm">
        <p><strong>Work Order ID:</strong> WO-1234</p>
        <p><strong>Product:</strong> SKU-45B (Steel Bracket)</p>
        <p><strong>Production Line:</strong> Line 3 - Assembly</p>
        <p><strong>Inspection Checkpoint:</strong> Final Assembly QA</p>
      </div>

      <!-- Inspection Checklist -->
      <div class="mb-6">
        <h3 class="mb-2 text-lg font-semibold">Inspection Checklist</h3>
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
                <label
                  ><input
                    type="radio"
                    :name="'status' + index"
                    value="Pass"
                    v-model="item.status"
                    class="mr-1"
                  />
                  Pass</label
                >
                <label class="ml-4"
                  ><input
                    type="radio"
                    :name="'status' + index"
                    value="Fail"
                    v-model="item.status"
                    class="mr-1"
                  />
                  Fail</label
                >
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
              <label
                ><input type="radio" value="Critical" v-model="defect.severity" /> Critical</label
              >
              <label><input type="radio" value="Major" v-model="defect.severity" /> Major</label>
              <label><input type="radio" value="Minor" v-model="defect.severity" /> Minor</label>
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
          <button class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
            Submit Inspection
          </button>
        </div>
      </div>
    </div>
  </Popup>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Popup from '@/components/popup.vue'
import { useQualityInspectionsStore } from '@/stores/useQualityInspections'

const qualityInspectionsStore = useQualityInspectionsStore()

const showStartInspectionPopup = ref(false)

const instructions = computed(() => qualityInspectionsStore.inspections)

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
  if (target && target.files) {
    const file = target.files[0]
    if (file) {
      checklist.value[index].photo = file
    }
  }
}

const startInspection = async (inspectionId: string) => {
  await qualityInspectionsStore.updateInspection(inspectionId, { status: 'Active' })
}

const handleApprove = () => {
  console.log('Inspection Approved')
  // Add logic to handle approval
}

const handleRework = () => {
  console.log('Inspection marked for Rework')
  // Add logic to handle rework
}

const handleReject = () => {
  console.log('Inspection Rejected')
  // Add logic to handle rejection
}

const fetchInspections = async () => {
  try {
    await qualityInspectionsStore.fetchInspections()
  } catch (error) {
    console.error('Failed to fetch inspections:', error)
  }
}

onMounted(() => {
  fetchInspections()
})
</script>

<style>
button {
  cursor: pointer;
}
</style>
