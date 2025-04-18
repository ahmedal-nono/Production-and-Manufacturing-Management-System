<template>
  <div>
    <Popup
      :visible="showProductionOrdersPopup"
      @update:visible="(value: boolean) => emitEvent('update:showProductionOrdersPopup', value)"
      @update-dates="updateOrderDatesHandler"
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

        <div>
          <h3 class="p-4 text-lg font-medium">Existing Production Orders</h3>
          <table class="w-full text-center">
            <thead>
              <tr class="bg-blue-500 text-white">
                <th class="border border-gray-700 px-4 py-2">Order ID</th>
                <th class="border border-gray-700 px-4 py-2">Product Name</th>
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
                <td class="border border-gray-700 px-4 py-2">{{ order.endDate }}</td>
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
                    @click="openEditPopup(order)"
                    class="cursor-pointer rounded bg-gray-200 px-3 py-1 hover:bg-gray-300"
                  >
                    Edit
                  </button>
                  <button
                    @click="() => deleteOrder(order.id)"
                    class="cursor-pointer rounded bg-red-500 px-3 py-1 text-white hover:bg-red-600"
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

    <!-- Create Order Popup -->
    <Popup
      :visible="showCreateProductionOrdersPopup"
      @update:visible="
        (value) => {
          showCreateProductionOrdersPopup = value
          if (!value) resetCreateForm()
        }
      "
    >
      <div>
        <h1 class="mb-6 text-2xl font-semibold">Create Production Order</h1>
        <div class="space-y-6">
          <!-- Order Details -->
          <div>
            <h2 class="mb-2 text-lg font-medium">Order Details</h2>
            <div class="grid grid-cols-2 gap-4">
              <label>
                Product Name
                <input
                  v-model="orderName"
                  type="text"
                  placeholder="Order Name"
                  class="w-full rounded border p-2"
                />
              </label>
              <label>
                Priority
                <select v-model="priority" class="w-full rounded border p-2">
                  <option>High</option>
                  <option>Low</option>
                </select>
              </label>
            </div>
          </div>

          <!-- Product Selection -->
          <div>
            <h2 class="mb-2 text-lg font-medium">Product Selection</h2>
            <div class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <label>
                  Selected Variant
                  <select v-model="selectedVariant" class="w-full rounded border p-2">
                    <option>Blue - Medium</option>
                    <option>Red - Large</option>
                    <option>Green - Small</option>
                  </select>
                </label>
                <div>
                  <label>Quantity</label>
                  <div class="flex items-center space-x-2">
                    <button
                      @click="decreaseQty"
                      class="rounded bg-gray-300 px-2 py-1 hover:bg-gray-400"
                    >
                      -
                    </button>
                    <span>{{ quantity }}</span>
                    <button
                      @click="increaseQty"
                      class="rounded bg-gray-300 px-2 py-1 hover:bg-gray-400"
                    >
                      +
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Production Parameters -->
          <div>
            <h2 class="mb-2 text-lg font-medium">Production Parameters</h2>
            <div class="grid grid-cols-3 gap-4">
              <label>
                Start Date
                <input v-model="startDate" type="date" class="w-full rounded border p-2" />
              </label>
              <label>
                Deadline
                <input v-model="deadline" type="date" class="w-full rounded border p-2" />
              </label>
              <label>
                Production Line
                <select v-model="productionLine" class="w-full rounded border p-2">
                  <option>Line 1</option>
                  <option>Line 2</option>
                  <option>Line 3</option>
                </select>
              </label>
            </div>
          </div>
        </div>
        <div class="mt-6 flex justify-end space-x-4">
          <button
            @click="submitOrder"
            class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            Create Production Order
          </button>
        </div>
      </div>
    </Popup>

    <!-- Edit Order Popup -->
    <Popup
      :visible="showEditProductionOrdersPopup"
      @update:visible="showEditProductionOrdersPopup = $event"
    >
      <div>
        <h1 class="mb-6 text-2xl font-semibold">Edit Production Order</h1>
        <div class="space-y-6">
          <!-- Order Details -->
          <div>
            <h2 class="mb-2 text-lg font-medium">Order Details</h2>
            <div class="grid grid-cols-2 gap-4">
              <label>
                Product Name
                <input
                  v-model="orderName"
                  type="text"
                  placeholder="Order Name"
                  class="w-full rounded border p-2"
                />
              </label>
              <label>
                Priority
                <select v-model="priority" class="w-full rounded border p-2">
                  <option>High</option>
                  <option>Low</option>
                </select>
              </label>
            </div>
          </div>

          <!-- Product Selection -->
          <div>
            <h2 class="mb-2 text-lg font-medium">Product Selection</h2>
            <div class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <label>
                  Selected Variant
                  <select v-model="selectedVariant" class="w-full rounded border p-2">
                    <option>Blue - Medium</option>
                    <option>Red - Large</option>
                    <option>Green - Small</option>
                  </select>
                </label>
                <div>
                  <label>Quantity</label>
                  <div class="flex items-center space-x-2">
                    <button
                      @click="decreaseQty"
                      class="rounded bg-gray-300 px-2 py-1 hover:bg-gray-400"
                    >
                      -
                    </button>
                    <span>{{ quantity }}</span>
                    <button
                      @click="increaseQty"
                      class="rounded bg-gray-300 px-2 py-1 hover:bg-gray-400"
                    >
                      +
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Production Parameters -->
          <div>
            <h2 class="mb-2 text-lg font-medium">Production Parameters</h2>
            <div class="grid grid-cols-3 gap-4">
              <label>
                Start Date
                <input v-model="startDate" type="date" class="w-full rounded border p-2" />
              </label>
              <label>
                Deadline
                <input v-model="deadline" type="date" class="w-full rounded border p-2" />
              </label>
              <label>
                Production Line
                <select v-model="productionLine" class="w-full rounded border p-2">
                  <option>Line 1</option>
                  <option>Line 2</option>
                  <option>Line 3</option>
                </select>
              </label>
            </div>
          </div>
        </div>
        <div class="mt-6 flex justify-end space-x-4">
          <button
            @click="editOrder"
            class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            Save Changes
          </button>
        </div>
      </div>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Popup from '@/components/popup.vue'
import useOrders from '@/composables/useOrders'

const { orders, deleteOrder, updateOrderDates } = useOrders()

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

const getStatusClass = (status: string) => {
  return status === 'On Track' ? 'bg-green-200 text-green-700' : 'bg-red-200 text-red-700'
}

const getPriorityClass = (priority: string) => {
  return priority === 'High' && 'high' ? 'bg-red-500 text-white' : 'bg-gray-200 text-gray-700'
}

const emitEvent = defineEmits(['close', 'submit', 'update:showProductionOrdersPopup'])

const orderName = ref('')
const priority = ref('Normal')
const selectedVariant = ref('Blue - Medium')
const quantity = ref(1)
const startDate = ref('')
const deadline = ref('')
const productionLine = ref('Line 1')
const selectedOrderId = ref<string | null>(null) // Track the selected order ID for editing

const increaseQty = () => {
  quantity.value++
}

const decreaseQty = () => {
  if (quantity.value > 1) quantity.value--
}

// Reset form fields for creating a new order
const resetCreateForm = () => {
  orderName.value = ''
  quantity.value = 1
  startDate.value = ''
  deadline.value = ''
  productionLine.value = 'Line 1'
  priority.value = 'Normal'
}

// Load orders from local storage on component mount
onMounted(() => {
  const storedOrders = localStorage.getItem('productionOrders')
  if (storedOrders) {
    orders.value = JSON.parse(storedOrders)
  }
})

// Save orders to local storage
const saveOrdersToLocalStorage = () => {
  localStorage.setItem('productionOrders', JSON.stringify(orders.value))
}

// Add a new order
const submitOrder = () => {
  const newOrder: Order = {
    id: `#${Math.floor(Math.random() * 10000)}`,
    product: orderName.value,
    quantity: quantity.value,
    status: 'On Track',
    startDate: startDate.value,
    endDate: deadline.value,
    productionLine: productionLine.value,
    priority: priority.value as 'High' | 'Low',
    dueDate: deadline.value,
  }
  orders.value.push(newOrder)
  saveOrdersToLocalStorage()
  showCreateProductionOrdersPopup.value = false
  resetCreateForm() // Reset form fields after creating an order
}

// Edit an existing order
const editOrder = () => {
  if (selectedOrderId.value) {
    const orderIndex = orders.value.findIndex((order) => order.id === selectedOrderId.value)
    if (orderIndex !== -1) {
      orders.value[orderIndex] = {
        ...orders.value[orderIndex],
        product: orderName.value,
        quantity: quantity.value,
        startDate: startDate.value,
        endDate: deadline.value,
        productionLine: productionLine.value,
        priority: priority.value as 'High' | 'Low',
        dueDate: deadline.value,
      }
      saveOrdersToLocalStorage()
      showEditProductionOrdersPopup.value = false
      resetCreateForm() // Reset form fields after editing an order
    }
  }
}

// Open the edit popup and populate the form with the selected order's data
const openEditPopup = (order: Order) => {
  selectedOrderId.value = order.id
  orderName.value = order.product
  quantity.value = order.quantity
  startDate.value = order.startDate
  deadline.value = order.endDate
  productionLine.value = order.productionLine
  priority.value = order.priority
  showEditProductionOrdersPopup.value = true
}

// Update order dates
const updateOrderDatesHandler = (payload: {
  orderId: string
  newStartTime: string
  newEndTime: string
}) => {
  const success = updateOrderDates(payload.orderId, payload.newStartTime, payload.newEndTime)
  if (!success) {
    console.error(`Failed to update order with ID ${payload.orderId}.`)
  }
}
</script>

<style>
button {
  cursor: pointer;
}
</style>
