<template>
  <Popup
    :visible="showJobCardsPopup"
    @update:visible="(value: boolean) => emitEvent('update:showJobCardsPopup', value)"
  >
    <div class="p-6">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <h1 class="text-2xl font-bold">Job Cards</h1>
        <span class="flex items-center gap-1 text-sm text-gray-600">
          <span class="h-2 w-2 rounded-full bg-green-500"></span> Synced 2 min ago
        </span>
      </div>

      <!-- Search and Filters -->
      <div class="mb-6 flex flex-wrap gap-4">
        <input
          v-model="filters.search"
          type="text"
          placeholder="Search job cards..."
          class="w-full max-w-md rounded border px-3 py-2 text-sm"
        />

        <select v-model="filters.status" class="rounded border px-3 py-2 text-sm">
          <option>All Statuses</option>
          <option>In Progress</option>
          <option>Completed</option>
          <option>Pending</option>
        </select>

        <select v-model="filters.priority" class="rounded border px-3 py-2 text-sm">
          <option>All Priorities</option>
          <option>High</option>
          <option>Low</option>
        </select>

        <select v-model="filters.line" class="rounded border px-3 py-2 text-sm">
          <option>All Production Lines</option>
          <option>Line A</option>
          <option>Line B</option>
        </select>

        <input v-model="filters.fromDate" type="date" class="rounded border px-3 py-2 text-sm" />
        <input v-model="filters.toDate" type="date" class="rounded border px-3 py-2 text-sm" />
      </div>

      <!-- Job Card -->
      <div
        class="w-full max-w-sm rounded-lg border bg-white p-4 shadow-sm"
        v-for="card in filteredJobCards"
        :key="card.id"
      >
        <div class="mb-2 flex items-center justify-between">
          <h2 class="font-semibold">JC-{{ card.id }}</h2>
          <span class="rounded-full bg-yellow-400 px-3 py-1 text-xs font-medium">
            {{ card.status }}
          </span>
        </div>

        <div class="mb-3 space-y-1 text-sm">
          <p><strong>Task:</strong> {{ card.task }}</p>
          <p><strong>Assigned To:</strong> {{ card.assignedTo }}</p>
          <p><strong>Due Date:</strong> {{ card.dueDate }}</p>
          <p class="flex items-center gap-2">
            <strong>Priority:</strong>
            <span
              :class="{
                'h-3 w-3 rounded-full bg-red-500': card.priority === 'High',
                'h-3 w-3 rounded-full bg-green-500': card.priority === 'Low',
              }"
            ></span>
          </p>
        </div>

        <div class="flex gap-2">
          <button class="rounded bg-blue-600 px-3 py-1 text-sm text-white hover:bg-blue-500">
            View Details
          </button>
          <button class="rounded bg-green-600 px-3 py-1 text-sm text-white hover:bg-green-500">
            Update Status
          </button>
        </div>
      </div>
    </div>
  </Popup>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Popup from '@/components/popup.vue'

defineProps<{
  showJobCardsPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showJobCardsPopup'])

const filters = ref({
  search: '',
  status: 'All Statuses',
  priority: 'All Priorities',
  line: 'All Production Lines',
  fromDate: '',
  toDate: '',
})

const jobCards = ref([
  {
    id: '1023',
    task: 'Weld Door Panel',
    assignedTo: 'John Doe',
    dueDate: '2023-08-15 14:00',
    priority: 'High',
    status: 'In Progress',
    line: 'Line A',
  },
])

const filteredJobCards = computed(() => {
  return jobCards.value.filter((card) => {
    const matchSearch =
      filters.value.search === '' ||
      card.task.toLowerCase().includes(filters.value.search.toLowerCase()) ||
      card.assignedTo.toLowerCase().includes(filters.value.search.toLowerCase())

    const matchStatus =
      filters.value.status === 'All Statuses' || card.status === filters.value.status

    const matchPriority =
      filters.value.priority === 'All Priorities' || card.priority === filters.value.priority

    const matchLine =
      filters.value.line === 'All Production Lines' || card.line === filters.value.line

    const matchDate =
      (!filters.value.fromDate || new Date(card.dueDate) >= new Date(filters.value.fromDate)) &&
      (!filters.value.toDate || new Date(card.dueDate) <= new Date(filters.value.toDate))

    return matchSearch && matchStatus && matchPriority && matchLine && matchDate
  })
})
</script>
