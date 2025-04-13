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
        <table class="w-full border text-sm">
          <thead class="">
            <tr class="text-left">
              <th class="border p-2">Work Order ID</th>
              <th class="border p-2">Product Name</th>
              <th class="border p-2">Quantity</th>
              <th class="border p-2">Due Date</th>
              <th class="border p-2">Status</th>
              <th class="border p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, index) in instructions"
              :key="index"
              class="border bg-white hover:bg-gray-50"
            >
              <td class="border p-2">{{ item.id }}</td>
              <td class="border p-2">{{ item.product }}</td>
              <td class="border p-2">{{ item.quantity }}</td>
              <td class="border p-2">{{ item.dueDate }}</td>
              <td class="border p-2">
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
              <td class="space-x-2 p-2">
                <button
                  @click="showStartInspectionPopup = true"
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
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Popup from '@/components/popup.vue'

const showStartInspectionPopup = ref(false)

const instructions = ref([
  {
    id: 'WO-1234',
    product: 'Product A',
    quantity: 100,
    dueDate: '2023-10-01',
    status: 'Active',
  },
  {
    id: 'WO-1235',
    product: 'Product B',
    quantity: 200,
    dueDate: '2023-10-02',
    status: 'Inactive',
  },
])

defineProps<{
  showQualityInspectionPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showQualityInspectionPopup'])
</script>
