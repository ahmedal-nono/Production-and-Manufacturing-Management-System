<template>
  <div>
    <!-- Main Production Orders Popup -->
    <Popup
      :visible="props.showProductionOrdersPopup"
      @update:visible="(value: boolean) => emit('update:showProductionOrdersPopup', value)"
      @update-dates="updateOrderDatesHandler"
    >
      <div class="p-4">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="rounded-t px-4 py-2 text-xl font-semibold">Production Order Management</h2>
          <button
            v-if="userRole === 'Production Manager'"
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
                <th class="border border-gray-700 px-4 py-2">Order Name</th>
                <th class="border border-gray-700 px-4 py-2">Product</th>
                <th class="border border-gray-700 px-4 py-2">Quantity</th>
                <th class="border border-gray-700 px-4 py-2">Start Date</th>
                <th class="border border-gray-700 px-4 py-2">End Date</th>
                <th class="border border-gray-700 px-4 py-2">Status</th>
                <th
                  v-if="userRole === 'Production Manager'"
                  class="border border-gray-700 px-4 py-2"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id" class="border border-gray-700 px-4 py-2">
                <td class="border border-gray-700 px-4 py-2">{{ order.id }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ order.order_name }}</td>
                <td class="border border-gray-700 px-4 py-2">
                  {{ getProductName(order.product) }}
                </td>
                <td class="border border-gray-700 px-4 py-2">{{ order.quantity }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ formatDate(order.start_date) }}</td>
                <td class="border border-gray-700 px-4 py-2">{{ formatDate(order.end_date) }}</td>
                <td class="border border-gray-700 px-4 py-2">
                  <span
                    :class="getStatusClass(order.status)"
                    class="rounded px-2 py-1 text-sm font-medium"
                  >
                    {{ order.status }}
                  </span>
                </td>
                <td v-if="userRole === 'Production Manager'" class="space-x-2 px-4 py-2">
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
      @update:visible="(value) => (showCreateProductionOrdersPopup = value)"
    >
      <div>
        <h1 class="mb-6 text-2xl font-semibold">Create Production Order</h1>
        <div class="space-y-6">
          <!-- Order Details -->
          <div>
            <h2 class="mb-2 text-lg font-medium">Order Details</h2>
            <div class="grid grid-cols-2 gap-4">
              <label>
                Order Name
                <input
                  v-model="orderName"
                  type="text"
                  placeholder="Order Name"
                  class="w-full rounded border p-2"
                  required
                />
              </label>
              <label>
                Priority
                <select v-model="priority" class="w-full rounded border p-2" required>
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
                  Product
                  <select v-model="productId" class="w-full rounded border p-2" required>
                    <option v-for="product in products" :key="product.id" :value="product.id">
                      {{ product.name }}
                    </option>
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
                <input
                  v-model="startDate"
                  type="datetime-local"
                  class="w-full rounded border p-2"
                  required
                />
              </label>
              <label>
                End Date
                <input
                  v-model="endDate"
                  type="datetime-local"
                  class="w-full rounded border p-2"
                  required
                />
              </label>
              <label>
                Production Line
                <select v-model="productionLine" class="w-full rounded border p-2" required>
                  <option :value="null" disabled>Select Production Line</option>
                  <option v-for="line in productionLines" :key="line.id" :value="line.id">
                    {{ line.line_name }}
                    <span v-if="line.capacity_limit">(Capacity: {{ line.capacity_limit }})</span>
                  </option>
                </select>
              </label>
              <label>
                Status
                <select v-model="status" class="w-full rounded border p-2" required>
                  <option>Pending</option>
                  <option>In Progress</option>
                  <option>Completed</option>
                  <option>Cancelled</option>
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
          <button
            @click="showCreateProductionOrdersPopup = false"
            class="rounded bg-gray-500 px-4 py-2 text-white hover:bg-gray-600"
          >
            Cancel
          </button>
        </div>
      </div>
    </Popup>

    <!-- Edit Order Popup -->
    <Popup
      :visible="showEditProductionOrdersPopup"
      @update:visible="(value) => (showEditProductionOrdersPopup = value)"
    >
      <div>
        <h1 class="mb-6 text-2xl font-semibold">Edit Production Order</h1>
        <div class="space-y-6">
          <!-- Order Details -->
          <div>
            <h2 class="mb-2 text-lg font-medium">Order Details</h2>
            <div class="grid grid-cols-2 gap-4">
              <label>
                Order Name
                <input
                  v-model="orderName"
                  type="text"
                  placeholder="Order Name"
                  class="w-full rounded border p-2"
                  required
                />
              </label>
              <label>
                Priority
                <select v-model="priority" class="w-full rounded border p-2" required>
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
                  Product
                  <select v-model="productId" class="w-full rounded border p-2" required>
                    <option v-for="product in products" :key="product.id" :value="product.id">
                      {{ product.name }}
                    </option>
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
                <input
                  v-model="startDate"
                  type="datetime-local"
                  class="w-full rounded border p-2"
                  required
                />
              </label>
              <label>
                End Date
                <input
                  v-model="endDate"
                  type="datetime-local"
                  class="w-full rounded border p-2"
                  required
                />
              </label>
              <label>
                Production Line
                <input
                  v-model="productionLine"
                  type="number"
                  placeholder="Production Line ID"
                  class="w-full rounded border p-2"
                  required
                />
              </label>
              <label>
                Status
                <select v-model="status" class="w-full rounded border p-2" required>
                  <option>Pending</option>
                  <option>In Progress</option>
                  <option>Completed</option>
                  <option>Cancelled</option>
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
          <button
            @click="showEditProductionOrdersPopup = false"
            class="rounded bg-gray-500 px-4 py-2 text-white hover:bg-gray-600"
          >
            Cancel
          </button>
        </div>
      </div>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Popup from '@/components/popup.vue'
import { useUserStore } from '@/stores/user'

const API_BASE_URL = 'http://localhost:8000/api/'

interface Order {
  id: number
  order_name: string
  priority: string
  product: number
  quantity: number
  start_date: string
  end_date: string
  production_line: number
  status: string
}

interface Product {
  id: number
  name: string
  sku: string
  category: string
  specifications: string
}

const props = defineProps<{
  showProductionOrdersPopup: boolean
}>()

const emit = defineEmits(['update:showProductionOrdersPopup'])

const userStore = useUserStore()
const userRole = userStore.user?.role

const showCreateProductionOrdersPopup = ref(false)
const showEditProductionOrdersPopup = ref(false)
const orders = ref<Order[]>([])
const products = ref<Product[]>([])
const selectedOrderId = ref<number | null>(null)
const productionLines = ref<any[]>([])
const productionLine = ref<number | null>(null)
// Form fields
const orderName = ref('')
const priority = ref('High')
const productId = ref(1)
const quantity = ref(1)
const startDate = ref('')
const endDate = ref('')
// const productionLine = ref(1)
const status = ref('Pending')

const getStatusClass = (status: string) => {
  switch (status) {
    case 'Completed':
      return 'bg-green-200 text-green-700'
    case 'In Progress':
      return 'bg-blue-200 text-blue-700'
    case 'Cancelled':
      return 'bg-red-200 text-red-700'
    default: // Pending
      return 'bg-yellow-200 text-yellow-700'
  }
}

const increaseQty = () => {
  quantity.value++
}

const decreaseQty = () => {
  if (quantity.value > 1) quantity.value--
}

const resetCreateForm = () => {
  orderName.value = ''
  priority.value = 'High'
  productId.value = products.value[0]?.id || 1
  quantity.value = 1
  startDate.value = ''
  endDate.value = ''
  productionLine.value = 1
  status.value = 'Pending'
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}

const getProductName = (productId: number) => {
  const product = products.value.find((p) => p.id === productId)
  return product ? product.name : 'Unknown Product'
}

// Fetch all production orders
const fetchOrders = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}production-orders/`)
    orders.value = response.data
  } catch (error) {
    console.error('Error fetching production orders:', error)
  }
}

// Fetch all products
const fetchProducts = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}products/`)
    products.value = response.data
    if (products.value.length > 0) {
      productId.value = products.value[0].id
    }
  } catch (error) {
    console.error('Error fetching products:', error)
  }
}

// Create a new production order
const submitOrder = async () => {
  try {
    const newOrder = {
      order_name: orderName.value,
      priority: priority.value,
      product: productId.value,
      quantity: quantity.value,
      start_date: new Date(startDate.value).toISOString(),
      end_date: new Date(endDate.value).toISOString(),
      production_line: productionLine.value,
      status: status.value,
    }

    const response = await axios.post(`${API_BASE_URL}production-orders/`, newOrder)
    orders.value.push(response.data)
    showCreateProductionOrdersPopup.value = false
    resetCreateForm()
  } catch (error) {
    console.error('Error creating production order:', error)
  }
}

// Edit an existing production order
const fetchProductionLines = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}production-lines/`)
    productionLines.value = response.data
    if (productionLines.value.length > 0) {
      productionLine.value = productionLines.value[0].id // Set default value
    }
  } catch (error) {
    console.error('Error fetching production lines:', error)
    alert('Failed to load production lines')
  }
}

const editOrder = async () => {
  if (selectedOrderId.value) {
    try {
      const updatedOrder = {
        order_name: orderName.value,
        priority: priority.value,
        product: productId.value,
        quantity: quantity.value,
        start_date: new Date(startDate.value).toISOString(),
        end_date: new Date(endDate.value).toISOString(),
        production_line: productionLine.value,
        status: status.value,
      }

      const response = await axios.put(
        `${API_BASE_URL}production-orders/${selectedOrderId.value}/`,
        updatedOrder,
      )

      const index = orders.value.findIndex((order) => order.id === selectedOrderId.value)
      if (index !== -1) {
        orders.value[index] = response.data
      }

      showEditProductionOrdersPopup.value = false
      resetCreateForm()
    } catch (error) {
      console.error('Error updating production order:', error)
    }
  }
}

// Delete a production order
const deleteOrder = async (id: number) => {
  try {
    await axios.delete(`${API_BASE_URL}production-orders/${id}/`)
    orders.value = orders.value.filter((order) => order.id !== id)
  } catch (error) {
    console.error('Error deleting production order:', error)
  }
}

// Open the edit popup and populate the form with the selected order's data
const openEditPopup = (order: Order) => {
  selectedOrderId.value = order.id
  orderName.value = order.order_name
  priority.value = order.priority
  productId.value = order.product
  quantity.value = order.quantity
  startDate.value = order.start_date.slice(0, 16)
  endDate.value = order.end_date.slice(0, 16)
  productionLine.value = order.production_line
  status.value = order.status
  showEditProductionOrdersPopup.value = true
}

// Update order dates
const updateOrderDatesHandler = async (payload: {
  orderId: number
  newStartTime: string
  newEndTime: string
}) => {
  try {
    const orderToUpdate = orders.value.find((order) => order.id === payload.orderId)
    if (orderToUpdate) {
      const updatedOrder = {
        ...orderToUpdate,
        start_date: new Date(payload.newStartTime).toISOString(),
        end_date: new Date(payload.newEndTime).toISOString(),
      }

      const response = await axios.put(
        `${API_BASE_URL}production-orders/${payload.orderId}/`,
        updatedOrder,
      )

      const index = orders.value.findIndex((order) => order.id === payload.orderId)
      if (index !== -1) {
        orders.value[index] = response.data
      }
    }
  } catch (error) {
    console.error('Error updating order dates:', error)
    return false
  }
  return true
}

// Fetch data when component is mounted
onMounted(() => {
  fetchOrders()
  fetchProducts()
  fetchProductionLines()
})
</script>

<style>
button {
  cursor: pointer;
}
</style>
