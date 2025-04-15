<template>
  <div>
    <Popup
      :visible="showWorkordersPopup"
      @update:visible="(value: boolean) => emitEvent('update:showWorkordersPopup', value)"
    >
      <div class="w-full max-w-6xl p-6">
        <!-- Header -->
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-2xl font-bold">Work Order Management</h2>
          <button
            @click="showCreateWorkOrderPopup = true"
            class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            + Create Work Order
          </button>
        </div>

        <!-- Filters -->
        <div class="mb-4 flex flex-wrap items-center gap-4">
          <input
            v-model="filters.search"
            type="text"
            placeholder="Search..."
            class="w-48 rounded border px-2 py-1"
          />
          <select v-model="filters.status" class="rounded border px-2 py-1">
            <option>All Statuses</option>
            <option>Active</option>
            <option>Completed</option>
            <option>Pending</option>
            <option>Inactive</option>
          </select>
          <select v-model="filters.priority" class="rounded border px-2 py-1">
            <option>All Priorities</option>
            <option>High</option>
            <option>Low</option>
          </select>
          <input v-model="filters.date" type="date" class="rounded border px-2 py-1" />
        </div>

        <!-- Table -->
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr class="">
              <th class="border border-gray-700 px-4 py-2">Work Order ID</th>
              <th class="border border-gray-700 px-4 py-2">Product</th>
              <th class="border border-gray-700 px-4 py-2">Quantity</th>
              <th class="border border-gray-700 px-4 py-2">Due Time</th>
              <th class="border border-gray-700 px-4 py-2">Priority</th>
              <th class="border border-gray-700 px-4 py-2">Status</th>
              <th class="border border-gray-700 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(order, index) in filteredOrders"
              :key="index"
              class="border-t bg-white hover:bg-gray-50"
            >
              <td class="border border-gray-700 px-4 py-2">{{ order.id }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ order.product }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ order.quantity }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ order.due }}</td>
              <td class="border border-gray-700 px-4 py-2">
                <span :class="getPriorityClass(order.priority)"> ● {{ order.priority }} </span>
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <span
                  :class="getStatusClass(order.status)"
                  class="rounded-full bg-green-100 px-2 py-1 text-xs text-green-700"
                  >{{ order.status }}</span
                >
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <button
                  @click="showViewWorkOrderPopup = true"
                  class="m-1 rounded bg-gray-200 px-2 py-1 text-sm hover:bg-gray-300"
                >
                  View
                </button>
                <button
                  @click="showEditWorkOrderPopup = true"
                  class="m-1 rounded bg-gray-200 px-2 py-1 text-sm hover:bg-gray-300"
                >
                  Edit
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Popup>

    <Popup :visible="showCreateWorkOrderPopup" @update:visible="showCreateWorkOrderPopup = $event">
      <div class="p-6">
        <div class="mb-6 flex flex-row justify-center">
          <h2 class="w-full text-center text-2xl font-bold">Create New Work Order</h2>
        </div>

        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <!-- Left Section -->
          <div class="space-y-4 md:col-span-2">
            <div>
              <label class="font-semibold">Workorder Name </label>
              <input
                v-model="form.workorderName"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="text"
              />
            </div>

            <div>
              <label class="font-semibold">Select Work Instruction</label>
              <select
                v-model="form.workInstruction"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option disabled value="">Select Work Instruction</option>
                <option>Weld & Inspect</option>
                <option>Electrical Assembly</option>
              </select>
            </div>

            <div>
              <label class="font-semibold">Assign to Production Line</label>
              <select
                v-model="form.productionLine"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option disabled value="">Select Production Line</option>
                <option>Line A</option>
                <option>Line B</option>
              </select>
            </div>

            <div>
              <label class="font-semibold">Quantity</label>
              <input
                v-model="form.quantity"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="number"
              />
            </div>

            <div>
              <label class="font-semibold">Due Time</label>
              <input
                v-model="form.dueTime"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="time"
              />
            </div>

            <div>
              <label class="font-semibold">Additional Notes</label>
              <textarea
                v-model="form.notes"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                rows="3"
              />
            </div>

            <div class="flex gap-3">
              <button class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
                Create Work Order
              </button>
            </div>
          </div>

          <!-- Right Section -->
          <div class="h-full w-full rounded border bg-white p-4 text-xl">
            <h3 class="mb-2 font-semibold">Work Instruction Preview</h3>
            <p class="">Steps</p>
            <ul class="mb-4 list-decimal pl-5 text-sm text-gray-700">
              <li>
                <input
                  class="m-1 w-full rounded border border-gray-300 px-2 py-1"
                  type="text"
                  name=""
                  id=""
                />
              </li>
              <li>
                <input
                  class="m-1 w-full rounded border border-gray-300 px-2 py-1"
                  type="text"
                  name=""
                  id=""
                />
              </li>
              <li>
                <input
                  class="m-1 w-full rounded border border-gray-300 px-2 py-1"
                  type="text"
                  name=""
                  id=""
                />
              </li>
            </ul>

            <p class="mb-1 font-medium">Attachments</p>
            <div class="mb-4 flex gap-2">
              <button class="rounded bg-gray-100 px-3 py-1 text-sm">PDF Icon</button>
              <button class="rounded bg-gray-100 px-3 py-1 text-sm">Video Icon</button>
            </div>

            <p class="font-medium">Linked BOM</p>
            <ul class="list-disc pl-5 text-sm">
              <li>Steel Sheets (20)</li>
              <li>Electrical Components (45)</li>
            </ul>
          </div>
        </div>
      </div>
    </Popup>
    <Popup :visible="showEditWorkOrderPopup" @update:visible="showEditWorkOrderPopup = $event">
      <div class="p-6">
        <div class="mb-6 flex flex-row justify-center">
          <h2 class="w-full text-center text-2xl font-bold">Edit Work Order</h2>
        </div>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <!-- Left Section -->
          <div class="space-y-4 md:col-span-2">
            <div>
              <label class="font-semibold">Workorder Name </label>
              <input
                v-model="form.workorderName"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="text"
              />
            </div>

            <div>
              <label class="font-semibold">Select Work Instruction</label>
              <select
                v-model="form.workInstruction"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option disabled value="">Select Work Instruction</option>
                <option>Weld & Inspect</option>
                <option>Electrical Assembly</option>
              </select>
            </div>

            <div>
              <label class="font-semibold">Assign to Production Line</label>
              <select
                v-model="form.productionLine"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option disabled value="">Select Production Line</option>
                <option>Line A</option>
                <option>Line B</option>
              </select>
            </div>

            <div>
              <label class="font-semibold">Quantity</label>
              <input
                v-model="form.quantity"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="number"
              />
            </div>

            <div>
              <label class="font-semibold">Due Time</label>
              <input
                v-model="form.dueTime"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="time"
              />
            </div>

            <div>
              <label class="font-semibold">Additional Notes</label>
              <textarea
                v-model="form.notes"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                rows="3"
              />
            </div>

            <div class="flex gap-3">
              <button class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
                Create Work Order
              </button>
            </div>
          </div>

          <!-- Right Section -->
          <div class="h-full w-full rounded border bg-white p-4 text-xl">
            <h3 class="mb-2 font-semibold">Work Instruction Preview</h3>
            <p class="">Steps</p>
            <ul class="mb-4 list-decimal pl-5 text-sm text-gray-700">
              <li>
                <input
                  class="m-1 w-full rounded border border-gray-300 px-2 py-1"
                  type="text"
                  name=""
                  id=""
                />
              </li>
              <li>
                <input
                  class="m-1 w-full rounded border border-gray-300 px-2 py-1"
                  type="text"
                  name=""
                  id=""
                />
              </li>
              <li>
                <input
                  class="m-1 w-full rounded border border-gray-300 px-2 py-1"
                  type="text"
                  name=""
                  id=""
                />
              </li>
            </ul>

            <p class="mb-1 font-medium">Attachments</p>
            <div class="mb-4 flex gap-2">
              <button class="rounded bg-gray-100 px-3 py-1 text-sm">PDF Icon</button>
              <button class="rounded bg-gray-100 px-3 py-1 text-sm">Video Icon</button>
            </div>

            <p class="font-medium">Linked BOM</p>
            <ul class="list-disc pl-5 text-sm">
              <li>Steel Sheets (20)</li>
              <li>Electrical Components (45)</li>
            </ul>
          </div>
        </div>
      </div>
    </Popup>
    <Popup :visible="showViewWorkOrderPopup" @update:visible="showViewWorkOrderPopup = $event">
      <div class="p-6">
        <div class="mb-6 flex flex-row justify-center">
          <h2 class="w-full text-center text-2xl font-bold">View Work Order</h2>
        </div>

        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <!-- Left Section -->
          <div class="space-y-4 md:col-span-2">
            <div>
              <label class="font-semibold">Workorder Name </label>
              <input
                v-model="form.workorderName"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="text"
              />
            </div>

            <div>
              <label class="font-semibold">Select Work Instruction</label>
              <select
                v-model="form.workInstruction"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option disabled value="">Select Work Instruction</option>
                <option>Weld & Inspect</option>
                <option>Electrical Assembly</option>
              </select>
            </div>

            <div>
              <label class="font-semibold">Assign to Production Line</label>
              <select
                v-model="form.productionLine"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
              >
                <option disabled value="">Select Production Line</option>
                <option>Line A</option>
                <option>Line B</option>
              </select>
            </div>

            <div>
              <label class="font-semibold">Quantity</label>
              <input
                v-model="form.quantity"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="number"
              />
            </div>

            <div>
              <label class="font-semibold">Due Time</label>
              <input
                v-model="form.dueTime"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                type="time"
              />
            </div>

            <div>
              <label class="font-semibold">Additional Notes</label>
              <textarea
                v-model="form.notes"
                class="mt-1 w-full rounded border border-gray-300 px-2 py-1"
                rows="3"
              />
            </div>

            <div class="flex gap-3">
              <button class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
                Create Work Order
              </button>
            </div>
          </div>

          <!-- Right Section -->
          <div class="h-full w-full rounded border bg-white p-4 text-xl">
            <h3 class="mb-2 font-semibold">Work Instruction Preview</h3>
            <p class="">Steps</p>
            <ul class="mb-4 list-decimal pl-5 text-sm text-gray-700">
              <li>
                <input
                  class="m-1 w-full rounded border border-gray-300 px-2 py-1"
                  type="text"
                  name=""
                  id=""
                  value=""
                  readonly
                />
              </li>
              <li>
                <input
                  class="m-1 w-full rounded border border-gray-300 px-2 py-1"
                  type="text"
                  name=""
                  id=""
                  value=""
                  readonly
                />
              </li>
              <li>
                <input
                  class="m-1 w-full rounded border border-gray-300 px-2 py-1"
                  type="text"
                  name=""
                  id=""
                  value=""
                  readonly
                />
              </li>
            </ul>

            <p class="mb-1 font-medium">Attachments</p>
            <div class="mb-4 flex gap-2">
              <button class="rounded bg-gray-100 px-3 py-1 text-sm">PDF Icon</button>
              <button class="rounded bg-gray-100 px-3 py-1 text-sm">Video Icon</button>
            </div>

            <p class="font-medium">Linked BOM</p>
            <ul class="list-disc pl-5 text-sm">
              <li>Steel Sheets (20)</li>
              <li>Electrical Components (45)</li>
            </ul>
          </div>
        </div>
      </div>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import Popup from '@/components/popup.vue'

const showCreateWorkOrderPopup = ref(false)
const showEditWorkOrderPopup = ref(false)
const showViewWorkOrderPopup = ref(false)

defineProps<{
  showWorkordersPopup: boolean
}>()

const emitEvent = defineEmits([
  'close',
  'submit',
  'update:showWorkordersPopup',
  'update:showCreateWorkOrderPopup',
])

const filters = reactive({
  search: '',
  status: 'All Statuses',
  priority: 'All Priorities',
  date: '',
})

const orders = ref([
  {
    id: 'WO-1234',
    product: 'SUV Door Assembly',
    quantity: 50,
    due: '50hr',
    priority: 'High',
    status: 'Active',
  },
  {
    id: 'WO-1234',
    product: 'SUV Door Assembly',
    quantity: 50,
    due: '50hr',
    priority: 'Low',
    status: 'Inactive',
  },
])

const filteredOrders = computed(() => {
  const searchLower = filters.search.toLowerCase()
  return orders.value.filter((order) => {
    const matchesSearch =
      order.id.toLowerCase().includes(searchLower) ||
      order.product.toLowerCase().includes(searchLower)

    const matchesStatus = filters.status === 'All Statuses' || order.status === filters.status

    const matchesPriority =
      filters.priority === 'All Priorities' || order.priority === filters.priority

    return matchesSearch && matchesStatus && matchesPriority
  })
})

const getPriorityClass = (priority: string) => {
  return priority === 'High' ? 'text-red-600' : 'text-blue-600'
}

const getStatusClass = (status: string) => {
  return status === 'Active' && 'active' ? 'bg-green-200 text-green-700' : 'bg-red-200 text-red-700'
}

const form = ref({
  workorderName: '',
  workInstruction: '',
  productionLine: '',
  quantity: '',
  dueTime: '',
  notes: '',
})
</script>

<style>
button {
  cursor: pointer;
}
</style>
