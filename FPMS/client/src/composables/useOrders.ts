import { ref, watch } from 'vue'

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

const LOCAL_STORAGE_KEY = 'production_orders'

const orders = ref<Order[]>([])

// Load orders from localStorage or fallback to dummy data
const loadOrders = () => {
  const saved = localStorage.getItem(LOCAL_STORAGE_KEY)
  if (saved) {
    orders.value = JSON.parse(saved)
  } else {
    orders.value = [
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
    ]
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(orders.value))
  }
}

// Save orders to localStorage whenever they change
watch(
  orders,
  (newVal) => {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(newVal))
  },
  { deep: true },
)

const saveOrdersToLocalStorage = () => {
  localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(orders.value))
}

const useOrders = () => {
  loadOrders()

  const deleteOrder = (id: string) => {
    orders.value = orders.value.filter((order) => order.id !== id)
  }

  const updateOrderDates = (orderId: string, newStartDate: string, newEndDate: string): boolean => {
    const index = orders.value.findIndex((order) => order.id === orderId)
    if (index !== -1) {
      orders.value[index].startDate = newStartDate
      orders.value[index].endDate = newEndDate
      saveOrdersToLocalStorage() // Persist changes to local storage
      return true
    } else {
      console.warn(`Order with ID ${orderId} not found.`) // Log a warning if the order is not found
      return false
    }
  }

  return {
    orders,
    deleteOrder,
    updateOrderDates, // Ensure this is included in the returned object
  }
}

export default useOrders
