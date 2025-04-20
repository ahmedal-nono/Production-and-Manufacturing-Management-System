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

export const useProductionLinesStore = defineStore('productionLines', {
  state: (): ProductionLineState => ({
    productionLines: [
      {
        id: '1',
        name: 'Line A',
        status: 'Active',
        currentOutput: 850,
        capacity: 1000,
        utilization: 85,
        oee: 88,
        workcenters: 5,
        workflows: ['Workflow X', 'Workflow Y'],
      },
      {
        id: '2',
        name: 'Line B',
        status: 'Maintenance',
        currentOutput: 0,
        capacity: 1200,
        utilization: 0,
        oee: null,
        workcenters: 6,
        workflows: ['Workflow Z'],
      },
      {
        id: '3',
        name: 'Line C',
        status: 'Inactive',
        currentOutput: 0,
        capacity: 800,
        utilization: 0,
        oee: null,
        workcenters: 4,
        workflows: [],
      },
    ],
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
  },
  getters: {
    getProductionLineById: (state) => (id: string) =>
      state.productionLines.find((line) => line.id === id),
    getNextId: (state) => {
      const lastId = state.productionLines.length
      return (lastId + 1).toString()
    },
  },
  persist: true,
})
