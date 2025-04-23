<template>
  <div>
    <Popup
      :visible="showWorkflowsPopup"
      @update:visible="(value: boolean) => emitEvent('update:showWorkflowsPopup', value)"
    >
      <div>
        <h1 class="mb-6 text-3xl font-extrabold">Existing Workflows</h1>
        <div class="overflow-x-auto">
          <table class="w-full border text-center">
            <thead>
              <tr class="bg-blue-500 text-white">
                <th class="border border-gray-700 px-4 py-2">Workflow Name</th>
                <th
                  v-if="userRole === 'Production Manager'"
                  class="border border-gray-700 px-4 py-2"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="workflow in filteredProducts"
                :key="workflow.id"
                class="border-t hover:bg-gray-100"
              >
                <td class="border border-gray-700 px-4 py-2">{{ workflow.name }}</td>
                <td v-if="userRole === 'Production Manager'" class="border border-gray-700 px-4 py-2">
                  <button
                    v-if="userRole === 'Production Manager'"
                    @click="editWorkflow(workflow.id)"
                    class="mr-2 rounded bg-green-600 px-3 py-1 text-white hover:bg-green-500"
                  >
                    Edit
                  </button>
                  <button
                    v-if="userRole === 'Production Manager'"
                    @click="deleteWorkflow(workflow.id)"
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
        @click="showCreateWorkflowPopup = true"
        class="mr-2 rounded bg-blue-600 px-3 py-1 text-white hover:bg-blue-500"
      >
        Create New Workflow
      </button>
    </Popup>

    <Popup :visible="showViewWorkflowPopup" @update:visible="showViewWorkflowPopup = $event">
      <div class="flex flex-col justify-start">
        <h1 class="mb-6 text-4xl font-extrabold">View Workflow</h1>
        <p class="mb-2 text-xl font-semibold">Workflow Details</p>
      </div>

      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Workflow Name</p>
          <input type="text" class="rounded border p-2" placeholder="Enter Workflow Name" />
        </div>
      </div>
      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Description</p>
          <textarea
            type="text"
            class="rounded border p-2"
            placeholder="Enter Workflow Description"
          />
        </div>
      </div>
      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Product/Process Selection</p>
          <select v-model="selectedCategory" class="rounded border p-2">
            <option value="">Select Product</option>
            <option v-for="product in workflowsStore.products" :key="product" :value="product">
              {{ product }}
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
              <th class="border border-gray-700 px-4 py-2">Inspection checkpoint</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="workflow in filteredProducts"
              :key="workflow.id"
              class="border-t hover:bg-gray-100"
            >
              <td class="border border-gray-700 px-4 py-2">
                <input
                  class="rounded-xl border border-black p-1"
                  type="text"
                  placeholder="Stage Name"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input
                  class="rounded-xl border border-black p-1"
                  type="text"
                  placeholder="Description"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <select v-model="selectedCategory" class="rounded border p-2">
                  <option value="">Select Workcenter</option>
                  <option>Category 1</option>
                  <option>Category 2</option>
                </select>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input
                  class="rounded-xl border border-black p-1"
                  type="text"
                  placeholder="Duration"
                />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <select v-model="selectedCategory" class="rounded border p-2">
                  <option value="">Select Workorder</option>
                  <option>Category 1</option>
                  <option>Category 2</option>
                </select>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <input class="rounded-xl border border-black p-1" type="text" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Popup>
    <Popup :visible="showEditWorkflowPopup" @update:visible="showEditWorkflowPopup = $event">
      <div class="flex flex-col justify-start">
        <h1 class="mb-6 text-4xl font-extrabold">Edit Workflow</h1>
        <p class="mb-2 text-xl font-semibold">Workflow Details</p>
      </div>

      <!-- Workflow name and description -->
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
          <p class="font-medium">Product/Process Selection</p>
          <select v-model="selectedProduct" class="rounded border p-2">
            <option value="">Select Product</option>
            <option v-for="product in workflowsStore.products" :key="product" :value="product">
              {{ product }}
            </option>
          </select>
        </div>
      </div>

      <!-- Stages -->
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
              <th class="border border-gray-700 px-4 py-2">Inspection checkpoint</th>
              <th class="border border-gray-700 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(stage, index) in stages" :key="index" class="border-t hover:bg-gray-100">
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
                <select class="rounded border p-2">
                  <optgroup v-for="(workcenter, index) in workCenters">
                    <option>{{ workcenter.name }}</option>
                  </optgroup>
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
                <select class="rounded border p-2">
                  <option value="">Select Workorder</option>
                  <option>WO-ELEC-101</option>
                  <option>WO-QUAL-303</option>
                </select>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <button
                  @click="showCreateQualityInspectionCheckpointPopup = true"
                  class="w-9/12 rounded-md bg-gray-300 p-0.5"
                >
                  Create
                </button>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <button
                  @click="removeStage(index)"
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

      <!-- Save -->
      <div class="flex justify-end">
        <button
          @click="saveWorkflow"
          class="mt-4 w-2/12 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
        >
          Save
        </button>
      </div>
    </Popup>
    <Popup :visible="showCreateWorkflowPopup" @update:visible="showCreateWorkflowPopup = $event">
      <div class="flex flex-col justify-start">
        <h1 class="mb-6 text-4xl font-extrabold">Create New Workflow</h1>
        <p class="mb-2 text-xl font-semibold">Workflow Details</p>
      </div>

      <!-- Workflow name and description -->
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
          <p class="font-medium">Product/Process Selection</p>
          <select v-model="selectedProduct" class="rounded border p-2">
            <option value="">Select Product</option>
            <option v-for="product in workflowsStore.products" :key="product" :value="product">
              {{ product }}
            </option>
          </select>
        </div>
      </div>

      <!-- Stages -->
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
              <th class="border border-gray-700 px-4 py-2">Inspection checkpoint</th>
              <th class="border border-gray-700 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(stage, index) in stages" :key="index" class="border-t hover:bg-gray-100">
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
                <select v-model="stage.workcenter" class="rounded border p-2">
                  <optgroup v-for="(workcenter, index) in workCenters">
                    <option>{{ workcenter.name }}</option>
                  </optgroup>
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
                <select v-model="stage.workorder" class="rounded border p-2">
                  <option value="">Select Workorder</option>
                  <option>WO-ELEC-101</option>
                  <option>WO-QUAL-303</option>
                </select>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <button
                  @click="showCreateQualityInspectionCheckpointPopup = true"
                  class="w-9/12 rounded-md bg-gray-300 p-0.5"
                >
                  Create
                </button>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <button
                  @click="removeStage(index)"
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

      <!-- Save -->
      <div class="flex justify-end">
        <button
          @click="saveWorkflow"
          class="mt-4 w-2/12 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
        >
          Save
        </button>
      </div>
    </Popup>

    <Popup
      :visible="showCreateQualityInspectionCheckpointPopup"
      @update:visible="showCreateQualityInspectionCheckpointPopup = $event"
    >
      <div>
        <div class="flex flex-col items-center justify-center">
          <h1 class="mb-6 text-4xl font-extrabold">Create Quality Inspection Checkpoints</h1>
        </div>

        <div class="mb-3 flex flex-row gap-4">
          <div class="flex w-full flex-col">
            <p class="mb-2 font-medium">Checkpoint Name</p>
            <input type="text" class="rounded border p-2" placeholder="Enter Checkpoint Name" />
          </div>
        </div>
        <div class="mb-3 flex flex-row gap-4">
          <div class="flex w-full flex-col">
            <p class="mb-2 font-medium">Inspection Criteria</p>
            <textarea
              type="text"
              class="rounded border p-2"
              placeholder="Describe inspection criteria (e.g., Dimensions, checks, material validation)"
            />
          </div>
        </div>
        <div class="flex flex-row gap-4">
          <div class="flex w-full flex-col">
            <p class="mb-2 font-medium">Tools/Equipment Required</p>
            <input
              type="text"
              class="rounded border p-2"
              placeholder="List tools or equipment required"
            />
          </div>
        </div>
      </div>
      <div class="flex justify-end">
        <button class="mt-4 w-2/12 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white">
          Save Checkpoint
        </button>
      </div>
    </Popup>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Popup from '@/components/popup.vue'
import { useWorkflowsStore } from '@/stores/useWorkflows'
import { useAxios } from '@vueuse/integrations/useAxios'
import { baseApiUrl } from '@/api.ts'
import { useOrdersStore } from '@/stores/useOrders'
import { useUserStore } from '@/stores/user'

const ordersStore = useOrdersStore()
const userStore = useUserStore()
const userRole = userStore.user?.role

const workflowsStore = useWorkflowsStore()

// Load products when the component is mounted
onMounted(() => {
  workflowsStore.loadProductsFromOrders()
})

const showCreateWorkflowPopup = defineModel<boolean>('visible')
const showEditWorkflowPopup = ref(false)
const showViewWorkflowPopup = ref(false)
const showCreateQualityInspectionCheckpointPopup = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('')
const variantAvailability = ref('')

const emitEvent = defineEmits(['close', 'submit', 'update:showWorkflowsPopup'])
defineProps<{
  showWorkflowsPopup: boolean
}>()

const filteredProducts = computed(() => {
  return workflowsStore.workflows.filter((workflow) => {
    const matchesSearch = workflow.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory =
      selectedCategory.value === '' || workflow.product === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})

const workflowName = ref('')
const description = ref('')
const selectedProduct = ref('')
const stages = ref([])
const editingWorkflowId = ref<string | null>(null)

function addStage() {
  stages.value.push({ name: '', description: '', workcenter: '', duration: null, workorder: '' })
}

function removeStage(index: number) {
  stages.value.splice(index, 1)
}

function saveWorkflow() {
  const data = {
    id: editingWorkflowId.value || workflowsStore.getLastAndUniqueId,
    name: workflowName.value,
    description: description.value,
    product: selectedProduct.value,
    stages: stages.value,
  }

  if (editingWorkflowId.value) {
    workflowsStore.editWorkflow(editingWorkflowId.value, data)
  } else {
    workflowsStore.createWorkflow(data)
    resetForm()
  }

  resetForm()
}

function editWorkflow(id: string) {
  const workflow = workflowsStore.getWorkflowById(id)
  if (workflow) {
    editingWorkflowId.value = workflow.id
    workflowName.value = workflow.name
    description.value = workflow.description
    selectedProduct.value = workflow.product
    stages.value = [...workflow.stages]
    showEditWorkflowPopup.value = true
  }
}

function deleteWorkflow(id: string) {
  workflowsStore.deleteWorkflow(id)
}

function resetForm() {
  editingWorkflowId.value = null
  workflowName.value = ''
  description.value = ''
  selectedProduct.value = ''
  stages.value = []
  showCreateWorkflowPopup.value = false
  showEditWorkflowPopup.value = false
}
const { data: workCenters } = useAxios(`${baseApiUrl}/workcentre/workcenters/`, { method: 'GET' })
</script>

<style>
button {
  cursor: pointer;
}
</style>
