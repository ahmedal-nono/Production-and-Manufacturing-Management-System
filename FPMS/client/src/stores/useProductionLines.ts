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
// @ts-ignore
export const useProductionLinesStore = defineStore('productionLines', {
  state: (): ProductionLineState => ({
    productionLines: [],
  }),
  actions: {
    addProductionLine(line: ProductionLine) {
      this.productionLines.push(line)
    },
    editProductionLine(id: string, updatedLine: Partial<ProductionLine>) {
      const index = this.productionLines.findIndex((line) => line.id === id)
      if (index !== -1) {
        this.productionLines[index] = { ...this.productionLines[index], ...updatedLine }
      }
    },
    deleteProductionLine(id: string) {
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
