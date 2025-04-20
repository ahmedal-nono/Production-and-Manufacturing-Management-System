<template>
  <Popup
    :visible="showWorkinstructionPopup"
    @update:visible="(value: boolean) => emitEvent('update:showWorkinstructionPopup', value)"
  >
    <div class="">
      <!-- Header -->
      <div class="mb-4 flex items-center justify-between">
        <h2 class="text-2xl font-bold">Work Instructions Library</h2>
        <button
          @click="showCreateWorkinstructionPopup = true"
          class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          + Create New Work Instruction
        </button>
      </div>

      <!-- Filters -->
      <div class="mb-4 flex flex-wrap items-center gap-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by title, product, or keyword"
          class="w-full flex-1 rounded border px-4 py-2 sm:w-auto"
          @input="fetchWorkInstructions"
        />
        <select
          v-model="statusFilter"
          class="rounded border px-4 py-2"
          @change="fetchWorkInstructions"
        >
          <option value="">All Statuses</option>
          <option value="Not Started">Not Started</option>
          <option value="In Progress">In Progress</option>
          <option value="Completed">Completed</option>
        </select>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center py-8">
        <div
          class="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"
        ></div>
      </div>

      <!-- Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr>
              <th class="border border-gray-700 px-4 py-2">Title</th>
              <th class="border border-gray-700 px-4 py-2">Tools Required</th>
              <th class="border border-gray-700 px-4 py-2">Last Updated</th>
              <th class="border border-gray-700 px-4 py-2">Status</th>
              <th class="border border-gray-700 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, index) in workInstructions"
              :key="index"
              class="border bg-white hover:bg-gray-50"
            >
              <td class="border border-gray-700 px-4 py-2">{{ item.title }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ item.tools_required }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ formatDate(item.updated_at) }}</td>
              <td class="border border-gray-700 px-4 py-2">
                <span :class="statusClass(item.status)" class="rounded-full px-2 py-1 text-xs">
                  {{ item.status }}
                </span>
              </td>
              <td class="space-x-2 border border-gray-700 px-4 py-2">
                <button
                  @click="viewWorkInstruction(item.id)"
                  class="m-1 rounded bg-gray-200 px-2 py-1 text-sm hover:bg-gray-300"
                >
                  View
                </button>
                <button
                  @click="editWorkInstruction(item.id)"
                  class="m-1 rounded bg-gray-200 px-2 py-1 text-sm hover:bg-gray-300"
                >
                  Edit
                </button>
                <button
                  @click="deleteWorkInstruction(item.id)"
                  class="m-1 rounded bg-red-200 px-2 py-1 text-sm hover:bg-red-300"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Popup>

  <!-- Create Work Instruction Popup -->
  <Popup
    :visible="showCreateWorkinstructionPopup"
    @update:visible="showCreateWorkinstructionPopup = $event"
  >
    <div class="">
      <h1 class="mb-6 text-2xl font-bold">Create New Work Instruction</h1>

      <!-- Basic Information -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Work instruction Information</h2>
        <div class="mb-4">
          <label class="mb-1 block font-medium">Title</label>
          <input
            v-model="form.title"
            type="text"
            placeholder="E.g., Brake System Assembly"
            class="w-full rounded border px-3 py-2"
            required
          />
        </div>
        <div>
          <label class="mb-1 block font-medium">Status</label>
          <select v-model="form.status" class="w-full rounded border px-3 py-2">
            <option value="Not Started">Not Started</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
          </select>
        </div>
      </section>

      <!-- Overall Description -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Overall Description</h2>
        <textarea
          v-model="form.step_description"
          rows="3"
          class="w-full rounded border px-3 py-2"
          placeholder="Overall description of the work instruction"
          required
        ></textarea>
      </section>

      <!-- Step-by-Step Instructions -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Step-by-Step Instructions</h2>
        <div
          v-for="(step, index) in form.task_steps"
          :key="index"
          class="relative mb-6 rounded border p-3"
        >
          <label class="mb-1 block font-medium">Step {{ index + 1 }}</label>
          <textarea
            v-model="form.task_steps[index]"
            rows="3"
            class="w-full rounded border px-3 py-2"
            placeholder="Enter step description"
            required
          ></textarea>
          <button
            @click="removeStep(index)"
            v-if="form.task_steps.length > 1"
            class="absolute top-2 right-4 text-lg text-red-500 hover:text-red-700"
          >
            Delete
          </button>
        </div>
        <button
          @click="addStep"
          class="rounded border bg-gray-100 px-4 py-2 text-sm hover:bg-gray-200"
        >
          + Add Step
        </button>
      </section>

      <!-- Tools & Materials -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Tools & Materials</h2>
        <div class="mb-4">
          <label class="mb-1 block font-medium">Tools Required</label>
          <textarea
            v-model="form.tools_required"
            rows="3"
            class="w-full rounded border px-3 py-2"
            required
          ></textarea>
        </div>
        <div>
          <label class="mb-1 block font-medium">Materials Required</label>
          <textarea
            v-model="form.materials_required"
            rows="3"
            class="w-full rounded border px-3 py-2"
            required
          ></textarea>
        </div>
      </section>

      <!-- Buttons -->
      <div class="flex justify-end gap-4">
        <button
          @click="createWorkInstruction"
          class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          Save & Publish
        </button>
      </div>
    </div>
  </Popup>

  <!-- View Work Instruction Popup -->
  <Popup
    :visible="showViewWorkinstructionPopup"
    @update:visible="showViewWorkinstructionPopup = $event"
  >
    <div v-if="currentWorkInstruction" class="">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <h1 class="text-2xl font-bold">{{ currentWorkInstruction.title }}</h1>
        <div class="space-x-2">
          <button class="rounded bg-blue-500 px-3 py-1 text-white hover:bg-blue-600">PDF</button>
          <button
            @click="editWorkInstruction(currentWorkInstruction.id)"
            class="rounded bg-blue-100 px-3 py-1 text-blue-700 hover:bg-blue-200"
          >
            Edit
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <!-- Left: Instructions -->
        <div class="space-y-6 lg:col-span-2">
          <!-- Overall Description -->
          <div class="rounded bg-white p-4 shadow">
            <h2 class="mb-2 text-lg font-semibold">Description</h2>
            <p class="text-gray-700">{{ currentWorkInstruction.step_description }}</p>
          </div>

          <!-- Steps -->
          <div
            v-for="(step, index) in currentWorkInstruction.task_steps.split('\n')"
            :key="index"
            class="rounded bg-white p-4 shadow"
          >
            <div class="flex items-start gap-4">
              <div class="text-xl font-bold text-gray-600">{{ index + 1 }}</div>
              <div>
                <p class="mb-2 text-gray-700">{{ step }}</p>
              </div>
            </div>
          </div>

          <!-- Tools & Materials -->
          <div class="rounded bg-white p-4 shadow">
            <h2 class="mb-2 text-lg font-semibold">Tools & Materials</h2>
            <div class="mb-4">
              <h3 class="font-medium">Tools Required:</h3>
              <p class="text-gray-700">{{ currentWorkInstruction.tools_required }}</p>
            </div>
            <div>
              <h3 class="font-medium">Materials Required:</h3>
              <p class="text-gray-700">{{ currentWorkInstruction.materials_required }}</p>
            </div>
          </div>
        </div>

        <!-- Right: Details -->
        <div class="space-y-4 rounded bg-white p-4 shadow">
          <div>
            <h2 class="text-md font-semibold text-gray-800">Details</h2>
            <p><strong>Status:</strong> {{ currentWorkInstruction.status }}</p>
            <p>
              <strong>Last Updated:</strong> {{ formatDate(currentWorkInstruction.updated_at) }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </Popup>

  <!-- Edit Work Instruction Popup -->
  <Popup
    :visible="showEditWorkinstructionPopup"
    @update:visible="showEditWorkinstructionPopup = $event"
  >
    <div v-if="currentWorkInstruction" class="">
      <h1 class="mb-6 text-2xl font-bold">Edit Work Instruction</h1>

      <!-- Basic Information -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Work instruction Information</h2>
        <div class="mb-4">
          <label class="mb-1 block font-medium">Title</label>
          <input
            v-model="currentWorkInstruction.title"
            type="text"
            placeholder="E.g., Brake System Assembly"
            class="w-full rounded border px-3 py-2"
            required
          />
        </div>
        <div>
          <label class="mb-1 block font-medium">Status</label>
          <select v-model="currentWorkInstruction.status" class="w-full rounded border px-3 py-2">
            <option value="Not Started">Not Started</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
          </select>
        </div>
      </section>

      <!-- Overall Description -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Overall Description</h2>
        <textarea
          v-model="currentWorkInstruction.step_description"
          rows="3"
          class="w-full rounded border px-3 py-2"
          required
        ></textarea>
      </section>

      <!-- Step-by-Step Instructions -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Step-by-Step Instructions</h2>
        <div
          v-for="(step, index) in currentWorkInstruction.task_steps_array"
          :key="index"
          class="relative mb-6 rounded border p-3"
        >
          <label class="mb-1 block font-medium">Step {{ index + 1 }}</label>
          <textarea
            v-model="currentWorkInstruction.task_steps_array[index]"
            rows="3"
            class="w-full rounded border px-3 py-2"
            required
          ></textarea>
          <button
            @click="removeStep(index)"
            v-if="currentWorkInstruction.task_steps_array.length > 1"
            class="absolute top-2 right-4 text-lg text-red-500 hover:text-red-700"
          >
            Delete
          </button>
        </div>
        <button
          @click="addStep"
          class="rounded border bg-gray-100 px-4 py-2 text-sm hover:bg-gray-200"
        >
          + Add Step
        </button>
      </section>

      <!-- Tools & Materials -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Tools & Materials</h2>
        <div class="mb-4">
          <label class="mb-1 block font-medium">Tools Required</label>
          <textarea
            v-model="currentWorkInstruction.tools_required"
            rows="3"
            class="w-full rounded border px-3 py-2"
            required
          ></textarea>
        </div>
        <div>
          <label class="mb-1 block font-medium">Materials Required</label>
          <textarea
            v-model="currentWorkInstruction.materials_required"
            rows="3"
            class="w-full rounded border px-3 py-2"
            required
          ></textarea>
        </div>
      </section>

      <!-- Buttons -->
      <div class="flex justify-end gap-4">
        <button
          @click="updateWorkInstruction"
          class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          Save Changes
        </button>
      </div>
    </div>
  </Popup>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import Popup from '@/components/popup.vue'

interface WorkInstruction {
  id: number
  title: string
  task_steps: string
  tools_required: string
  materials_required: string
  status: string
  step_description: string
  created_at: string
  updated_at: string
  task_steps_array: string[]
}

const BASE_URL = 'http://127.0.0.1:8000/api'

const showCreateWorkinstructionPopup = ref<boolean>(false)
const showViewWorkinstructionPopup = ref<boolean>(false)
const showEditWorkinstructionPopup = ref<boolean>(false)
const loading = ref<boolean>(false)
const searchQuery = ref<string>('')
const statusFilter = ref<string>('')
const workInstructions = ref<WorkInstruction[]>([])
const currentWorkInstruction = ref<WorkInstruction | null>(null)

const form = reactive({
  title: '',
  task_steps: [''] as string[],
  tools_required: '',
  materials_required: '',
  status: 'Not Started',
  step_description: ''
})

defineProps<{
  showWorkinstructionPopup: boolean
}>()

const emitEvent = defineEmits<{
  (e: 'close'): void
  (e: 'submit'): void
  (e: 'update:showWorkinstructionPopup', value: boolean): void
}>()

// Fetch all work instructions
const fetchWorkInstructions = async () => {
  try {
    loading.value = true
    let url = `${BASE_URL}/work_instructions/`
    const params = new URLSearchParams()

    if (searchQuery.value) {
      params.append('search', searchQuery.value)
    }

    if (statusFilter.value) {
      params.append('status', statusFilter.value)
    }

    if (params.toString()) {
      url += `?${params.toString()}`
    }

    const response = await axios.get(url)
    workInstructions.value = response.data
  } catch (error) {
    console.error('Error fetching work instructions:', error)
  } finally {
    loading.value = false
  }
}

// View a single work instruction
const viewWorkInstruction = async (id: number) => {
  try {
    const response = await axios.get(`${BASE_URL}/work_instructions/${id}/`)
    currentWorkInstruction.value = {
      ...response.data,
      task_steps_array: response.data.task_steps.split('\n').filter(step => step.trim())
    }
    showViewWorkinstructionPopup.value = true
  } catch (error) {
    console.error('Error fetching work instruction:', error)
  }
}

// Edit a work instruction
const editWorkInstruction = async (id: number) => {
  try {
    const response = await axios.get(`${BASE_URL}/work_instructions/${id}/`)
    currentWorkInstruction.value = {
      ...response.data,
      task_steps_array: response.data.task_steps.split('\n').filter(step => step.trim())
    }
    showEditWorkinstructionPopup.value = true
    showViewWorkinstructionPopup.value = false
  } catch (error) {
    console.error('Error fetching work instruction:', error)
  }
}

// Create a new work instruction
const createWorkInstruction = async () => {
  try {
    // Validate required fields
    if (!form.title.trim()) {
      alert('Please enter a title')
      return
    }

    if (!form.step_description.trim()) {
      alert('Please enter an overall description')
      return
    }

    // Filter out empty steps
    const nonEmptySteps = form.task_steps.filter(step => step.trim())
    if (nonEmptySteps.length === 0) {
      alert('Please add at least one step with content')
      return
    }

    if (!form.tools_required.trim()) {
      alert('Please enter required tools')
      return
    }

    if (!form.materials_required.trim()) {
      alert('Please enter required materials')
      return
    }

    const payload = {
      title: form.title,
      task_steps: nonEmptySteps.join('\n'),
      tools_required: form.tools_required,
      materials_required: form.materials_required,
      status: form.status,
      step_description: form.step_description
    }

    await axios.post(`${BASE_URL}/work_instructions/`, payload)
    showCreateWorkinstructionPopup.value = false
    resetForm()
    fetchWorkInstructions()
  } catch (error) {
    console.error('Error creating work instruction:', error)
    alert('Failed to create work instruction. Please check all fields.')
  }
}

// Update a work instruction
const updateWorkInstruction = async () => {
  if (!currentWorkInstruction.value) return

  try {
    // Validate required fields
    if (!currentWorkInstruction.value.title.trim()) {
      alert('Please enter a title')
      return
    }

    if (!currentWorkInstruction.value.step_description.trim()) {
      alert('Please enter an overall description')
      return
    }

    // Filter out empty steps
    const nonEmptySteps = currentWorkInstruction.value.task_steps_array.filter(step => step.trim())
    if (nonEmptySteps.length === 0) {
      alert('Please add at least one step with content')
      return
    }

    if (!currentWorkInstruction.value.tools_required.trim()) {
      alert('Please enter required tools')
      return
    }

    if (!currentWorkInstruction.value.materials_required.trim()) {
      alert('Please enter required materials')
      return
    }

    const payload = {
      title: currentWorkInstruction.value.title,
      task_steps: nonEmptySteps.join('\n'),
      tools_required: currentWorkInstruction.value.tools_required,
      materials_required: currentWorkInstruction.value.materials_required,
      status: currentWorkInstruction.value.status,
      step_description: currentWorkInstruction.value.step_description
    }

    await axios.put(`${BASE_URL}/work_instructions/${currentWorkInstruction.value.id}/`, payload)
    showEditWorkinstructionPopup.value = false
    fetchWorkInstructions()
  } catch (error) {
    console.error('Error updating work instruction:', error)
    alert('Failed to update work instruction. Please check all fields.')
  }
}

// Delete a work instruction
const deleteWorkInstruction = async (id: number) => {
  if (!confirm('Are you sure you want to delete this work instruction?')) return

  try {
    await axios.delete(`${BASE_URL}/work_instructions/${id}/`)
    fetchWorkInstructions()
  } catch (error) {
    console.error('Error deleting work instruction:', error)
  }
}

// Add a new step
const addStep = () => {
  if (showEditWorkinstructionPopup.value && currentWorkInstruction.value) {
    currentWorkInstruction.value.task_steps_array.push('')
  } else {
    form.task_steps.push('')
  }
}

// Remove a step
const removeStep = (index: number) => {
  if (showEditWorkinstructionPopup.value && currentWorkInstruction.value) {
    if (currentWorkInstruction.value.task_steps_array.length > 1) {
      currentWorkInstruction.value.task_steps_array.splice(index, 1)
    } else {
      alert('You must have at least one step')
    }
  } else {
    if (form.task_steps.length > 1) {
      form.task_steps.splice(index, 1)
    } else {
      alert('You must have at least one step')
    }
  }
}

// Reset form
const resetForm = () => {
  form.title = ''
  form.task_steps = ['']
  form.tools_required = ''
  form.materials_required = ''
  form.status = 'Not Started'
  form.step_description = ''
}

// Format date
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}

// Status class
const statusClass = (status: string) => {
  switch (status) {
    case 'Completed':
      return 'bg-green-100 text-green-700'
    case 'In Progress':
      return 'bg-blue-100 text-blue-700'
    case 'Not Started':
      return 'bg-gray-200 text-gray-600'
    default:
      return 'bg-gray-200 text-gray-600'
  }
}

// Initialize
onMounted(() => {
  fetchWorkInstructions()
})
</script>

<style>
button {
  cursor: pointer;
}
</style>