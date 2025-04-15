<template>
  <div>
    <Popup
      :visible="showProductionOrdersPopup"
      @update:visible="(value: boolean) => emitEvent('update:showProductionOrdersPopup', value)"
    >
      <div class="p-4">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="rounded-t px-4 py-2 text-xl font-semibold">Production Order Management</h2>
          <button
            @click="showCreateProductionOrdersPopup = true"
            class="cursor-pointer rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            Create New Production Order
          </button>
        </div>

        <div class="">
          <h3 class="p-4 text-lg font-medium">Existing Production Orders</h3>
          <table class="w-full text-center">
            <thead>
              <tr class="bg-blue-500 text-white">
                <th class="border border-gray-700 px-4 py-2">Order ID</th>
                <th class="border border-gray-700 px-4 py-2">Product name</th>
                <th class="border border-gray-700 px-4 py-2">Quantity</th>
                <th class="border border-gray-700 px-4 py-2">Due Date</th>
                <th class="border border-gray-700 px-4 py-2">Status</th>
                <th class="border border-gray-700 px-4 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id" class="border border-gray-700 px-4 py-2">
                <td class="border border-gray-700 px-4 py-2">{{ order.id }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ order.product }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ order.quantity }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ order.dueDate }}</td>
                <td class="border border-gray-700 px-4 py-2">
                  <span
                    :class="getStatusClass(order.status)"
                    class="rounded px-2 py-1 text-sm font-medium"
                  >
                    {{ order.status }}
                  </span>
                </td>
                <td class="space-x-2 px-4 py-2">
                  <button
                    @click="showEditProductionOrdersPopup = true"
                    class="cursor-pointer rounded bg-gray-200 px-3 py-1 hover:bg-gray-300"
                  >
                    Edit
                  </button>
                  <button
                    @click="showViewProductionOrdersPopup = true"
                    class="cursor-pointer rounded bg-gray-200 px-3 py-1 hover:bg-gray-300"
                  >
                    View
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </Popup>

    <Popup
      :visible="showCreateProductionOrdersPopup"
      @update:visible="showCreateProductionOrdersPopup = $event"
    >
      <div>
        <h1 class="mb-6 text-2xl font-semibold">Create Production Order</h1>

        <!-- Order Details -->

        <div class="ml-4 flex flex-row gap-4">
          <div class="flex w-full flex-col">
            <h2 class="mb-4 text-lg font-medium">Order Details</h2>
            <input
              v-model="orderName"
              type="text"
              placeholder="Order Name"
              class="rounded border p-2"
            />
          </div>
          <div class="flex w-full flex-col">
            <h2 class="mb-4 text-lg font-medium">Priority</h2>
            <select v-model="priority" class="rounded border p-2">
              <option>Normal</option>
              <option>High</option>
              <option>Low</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-2"></div>
        <section class="mb-6 rounded p-4">
          <h2 class="mb-4 text-lg font-semibold">Product Selection</h2>
          <input
            v-model="searchProduct"
            type="text"
            placeholder="Search products..."
            class="mb-4 w-full rounded border p-2"
          />
          <div class="flex flex-col items-center gap-4 md:flex-row">
            <select v-model="selectedVariant" class="flex-1 rounded border p-2">
              <option>Blue - Medium</option>
              <option>Red - Large</option>
              <option>Green - Small</option>
            </select>
            <div class="flex items-center gap-2">
              <button @click="decreaseQty" class="rounded border px-3 py-1">-</button>
              <input v-model="quantity" type="number" class="w-16 rounded border p-1 text-center" />
              <button @click="increaseQty" class="rounded border px-3 py-1">+</button>
            </div>
          </div>
        </section>

        <section class="mb-6 rounded p-4">
          <h2 class="mb-4 text-lg font-semibold">Production Parameters</h2>
          <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
            <input v-model="startDate" type="date" class="rounded border p-2" />
            <input v-model="deadline" type="date" class="rounded border p-2" />
            <select v-model="productionLine" class="rounded border p-2">
              <option>Line 1</option>
              <option>Line 2</option>
              <option>Line 3</option>
            </select>
          </div>
        </section>

        <div class="flex justify-end gap-4">
          <button @click="submitOrder" class="rounded bg-blue-600 px-4 py-2 text-white">
            Create Production Order
          </button>
        </div>
      </div>
    </Popup>
    <Popup
      :visible="showEditProductionOrdersPopup"
      @update:visible="showEditProductionOrdersPopup = $event"
    >
      <div>
        <h1 class="mb-6 text-2xl font-semibold">Edit Production Order</h1>

        <!-- Order Details -->

        <div class="ml-4 flex flex-row gap-4">
          <div class="flex w-full flex-col">
            <h2 class="mb-4 text-lg font-medium">Order Details</h2>
            <input
              v-model="orderName"
              type="text"
              placeholder="Order Name"
              class="rounded border p-2"
            />
          </div>
          <div class="flex w-full flex-col">
            <h2 class="mb-4 text-lg font-medium">Priority</h2>
            <select v-model="priority" class="rounded border p-2">
              <option>Normal</option>
              <option>High</option>
              <option>Low</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-2"></div>
        <section class="mb-6 rounded p-4">
          <h2 class="mb-4 text-lg font-semibold">Product Selection</h2>
          <input
            v-model="searchProduct"
            type="text"
            placeholder="Search products..."
            class="mb-4 w-full rounded border p-2"
          />
          <div class="flex flex-col items-center gap-4 md:flex-row">
            <select v-model="selectedVariant" class="flex-1 rounded border p-2">
              <option>Blue - Medium</option>
              <option>Red - Large</option>
              <option>Green - Small</option>
            </select>
            <div class="flex items-center gap-2">
              <button @click="decreaseQty" class="rounded border px-3 py-1">-</button>
              <input v-model="quantity" type="number" class="w-16 rounded border p-1 text-center" />
              <button @click="increaseQty" class="rounded border px-3 py-1">+</button>
            </div>
          </div>
        </section>

        <section class="mb-6 rounded p-4">
          <h2 class="mb-4 text-lg font-semibold">Production Parameters</h2>
          <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
            <input v-model="startDate" type="date" class="rounded border p-2" />
            <input v-model="deadline" type="date" class="rounded border p-2" />
            <select v-model="productionLine" class="rounded border p-2">
              <option>Line 1</option>
              <option>Line 2</option>
              <option>Line 3</option>
            </select>
          </div>
        </section>

        <div class="flex justify-end gap-4">
          <button @click="submitOrder" class="rounded bg-blue-600 px-4 py-2 text-white">
            Create Production Order
          </button>
        </div>
      </div>
    </Popup>
    <Popup
      :visible="showViewProductionOrdersPopup"
      @update:visible="showViewProductionOrdersPopup = $event"
    >
      <div>
        <h1 class="mb-6 text-2xl font-semibold">Production Order</h1>

        <!-- Order Details -->

        <div class="ml-4 flex flex-row gap-4">
          <div class="flex w-full flex-col">
            <h2 class="mb-4 text-lg font-medium">Order Details</h2>
            <input
              v-model="orderName"
              type="text"
              placeholder="Order Name"
              class="rounded border p-2"
            />
          </div>
          <div class="flex w-full flex-col">
            <h2 class="mb-4 text-lg font-medium">Priority</h2>
            <select v-model="priority" class="rounded border p-2">
              <option>Normal</option>
              <option>High</option>
              <option>Low</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-2"></div>
        <section class="mb-6 rounded p-4">
          <h2 class="mb-4 text-lg font-semibold">Product Selection</h2>
          <input
            v-model="searchProduct"
            type="text"
            placeholder="Search products..."
            class="mb-4 w-full rounded border p-2"
          />
          <div class="flex flex-col items-center gap-4 md:flex-row">
            <select v-model="selectedVariant" class="flex-1 rounded border p-2">
              <option>Blue - Medium</option>
              <option>Red - Large</option>
              <option>Green - Small</option>
            </select>
            <div class="flex items-center gap-2">
              <button @click="decreaseQty" class="rounded border px-3 py-1">-</button>
              <input v-model="quantity" type="number" class="w-16 rounded border p-1 text-center" />
              <button @click="increaseQty" class="rounded border px-3 py-1">+</button>
            </div>
          </div>
        </section>

        <section class="mb-6 rounded p-4">
          <h2 class="mb-4 text-lg font-semibold">Production Parameters</h2>
          <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
            <input v-model="startDate" type="date" class="rounded border p-2" />
            <input v-model="deadline" type="date" class="rounded border p-2" />
            <select v-model="productionLine" class="rounded border p-2">
              <option>Line 1</option>
              <option>Line 2</option>
              <option>Line 3</option>
            </select>
          </div>
        </section>

        <div class="flex justify-end gap-4">
          <button @click="submitOrder" class="rounded bg-blue-600 px-4 py-2 text-white">
            Create Production Order
          </button>
        </div>
      </div>
    </Popup>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import Popup from '@/components/popup.vue'

const showCreateProductionOrdersPopup = ref(false)
const showEditProductionOrdersPopup = ref(false)
const showViewProductionOrdersPopup = ref(false)

const props = defineProps<{
  showProductionOrdersPopup: boolean
}>()

interface Order {
  id: string
  product: string
  quantity: number
  status: 'On Track' | 'Delayed'
  startDate: string
  endDate: string
  productionLine: string
  priority: 'High' | 'Low'
  dueDate: string
}

const orders = ref<Order[]>([
  {
    id: '#1234',
    product: 'Product A',
    quantity: 500,
    status: 'On Track',
    startDate: '2024-03-15',
    endDate: '2024-03-20',
    productionLine: 'Line 1',
    priority: 'High',
    dueDate: '2024-03-20',
  },
  {
    id: '#1235',
    product: 'Product B',
    quantity: 1000,
    status: 'Delayed',
    startDate: '2024-03-18',
    endDate: '2024-03-22',
    productionLine: 'Line 2',
    priority: 'Low',
    dueDate: '2024-03-22',
  },
])

const getStatusClass = (status: string) => {
  return status === 'On Track' ? 'bg-green-200 text-green-700' : 'bg-red-200 text-red-700'
}

const emitEvent = defineEmits(['close', 'submit', 'update:showProductionOrdersPopup'])

const orderName = ref('')
const priority = ref('Normal')
const searchProduct = ref('')
const selectedVariant = ref('Blue - Medium')
const quantity = ref(1)
const startDate = ref('')
const deadline = ref('')
const productionLine = ref('Line 1')

const increaseQty = () => {
  quantity.value++
}

const decreaseQty = () => {
  if (quantity.value > 1) quantity.value--
}

const submitOrder = () => {
  const payload = {
    orderName: orderName.value,
    priority: priority.value,
    selectedVariant: selectedVariant.value,
    quantity: quantity.value,
    startDate: startDate.value,
    deadline: deadline.value,
    productionLine: productionLine.value,
  }
}
</script>

<style>
button {
  cursor: pointer;
}
</style>
