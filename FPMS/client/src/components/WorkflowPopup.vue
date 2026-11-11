<template>
  <div>
    <Popup
      :visible="showWorkflowsPopup"
      @update:visible="(value: boolean) => emitEvent('update:showWorkflowsPopup', value)"
    >
      <div>
        <h1 class="mb-6 text-3xl font-extrabold">Existing Workflows</h1>
        <div class="mb-4 flex items-center">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search workflows..."
            class="rounded border p-2"
          />
          <select v-model="selectedCategory" class="ml-2 rounded border p-2">
            <option value="">All Categories</option>
            <option v-for="product in apiProducts" :key="product.id" :value="product.id">
              {{ product.name }}
            </option>
          </select>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full border text-center">
            <thead>
              <tr class="bg-blue-500 text-white">
                <th class="border border-gray-700 px-4 py-2">Workflow Name</th>
                <th class="border border-gray-700 px-4 py-2">Product</th>
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
                v-if="workflowsLoading"
                :rows="4"
                :cols="userRole === 'Production Manager' ? 3 : 2"
              />
              <tr v-for="workflow in filteredWorkflows" :key="workflow.id" class="border-t">
                <td class="border border-gray-700 px-4 py-2">{{ workflow.name }}</td>
                <td class="border border-gray-700 px-4 py-2">
                  {{ getProductName(workflow.product) }}
                </td>
                <td
                  v-if="userRole === 'Production Manager'"
                  class="border border-gray-700 px-4 py-2"
                >
                  <button
                    @click="() => viewWorkflow(workflow.id)"
                    class="mr-2 rounded bg-blue-600 px-3 py-1 text-white hover:bg-blue-500"
                  >
                    View
                  </button>
                  <button
                    @click="() => editWorkflow(workflow.id)"
                    class="mr-2 rounded bg-green-600 px-3 py-1 text-white hover:bg-green-500"
                  >
                    Edit
                  </button>
                  <button
                    @click="() => deleteWorkflow(workflow.id)"
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
        @click="() => (showCreateWorkflowPopup = true)"
        class="mt-4 rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-500"
      >
        Create New Workflow
      </button>
    </Popup>

    <!-- Create Workflow Popup -->
    <Popup :visible="showCreateWorkflowPopup" @update:visible="showCreateWorkflowPopup = $event">
      <div class="flex flex-col justify-start">
        <h1 class="mb-6 text-4xl font-extrabold">Create New Workflow</h1>
        <p class="mb-2 text-xl font-semibold">Workflow Details</p>
      </div>

      <div class="mb-4 flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Workflow Name</p>
          <input
            v-model="workflowName"
            type="text"
            class="rounded border p-2"
            placeholder="Enter Workflow Name"
          />
        </div>
      </div>

      <div class="mb-4 flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Description</p>
          <textarea
            v-model="description"
            class="rounded border p-2"
            placeholder="Enter Workflow Description"
          />
        </div>
      </div>

      <div class="mb-6 flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Product</p>
          <select v-model="selectedProduct" class="rounded border p-2">
            <option :value="null">Select Product</option>
            <option v-for="product in apiProducts" :key="product.id" :value="product.id">
              {{ product.name }}
            </option>
          </select>
        </div>
      </div>

      <h1 class="mb-2 text-xl font-semibold">Define Stages</h1>
      <div class="overflow-x-auto">
        <table class="w-full text-center">
          <thead>
            <tr class="bg-blue-500 text-white">
              <th class="border border-gray-700 px-4 py-2">Stage Name</th>
              <th class="border border-gray-700 px-4 py-2">Description</th>
              <th class="border border-gray-700 px-4 py-2">Assigned Workcenter</th>
              <th class="border border-gray-700 px-4 py-2">Duration (min)</th>
              <th class="border border-gray-700 px-4 py-2">Workorders</th>
              <th class="border border-gray-700 px-4 py-2">Inspection Checkpoints</th>
              <th class="border border-gray-700 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(stage, index) in stages" :key="index" class="border-t">
              <td class="border border-gray-700 px-4 py-2">
                <input
                  v-model="stage.name"
                  class="rounded-xl border p-1"
                  type="text"
                  placeholder="Stage Name"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input
                  v-model="stage.description"
                  class="rounded-xl border p-1"
                  type="text"
                  placeholder="Description"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <select v-model="stage.assigned_work_center" class="rounded border p-2">
                  <option :value="null">Select Workcenter</option>
                  <option v-for="wc in workCenters" :key="wc.id" :value="wc.id">
                    {{ wc.name }}
                  </option>
                </select>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input
                  v-model="stage.duration"
                  class="rounded-xl border p-1"
                  type="number"
                  placeholder="Duration"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input
                  v-model="stage.work_order"
                  class="rounded-xl border p-1"
                  type="text"
                  placeholder="Workorder"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <button
                  @click="
                    () => {
                      showCreateQualityInspectionCheckpointPopup = true
                    }
                  "
                  class="mt-2 rounded bg-gray-300 px-2 py-1 text-black hover:bg-gray-400"
                >
                  Create Checkpoint
                </button>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <button
                  @click="() => removeStage(index)"
                  class="rounded bg-red-600 px-3 py-1 text-white hover:bg-red-500"
                >
                  Remove
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <button
          @click="addStage"
          class="mt-4 w-2/12 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
        >
          Add Stage
        </button>
      </div>

      <div class="mt-4 flex justify-end gap-4">
        <button
          @click="resetForm"
          class="w-2/12 cursor-pointer rounded-lg bg-gray-600 p-1.5 text-white"
        >
          Cancel
        </button>
        <button
          @click="saveWorkflow"
          class="w-2/12 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
        >
          Save
        </button>
      </div>
    </Popup>

    <!-- Edit Workflow Popup -->
    <Popup :visible="showEditWorkflowPopup" @update:visible="showEditWorkflowPopup = $event">
      <div class="flex flex-col justify-start">
        <h1 class="mb-6 text-4xl font-extrabold">Edit Workflow</h1>
        <p class="mb-2 text-xl font-semibold">Workflow Details</p>
      </div>

      <div class="mb-4 flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Workflow Name</p>
          <input
            v-model="workflowName"
            type="text"
            class="rounded border p-2"
            placeholder="Enter Workflow Name"
          />
        </div>
      </div>

      <div class="mb-4 flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Description</p>
          <textarea
            v-model="description"
            class="rounded border p-2"
            placeholder="Enter Workflow Description"
          />
        </div>
      </div>

      <div class="mb-6 flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Product</p>
          <select v-model="selectedProduct" class="rounded border p-2">
            <option :value="null">Select Product</option>
            <option v-for="product in apiProducts" :key="product.id" :value="product.id">
              {{ product.name }}
            </option>
          </select>
        </div>
      </div>

      <h1 class="mb-2 text-xl font-semibold">Define Stages</h1>
      <div class="overflow-x-auto">
        <table class="w-full text-center">
          <thead>
            <tr class="bg-blue-500 text-white">
              <th class="border border-gray-700 px-4 py-2">Stage Name</th>
              <th class="border border-gray-700 px-4 py-2">Description</th>
              <th class="border border-gray-700 px-4 py-2">Assigned Workcenter</th>
              <th class="border border-gray-700 px-4 py-2">Duration (min)</th>
              <th class="border border-gray-700 px-4 py-2">Workorders</th>
              <th class="border border-gray-700 px-4 py-2">Inspection Checkpoints</th>
              <th class="border border-gray-700 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(stage, index) in stages" :key="index" class="border-t">
              <td class="border border-gray-700 px-4 py-2">
                <input
                  v-model="stage.name"
                  class="rounded-xl border p-1"
                  type="text"
                  placeholder="Stage Name"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input
                  v-model="stage.description"
                  class="rounded-xl border p-1"
                  type="text"
                  placeholder="Description"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <select v-model="stage.assigned_work_center" class="rounded border p-2">
                  <option :value="null">Select Workcenter</option>
                  <option v-for="wc in workCenters" :key="wc.id" :value="wc.id">
                    {{ wc.name }}
                  </option>
                </select>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input
                  v-model="stage.duration"
                  class="rounded-xl border p-1"
                  type="number"
                  placeholder="Duration"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input
                  v-model="stage.work_order"
                  class="rounded-xl border p-1"
                  type="text"
                  placeholder="Workorder"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <button
                  @click="() => (showCreateQualityInspectionCheckpointPopup = true)"
                  class="mt-2 rounded bg-gray-300 px-2 py-1 text-black hover:bg-gray-400"
                >
                  Create Checkpoint
                </button>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <button
                  @click="() => removeStage(index)"
                  class="rounded bg-red-600 px-3 py-1 text-white hover:bg-red-500"
                >
                  Remove
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <button
          @click="addStage"
          class="mt-4 w-2/12 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
        >
          Add Stage
        </button>
      </div>

      <div class="mt-4 flex justify-end gap-4">
        <button
          @click="resetForm"
          class="w-2/12 cursor-pointer rounded-lg bg-gray-600 p-1.5 text-white"
        >
          Cancel
        </button>
        <button
          @click="saveWorkflow"
          class="w-2/12 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
        >
          Save
        </button>
      </div>
    </Popup>

    <!-- View Workflow Popup -->
    <Popup :visible="showViewWorkflowPopup" @update:visible="showViewWorkflowPopup = $event">
      <div class="flex flex-col justify-start">
        <h1 class="mb-6 text-4xl font-extrabold">View Workflow</h1>
        <p class="mb-2 text-xl font-semibold">Workflow Details</p>
      </div>

      <div class="mb-4 flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Workflow Name</p>
          <input v-model="currentWorkflow.name" type="text" class="rounded border p-2" readonly />
        </div>
      </div>

      <div class="mb-4 flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Description</p>
          <textarea v-model="currentWorkflow.description" class="rounded border p-2" readonly />
        </div>
      </div>

      <div class="mb-6 flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Product</p>
          <input
            :value="getProductName(currentWorkflow.product)"
            type="text"
            class="rounded border p-2"
            readonly
          />
        </div>
      </div>

      <h1 class="mb-2 text-xl font-semibold">Stages</h1>
      <div class="overflow-x-auto">
        <table class="w-full text-center">
          <thead>
            <tr class="bg-blue-500 text-white">
              <th class="border border-gray-700 px-4 py-2">Stage Name</th>
              <th class="border border-gray-700 px-4 py-2">Description</th>
              <th class="border border-gray-700 px-4 py-2">Workcenter</th>
              <th class="border border-gray-700 px-4 py-2">Duration (min)</th>
              <th class="border border-gray-700 px-4 py-2">Workorder</th>
              <th class="border border-gray-700 px-4 py-2">Inspection Checkpoints</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(stage, index) in currentWorkflow.stages" :key="index" class="border-t">
              <td class="border border-gray-700 px-4 py-2">{{ stage.name }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ stage.description }}</td>
              <td class="border border-gray-700 px-4 py-2">
                {{ getWorkCenterName(stage.assigned_work_center) }}
              </td>
              <td class="border border-gray-700 px-4 py-2">{{ stage.duration }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ stage.work_order }}</td>
              <td class="border border-gray-700 px-4 py-2">
                <ul>
                  <li v-for="cpId in stage.inspection_checkpoints" :key="cpId">
                    {{ getCheckpointName(cpId) }}
                  </li>
                </ul>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-4 flex justify-end">
        <button
          @click="() => (showViewWorkflowPopup = false)"
          class="w-2/12 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
        >
          Close
        </button>
      </div>
    </Popup>

    <!-- Quality Inspection Checkpoint Popup -->
    <Popup
      :visible="showCreateQualityInspectionCheckpointPopup"
      @update:visible="showCreateQualityInspectionCheckpointPopup = $event"
    >
      <div>
        <div class="flex flex-col items-center justify-center">
          <h1 class="mb-6 text-4xl font-extrabold">Create Quality Inspection Checkpoint</h1>
        </div>

        <div class="mb-3 flex flex-row gap-4">
          <div class="flex w-full flex-col">
            <p class="mb-2 font-medium">Checkpoint Name</p>
            <input
              v-model="checkpointName"
              type="text"
              class="rounded border p-2"
              placeholder="Enter Checkpoint Name"
            />
          </div>
        </div>
        <div class="mb-3 flex flex-row gap-4">
          <div class="flex w-full flex-col">
            <p class="mb-2 font-medium">Inspection Criteria</p>
            <textarea
              v-model="inspectionCriteria"
              class="rounded border p-2"
              placeholder="Describe inspection criteria"
            />
          </div>
        </div>
        <div class="flex flex-row gap-4">
          <div class="flex w-full flex-col">
            <p class="mb-2 font-medium">Tools/Equipment Required</p>
            <input
              v-model="toolsEquipmentRequired"
              type="text"
              class="rounded border p-2"
              placeholder="List tools or equipment required"
            />
          </div>
        </div>
      </div>
      <div class="mt-4 flex justify-end gap-4">
        <button
          @click="() => (showCreateQualityInspectionCheckpointPopup = false)"
          class="w-2/12 cursor-pointer rounded-lg bg-gray-600 p-1.5 text-white"
        >
          Cancel
        </button>
        <button
          @click="saveQualityInspectionCheckpoint"
          class="w-2/12 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
        >
          Save
        </button>
      </div>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Popup from '@/components/popup.vue'
import SkeletonRows from '@/components/SkeletonRows.vue'
import { useWorkflowsStore } from '@/stores/useWorkflows'
import { baseApiUrl } from '@/api.ts'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

defineProps<{
  showWorkflowsPopup: boolean
}>()

const emitEvent = defineEmits(['update:showWorkflowsPopup'])

// Stores
const userStore = useUserStore()
const userRole = userStore.user?.role
const workflowsStore = useWorkflowsStore()

// Popup visibility
const showCreateWorkflowPopup = ref(false)
const showEditWorkflowPopup = ref(false)
const showViewWorkflowPopup = ref(false)
const showCreateQualityInspectionCheckpointPopup = ref(false)

// Data
const workflows = ref<any[]>([])
const workflowsLoading = ref(false)
const apiProducts = ref<any[]>([])
const workCenters = ref<any[]>([])
const inspectionCheckpoints = ref<any[]>([])
const currentWorkflow = ref<any>({})

// Form data
const searchQuery = ref('')
const selectedCategory = ref('')
const workflowName = ref('')
const description = ref('')
const selectedProduct = ref<number | null>(null)
const stages = ref<any[]>([])
const editingWorkflowId = ref<number | null>(null)

// Quality inspection checkpoint form
const checkpointName = ref('')
const inspectionCriteria = ref('')
const toolsEquipmentRequired = ref('')

// Computed
const filteredWorkflows = computed(() => {
  return workflows.value.filter((workflow) => {
    const matchesSearch = workflow.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory =
      selectedCategory.value === '' || workflow.product.toString() === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})

// Methods
function getProductName(productId: number) {
  const product = apiProducts.value.find((p) => p.id === productId)
  return product ? product.name : 'Unknown'
}

function getWorkCenterName(workCenterId: number) {
  const wc = workCenters.value.find((w) => w.id === workCenterId)
  return wc ? wc.name : 'Unknown'
}

function getCheckpointName(checkpointId: number) {
  const cp = inspectionCheckpoints.value.find((c) => c.id === checkpointId)
  return cp ? cp.checkpoint_name : 'Unknown'
}

function addStage() {
  stages.value.push({
    name: '',
    description: '',
    assigned_work_center: null,
    duration: null,
    work_order: '',
    inspection_checkpoints: [],
  })
}

function removeStage(index: number) {
  stages.value.splice(index, 1)
}

async function fetchWorkflows() {
  workflowsLoading.value = true
  try {
    const response = await axios.get(`${baseApiUrl}/workflows/`)
    workflows.value = response.data
  } catch (error) {
    console.error('Error fetching workflows:', error)
  } finally {
    workflowsLoading.value = false
  }
}

async function fetchProducts() {
  try {
    const response = await axios.get(`${baseApiUrl}/products/`)
    apiProducts.value = response.data
  } catch (error) {
    console.error('Error fetching products:', error)
  }
}

async function fetchWorkCenters() {
  try {
    const response = await axios.get(`${baseApiUrl}/workcentre/workcenters/`)
    workCenters.value = response.data
  } catch (error) {
    console.error('Error fetching work centers:', error)
  }
}

async function fetchInspectionCheckpoints() {
  try {
    const response = await axios.get(`${baseApiUrl}/inspection-checkpoints/`)
    inspectionCheckpoints.value = response.data
  } catch (error) {
    console.error('Error fetching inspection checkpoints:', error)
  }
}

async function saveWorkflow() {
  try {
    const workflowData = {
      name: workflowName.value,
      description: description.value,
      product_id: selectedProduct.value,
      assigned_work_center: stages.value[0]?.assigned_work_center || null,
      stages: stages.value,
    }

    if (editingWorkflowId.value) {
      await axios.put(`${baseApiUrl}/workflows/${editingWorkflowId.value}/`, workflowData)
    } else {
      await axios.post(`${baseApiUrl}/workflows/`, workflowData)
    }

    await fetchWorkflows()
    resetForm()
  } catch (error) {
    console.error('Error saving workflow:', error)
  }
}

async function editWorkflow(id: number) {
  try {
    const response = await axios.get(`${baseApiUrl}/workflows/${id}/`)
    const workflow = response.data

    editingWorkflowId.value = workflow.id
    workflowName.value = workflow.name
    description.value = workflow.description
    selectedProduct.value = workflow.product
    stages.value = workflow.stages || []
    showEditWorkflowPopup.value = true
  } catch (error) {
    console.error('Error fetching workflow:', error)
  }
}

async function viewWorkflow(id: number) {
  try {
    const response = await axios.get(`${baseApiUrl}/workflows/${id}/`)
    currentWorkflow.value = response.data
    showViewWorkflowPopup.value = true
  } catch (error) {
    console.error('Error fetching workflow:', error)
  }
}

async function deleteWorkflow(id: number) {
  const index = workflows.value.findIndex((workflow) => workflow.id === id)
  if (index === -1) return
  const removed = workflows.value[index]
  workflows.value.splice(index, 1) // optimistic removal
  try {
    await axios.delete(`${baseApiUrl}/workflows/${id}/`)
  } catch (error) {
    workflows.value.splice(index, 0, removed) // rollback on failure
    console.error('Error deleting workflow:', error)
  }
}

async function saveQualityInspectionCheckpoint() {
  try {
    const checkpointData = {
      checkpoint_name: checkpointName.value,
      inspection_criteria: inspectionCriteria.value,
      tools_equipment_required: toolsEquipmentRequired.value,
    }

    await axios.post(`${baseApiUrl}/inspection-checkpoints/`, checkpointData)
    await fetchInspectionCheckpoints()

    checkpointName.value = ''
    inspectionCriteria.value = ''
    toolsEquipmentRequired.value = ''
    showCreateQualityInspectionCheckpointPopup.value = false
  } catch (error) {
    console.error('Error saving inspection checkpoint:', error)
  }
}

function resetForm() {
  editingWorkflowId.value = null
  workflowName.value = ''
  description.value = ''
  selectedProduct.value = null
  stages.value = []
  showCreateWorkflowPopup.value = false
  showEditWorkflowPopup.value = false
}

// Initialize
onMounted(() => {
  fetchWorkflows()
  fetchProducts()
  fetchWorkCenters()
  fetchInspectionCheckpoints()
})
</script>

<style scoped>
button {
  cursor: pointer;
}

input,
select,
textarea {
  border: 1px solid #ccc;
}
</style>
