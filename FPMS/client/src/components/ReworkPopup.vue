<template>
  <Popup
    :visible="showReworkPopup"
    @update:visible="(value: boolean) => emitEvent('update:showReworkPopup', value)"
  >
    <div class="">
      <h2 class="mb-4 text-2xl font-semibold">Rework Management</h2>

      <!-- Filters -->
      <div class="mb-4 flex flex-wrap items-center gap-4 text-sm">
        <div>
          <label class="block font-medium">Status:</label>
          <select v-model="filters.status" class="rounded border p-1">
            <option>All</option>
            <option>Open</option>
            <option>Completed</option>
          </select>
        </div>

        <div>
          <label class="block font-medium">Defect Type:</label>
          <select v-model="filters.defectType" class="rounded border p-1">
            <option>All</option>
            <option>Material Defect</option>
            <option>Assembly Defect</option>
          </select>
        </div>

        <div>
          <label class="block font-medium">Date Range:</label>
          <input type="date" v-model="filters.date" class="rounded border p-1" />
        </div>

        <div class="flex-1">
          <label class="block font-medium">Work Order ID:</label>
          <input
            type="text"
            v-model="filters.workOrderId"
            placeholder="Search by Work Order ID"
            class="w-full rounded border p-1"
          />
        </div>
      </div>

      <!-- Table -->
      <table class="w-full border text-sm">
        <thead class="bg-gray-100">
          <tr>
            <th class="border p-2 text-left">Rework ID</th>
            <th class="border p-2 text-left">Work Order</th>
            <th class="border p-2 text-left">Product</th>
            <th class="border p-2 text-left">Defect Type</th>
            <th class="border p-2 text-left">Assigned To</th>
            <th class="border p-2 text-left">Due Date</th>
            <th class="border p-2 text-left">Status</th>
            <th class="border p-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(rework, index) in filteredReworks"
            :key="index"
            :class="rowClass(rework.defectLevel)"
          >
            <td class="cursor-pointer border p-2 text-blue-600 underline">{{ rework.id }}</td>
            <td class="border p-2">{{ rework.workOrder }}</td>
            <td class="border p-2">{{ rework.product }}</td>
            <td class="border p-2">
              <span
                class="rounded px-2 py-1 text-xs text-white"
                :class="badgeClass(rework.defectLevel)"
              >
                {{ rework.defectLevel }}
              </span>
            </td>
            <td class="border p-2">{{ rework.assignedTo || 'Not Assigned' }}</td>
            <td class="border p-2">
              <input type="date" v-model="rework.dueDate" class="rounded border p-1" />
            </td>
            <td class="border p-2">
              <span v-if="rework.status === 'Open'" class="font-semibold text-orange-500"
                >Open ●</span
              >
              <span v-else class="font-semibold text-green-600">Completed ✅</span>
            </td>
            <td class="space-x-2 border p-2">
              <button
                v-if="rework.status === 'Open'"
                class="rounded bg-gray-500 px-3 py-1 text-white"
                @click="assignRework(rework.id, 'John Doe')"
              >
                Assign to
              </button>
              <button v-else class="rounded bg-gray-500 px-3 py-1 text-white">Reassign</button>

              <button
                :class="
                  rework.status === 'Open'
                    ? 'bg-green-500 hover:bg-green-600'
                    : 'bg-red-500 hover:bg-red-600'
                "
                class="rounded px-3 py-1 text-white"
                @click="toggleStatus(rework)"
              >
                {{ rework.status === 'Open' ? 'Mark Complete' : 'Mark UnCompleted' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </Popup>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Popup from '@/components/popup.vue'
import { useReworkStore } from '@/stores/useRework'

const reworkStore = useReworkStore()

defineProps<{
  showReworkPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showReworkPopup'])

const filters = ref({
  status: 'All',
  defectType: 'All',
  date: '',
  workOrderId: '',
})

const reworks = computed(() => reworkStore.reworks)

const badgeClass = (level: 'Critical' | 'Major' | 'Minor') => {
  return (
    {
      Critical: 'bg-red-500',
      Major: 'bg-orange-500',
      Minor: 'bg-yellow-500 text-black',
    }[level] || 'bg-gray-300'
  )
}

const rowClass = (level: 'Critical' | 'Major' | 'Minor') => {
  return (
    {
      Critical: 'bg-red-100',
      Major: 'bg-orange-100',
      Minor: 'bg-yellow-100',
    }[level] || ''
  )
}

const toggleStatus = async (item: { id: string; status: string }) => {
  const newStatus = item.status === 'Open' ? 'Completed' : 'Open'
  await reworkStore.updateRework(item.id, { status: newStatus })
}

const assignRework = async (reworkId: string, assignedTo: string) => {
  try {
    await reworkStore.updateRework(reworkId, { assignedTo })
    console.log(`Rework ${reworkId} assigned to ${assignedTo}`)
  } catch (error) {
    console.error('Failed to assign rework:', error)
  }
}

const fetchReworks = async () => {
  try {
    await reworkStore.fetchReworks()
  } catch (error) {
    console.error('Failed to fetch reworks:', error)
  }
}

onMounted(() => {
  fetchReworks()
})

const filteredReworks = computed(() => {
  return reworks.value.filter((r) => {
    const matchStatus = filters.value.status === 'All' || r.status === filters.value.status
    const matchDefect =
      filters.value.defectType === 'All' || r.defectLevel === filters.value.defectType
    const matchWorkOrder = r.workOrder.includes(filters.value.workOrderId)
    const matchDate = !filters.value.date || r.dueDate === filters.value.date

    return matchStatus && matchDefect && matchWorkOrder && matchDate
  })
})
</script>

<style>
button {
  cursor: pointer;
}
</style>
