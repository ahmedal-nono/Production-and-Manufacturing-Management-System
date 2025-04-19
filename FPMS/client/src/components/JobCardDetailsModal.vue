<template>
    <Popup :visible="visible" @update:visible="$emit('close')">
      <div class="w-full max-w-2xl p-6">
        <div class="mb-6 flex items-center justify-between">
          <h2 class="text-xl font-bold">Job Card Details - JC-{{ jobCard.id }}</h2>
          <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
  
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
          <!-- Left Column -->
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Task Name</label>
              <p class="mt-1 text-sm">{{ jobCard.task_name }}</p>
            </div>
  
            <div>
              <label class="block text-sm font-medium text-gray-700">Work Order</label>
              <p class="mt-1 text-sm">WO-{{ jobCard.work_order }}</p>
            </div>
  
            <div>
              <label class="block text-sm font-medium text-gray-700">Status</label>
              <span 
                class="mt-1 inline-block rounded-full px-3 py-1 text-xs font-medium"
                :class="getStatusClass(jobCard.status)"
              >
                {{ jobCard.status }}
              </span>
            </div>
  
            <div>
              <label class="block text-sm font-medium text-gray-700">Priority</label>
              <p class="mt-1 flex items-center gap-2 text-sm">
                <span
                  :class="{
                    'h-3 w-3 rounded-full bg-red-500': jobCard.priority === 'High',
                    'h-3 w-3 rounded-full bg-yellow-500': jobCard.priority === 'Medium',
                    'h-3 w-3 rounded-full bg-green-500': jobCard.priority === 'Low',
                  }"
                ></span>
                {{ jobCard.priority }}
              </p>
            </div>
          </div>
  
          <!-- Right Column -->
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Assigned To</label>
              <p class="mt-1 text-sm">{{ getEmployeeName(jobCard.assigned_to) }}</p>
            </div>
  
            <div>
              <label class="block text-sm font-medium text-gray-700">Required Tools</label>
              <p class="mt-1 text-sm">{{ jobCard.required_tools }}</p>
            </div>
  
            <div>
              <label class="block text-sm font-medium text-gray-700">Required Materials</label>
              <p class="mt-1 text-sm">{{ jobCard.required_materials }}</p>
            </div>
  
            <div>
              <label class="block text-sm font-medium text-gray-700">Created At</label>
              <p class="mt-1 text-sm">{{ formatDate(jobCard.created_at) }}</p>
            </div>
          </div>
        </div>
  
        <div class="mt-6 flex justify-end">
          <button
            @click="$emit('close')"
            class="rounded bg-gray-500 px-4 py-2 text-white hover:bg-gray-600"
          >
            Close
          </button>
        </div>
      </div>
    </Popup>
  </template>
  
  <script setup lang="ts">
  import { defineProps } from 'vue'
  import Popup from '@/components/popup.vue'
  
  const props = defineProps({
    jobCard: {
      type: Object,
      required: true
    },
    visible: {
      type: Boolean,
      default: false
    }
  })
  
  const emit = defineEmits(['close'])
  
  // You might want to move these to a shared utility file
  const getStatusClass = (status: string) => {
    switch (status) {
      case 'Not Started': return 'bg-gray-200 text-gray-800'
      case 'In Progress': return 'bg-blue-200 text-blue-800'
      case 'Completed': return 'bg-green-200 text-green-800'
      case 'On Hold': return 'bg-yellow-200 text-yellow-800'
      case 'Cancelled': return 'bg-red-200 text-red-800'
      default: return 'bg-gray-200 text-gray-800'
    }
  }
  
  const getEmployeeName = (employeeId: number) => {
    // This would ideally come from a store or props
    return `Employee ${employeeId}` // Replace with actual employee name lookup
  }
  
  const formatDate = (dateString: string) => {
    if (!dateString) return 'N/A'
    return new Date(dateString).toLocaleString()
  }
  </script>