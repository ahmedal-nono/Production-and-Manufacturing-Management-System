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

// @ts-ignore
export const useOrdersStore = defineStore('orders', {
  state: (): OrderState => ({
    orders: [],
  }),
  actions: {
    createOrder(order: Order) {
      this.orders.push(order)
    },
    deleteOrder(id: string) {
      this.orders = this.orders.filter((order) => order.id !== id)
    },
    editOrder(orderId: string, order: Order) {
      const index = this.orders.findIndex((order) => order.id === orderId)
      if (index >= 0) {
        this.orders[index] = order
      }
    },
    updateOrderDates(orderId: string, newStartDate: string, newEndDate: string): boolean {
      console.log({
        orderId,
        newStartDate,
        newEndDate,
        orders: this.orders,
      })

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
