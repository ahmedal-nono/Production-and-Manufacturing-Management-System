import { defineStore } from 'pinia'
import notificationStore from '@/stores/notificationStore'

interface ProductionLine {
  id: string
  name: string
  status: 'Active' | 'Maintenance' | 'Inactive'
  currentOutput: number
  capacity: number
  utilization: number
  oee: number | null
  workcenters: number
  workflows: string[]
}

interface ProductionLineState {
  productionLines: ProductionLine[]
}

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

// @ts-ignore
export const useProductionLinesStore = defineStore('productionLines', {
  state: (): ProductionLineState => ({
    productionLines: [],
  }),
  actions: {
    async addProductionLine(line: ProductionLine) {
      try {
        await delay(1500) // Simulate API delay
        this.productionLines.push(line)
        notificationStore.addNotification(
          'Production line created successfully!',
          'success',
          'production_manager',
        )
      } catch (error) {
        notificationStore.addNotification(
          'Failed to create production line.',
          'error',
          'production_manager',
        )
        throw error
      }
    },
    async editProductionLine(id: string, updatedLine: Partial<ProductionLine>) {
      try {
        await delay(1500) // Simulate API delay
        const index = this.productionLines.findIndex((line) => line.id === id)
        if (index !== -1) {
          this.productionLines[index] = { ...this.productionLines[index], ...updatedLine }
          notificationStore.addNotification(
            'Production line updated successfully!',
            'success',
            'production_manager',
          )
        }
      } catch (error) {
        notificationStore.addNotification(
          'Failed to update production line.',
          'error',
          'production_manager',
        )
        throw error
      }
    },
    async deleteProductionLine(id: string) {
      try {
        await delay(1500) // Simulate API delay
        this.productionLines = this.productionLines.filter((line) => line.id !== id)
        notificationStore.addNotification(
          'Production line deleted successfully!',
          'success',
          'production_manager',
        )
      } catch (error) {
        notificationStore.addNotification(
          'Failed to delete production line.',
          'error',
          'production_manager',
        )
        throw error
      }
    },
  },
  getters: {
    getProductionLineById: (state) => async (id: string) => {
      try {
        // Simulate API call or fetch from state
        await delay(500) // Simulate delay
        return state.productionLines.find((line) => line.id === id) || null
      } catch (error) {
        console.error('Error fetching production line by ID:', error)
        return null
      }
    },
    getNextId: (state) => {
      const lastLine = state.productionLines[state.productionLines.length - 1]
      if (lastLine) {
        const lastId = parseInt(lastLine.id)
        return (lastId + 1).toString()
      }
      return '1'
    },
  },
  persist: true,
})
