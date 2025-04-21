import { defineStore } from 'pinia'
import piniaPersistedState from 'pinia-plugin-persistedstate'

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

interface OrderState {
  orders: Order[]
}

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

// @ts-ignore
export const useOrdersStore = defineStore('orders', {
  state: (): OrderState => ({
    orders: [],
  }),
  actions: {
    async createOrder(order: Order) {
      await delay(1500) // Simulate API delay
      this.orders.push(order)
    },
    async deleteOrder(id: string) {
      await delay(1500) // Simulate API delay
      this.orders = this.orders.filter((order) => order.id !== id)
    },
    async editOrder(orderId: string, order: Order) {
      await delay(1500) // Simulate API delay
      const index = this.orders.findIndex((order) => order.id === orderId)
      if (index >= 0) {
        this.orders[index] = order
      }
    },
    async updateOrderDates(
      orderId: string,
      newStartDate: string,
      newEndDate: string,
    ): Promise<boolean> {
      await delay(1500) // Simulate API delay
      const index = this.orders.findIndex((order) => order.id === orderId)
      if (index !== -1) {
        this.orders[index].startDate = newStartDate
        this.orders[index].endDate = newEndDate
        return true
      } else {
        console.warn(`Order with ID ${orderId} not found.`)
        return false
      }
    },
  },
  getters: {
    getOrderById: (state) => (id: string) => state.orders.find((order) => order.id === id),
    getLastAndUniqeId: (state) => {
      const lastOrder = state.orders[state.orders.length - 1]
      if (lastOrder) {
        const lastId = parseInt(lastOrder.id)
        return (lastId + 1).toString()
      }
      return '1'
    },
  },
  persist: true,
})
