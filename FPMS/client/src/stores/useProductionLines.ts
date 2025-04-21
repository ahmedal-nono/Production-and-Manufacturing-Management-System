import { defineStore } from 'pinia'

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
      await delay(1000) // Simulate API delay
      this.productionLines.push(line)
    },
    async editProductionLine(id: string, updatedLine: Partial<ProductionLine>) {
      await delay(1000) // Simulate API delay
      const index = this.productionLines.findIndex((line) => line.id === id)
      if (index !== -1) {
        this.productionLines[index] = { ...this.productionLines[index], ...updatedLine }
      }
    },
    async deleteProductionLine(id: string) {
      await delay(1000) // Simulate API delay
      this.productionLines = this.productionLines.filter((line) => line.id !== id)
    },
  },
  getters: {
    getProductionLineById: (state) => (id: string) =>
      state.productionLines.find((line) => line.id === id),
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
