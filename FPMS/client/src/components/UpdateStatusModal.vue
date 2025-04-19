<template>
  <Popup :visible="visible" @update:visible="$emit('close')">
    <div class="w-full max-w-md p-6">
      <div class="mb-6 flex items-center justify-between">
        <h2 class="text-xl font-bold">Update Status - JC-{{ jobCard.id }}</h2>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="mb-4 rounded bg-red-100 p-3 text-red-700">
        {{ errorMessage }}
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Current Task</label>
          <p class="mt-1 text-sm">{{ jobCard.task_name }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Current Status</label>
          <span
            class="mt-1 inline-block rounded-full px-3 py-1 text-xs font-medium"
            :class="getStatusClass(jobCard.status)"
          >
            {{ jobCard.status }}
          </span>
        </div>

        <div>
          <label for="status" class="block text-sm font-medium text-gray-700">New Status</label>
          <select
            id="status"
            v-model="newStatus"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          >
            <option v-for="status in statusOptions" :key="status" :value="status">
              {{ status }}
            </option>
          </select>
        </div>

        <div>
          <label for="notes" class="block text-sm font-medium text-gray-700">Notes</label>
          <textarea
            id="notes"
            v-model="notes"
            rows="3"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          ></textarea>
        </div>
      </div>

      <div class="mt-6 flex justify-end gap-3">
        <button
          @click="$emit('close')"
          class="rounded bg-gray-500 px-4 py-2 text-white hover:bg-gray-600"
          :disabled="isLoading"
        >
          Cancel
        </button>
        <button
          @click="updateStatus"
          class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          :disabled="isLoading"
        >
          <span v-if="isLoading">Updating...</span>
          <span v-else>Update Status</span>
        </button>
      </div>
    </div>
  </Popup>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import Popup from '@/components/popup.vue'

const API_BASE_URL = 'http://localhost:8000/api'

const props = defineProps({
  jobCard: {
    type: Object,
    required: true,
  },
  visible: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close', 'status-updated'])

const statusOptions = ['Not Started', 'In Progress', 'Completed']
const newStatus = ref(props.jobCard.status)
const notes = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

const getStatusClass = (status: string) => {
  switch (status) {
    case 'Not Started':
      return 'bg-gray-200 text-gray-800'
    case 'In Progress':
      return 'bg-blue-200 text-blue-800'
    case 'Completed':
      return 'bg-green-200 text-green-800'
    default:
      return 'bg-gray-200 text-gray-800'
  }
}

const updateStatus = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const payload = {
      status: newStatus.value,
      task_name: props.jobCard.task_name,
      required_tools: props.jobCard.required_tools,
      required_materials: props.jobCard.required_materials,
      assigned_to: props.jobCard.assigned_to?.id || null,
      // Send full work_order object as the backend expects
      work_order: {
        id: props.jobCard.work_order.id,
        name: props.jobCard.work_order.name,
        quantity_required: props.jobCard.work_order.quantity_required,
        due_date: props.jobCard.work_order.due_date,
        priority: props.jobCard.work_order.priority,
        work_instruction: props.jobCard.work_order.work_instruction,
        production_line: props.jobCard.work_order.production_line,
      },
    }

    const response = await axios.patch(`${API_BASE_URL}/job_cards/${props.jobCard.id}/`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    })

    emit('status-updated', response.data)
    emit('close')
  } catch (error: any) {
    console.error('Error updating job card status:', error)

    if (error.response) {
      if (error.response.data) {
        if (typeof error.response.data === 'object') {
          const errors = Object.entries(error.response.data)
            .map(
              ([field, messages]) =>
                `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`,
            )
            .join('\n')
          errorMessage.value = `Validation errors:\n${errors}`
        } else {
          errorMessage.value =
            error.response.data.detail || error.response.data.message || 'Failed to update status'
        }
      } else {
        errorMessage.value = `Server error: ${error.response.status}`
      }
    } else if (error.request) {
      errorMessage.value = 'No response from server'
    } else {
      errorMessage.value = 'Request failed to send'
    }
  } finally {
    isLoading.value = false
  }
}
</script>
