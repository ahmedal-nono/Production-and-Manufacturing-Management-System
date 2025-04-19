<template>
  <Popup
    :visible="showReportedIssuesPopup"
    @update:visible="(value: boolean) => emitEvent('update:showReportedIssuesPopup', value)"
  >
    <div class="">
      <!-- Header -->
      <div class="mb-4 flex items-center justify-between">
        <h2 class="text-2xl font-bold">Reports</h2>
        <button
          @click="showNewIssuePopup = true"
          class="m-2 mt-4 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
        >
          New Issue
        </button>
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

      <!-- Issues Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr>
              <th class="border border-gray-700 px-4 py-2">Issue ID</th>
              <th class="border border-gray-700 px-4 py-2">Category</th>
              <th class="border border-gray-700 px-4 py-2">Priority</th>
              <th class="border border-gray-700 px-4 py-2">Affected Workflow/Job card</th>
              <th class="border border-gray-700 px-4 py-2">Time Stamp</th>
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
              <td class="border border-gray-700 px-4 py-2">{{ item.category }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ item.priority }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ item.affected_item }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ item.created_at }}</td>
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
                  @click="openEditIssuePopup(item)"
                  class="rounded bg-yellow-500 px-2 py-1 text-white hover:bg-yellow-600"
                >
                  Edit
                </button>
                <button
                  @click="deleteIssue(item.id)"
                  class="rounded bg-red-600 px-2 py-1 text-white hover:bg-red-700"
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

  <!-- New/Edit Issue Popup -->
  <Popup :visible="showNewIssuePopup" @update:visible="showNewIssuePopup = $event">
    <div class="">
      <h2 class="mb-4 text-xl font-semibold">
        {{ editingIssueId ? 'Edit Issue' : 'Submit an Issue' }}
      </h2>

      <form @submit.prevent="submitIssue" class="space-y-4">
        <!-- Issue Category -->
        <div>
          <label class="mb-1 block font-medium">Issue Category</label>
          <select
            v-model="form.category"
            class="w-full rounded border px-3 py-2 focus:outline-none"
          >
            <option value="">Select Category</option>
            <option value="Production">Production</option>
            <option value="Quality">Quality</option>
            <option value="Maintenance">Maintenance</option>
          </select>
        </div>

        <!-- Affected Workflow -->
        <div>
          <label class="mb-1 block font-medium">Affected Workflow/Workorder/JobCard</label>
          <input
            type="text"
            v-model="form.workflow"
            placeholder="Search workflows/job cards..."
            class="w-full rounded border px-3 py-2 focus:outline-none"
          />
        </div>

        <!-- Urgency -->
        <div>
          <label class="mb-1 block font-medium">Urgency/Priority</label>
          <div class="flex gap-6">
            <label
              v-for="priority in ['Low', 'Medium', 'High', 'Critical']"
              :key="priority"
              class="flex items-center gap-1"
            >
              <input type="radio" v-model="form.priority" :value="priority" />
              {{ priority }}
            </label>
          </div>
        </div>

        <!-- Description -->
        <div>
          <label class="mb-1 block font-medium">Description</label>
          <div class="rounded border">
            <textarea
              v-model="form.description"
              rows="5"
              class="w-full resize-none px-3 py-2 focus:outline-none"
              placeholder="Enter issue description..."
            ></textarea>
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-4 flex justify-end gap-2">
          <button type="submit" class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
            {{ editingIssueId ? 'Update Issue' : 'Submit Issue' }}
          </button>
        </div>
      </form>
    </div>
  </Popup>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Popup from '@/components/popup.vue'
import { useAxios } from '@vueuse/integrations/useAxios'

const API_BASE_URL = 'http://localhost:8000/api/'

// Interfaces
interface Issue {
  id: number
  category: string
  affected_item: string
  priority: string
  description: string
  created_at: string
  status?: string
}

// State
const showNewIssuePopup = ref(false)
const instructions = ref<Issue[]>([])
const isLoading = ref(false)
const error = ref<string | null>(null)
const editingIssueId = ref<number | null>(null)

// Props and Emits
defineProps<{ showReportedIssuesPopup: boolean }>()
const emitEvent = defineEmits(['close', 'submit', 'update:showReportedIssuesPopup'])

// Form Data
const form = ref({
  category: '',
  workflow: '',
  priority: '',
  description: '',
})

// Fetch Issues
const fetchIssues = async () => {
  try {
    isLoading.value = true
    const { data } = await useAxios<Issue[]>(`${API_BASE_URL}issues/`, { method: 'GET' })
    if (data.value) {
      instructions.value = data.value
        .map((issue) => ({
          ...issue,
          status: 'Active', // Default status
        }))
        .sort((a, b) => a.id - b.id) // Sort in ascending order by id
    }
  } catch (err) {
    error.value = 'Failed to fetch issues'
    console.error('Error fetching issues:', err)
  } finally {
    isLoading.value = false
  }
}

// Submit New or Update Issue
const submitIssue = async () => {
  try {
    const payload = {
      category: form.value.category,
      affected_item: form.value.workflow,
      priority: form.value.priority.toLowerCase(),
      description: form.value.description,
    }

    if (editingIssueId.value) {
      // Update Issue
      await useAxios(`${API_BASE_URL}issues/${editingIssueId.value}/`, {
        method: 'PUT',
        data: payload,
      })
    } else {
      // Create New Issue
      const { data } = await useAxios<Issue>(`${API_BASE_URL}issues/`, {
        method: 'POST',
        data: payload,
      })
      if (data.value) {
        instructions.value = [
          {
            ...data.value,
            status: 'Active',
          },
          ...instructions.value,
        ]
      }
    }

    resetForm()
    showNewIssuePopup.value = false
  } catch (err) {
    error.value = 'Failed to submit issue'
    console.error('Error submitting issue:', err)
  }
}

// Delete Issue
const deleteIssue = async (id: number) => {
  if (!confirm('Are you sure you want to delete this issue?')) return

  try {
    await useAxios(`${API_BASE_URL}issues/${id}/`, { method: 'DELETE' })
    instructions.value = instructions.value.filter((issue) => issue.id !== id)
  } catch (err) {
    error.value = 'Failed to delete issue'
    console.error('Error deleting issue:', err)
  }
}

// Open Edit Issue Popup
const openEditIssuePopup = (issue: Issue) => {
  form.value = {
    category: issue.category,
    workflow: issue.affected_item,
    priority: issue.priority,
    description: issue.description,
  }
  editingIssueId.value = issue.id
  showNewIssuePopup.value = true
}

// Reset Form
const resetForm = () => {
  form.value = {
    category: '',
    workflow: '',
    priority: '',
    description: '',
  }
  editingIssueId.value = null
}

// On Component Mount
onMounted(async () => {
  await fetchIssues()
})
</script>

<style>
button {
  cursor: pointer;
}
</style>
