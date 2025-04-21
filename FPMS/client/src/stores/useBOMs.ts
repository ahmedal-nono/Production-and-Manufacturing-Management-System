import { defineStore } from 'pinia'

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

interface Component {
  name: string
  partNumber: string
  quantity: number
  unit: string
  unitCost: number
}

interface BOM {
  id: string
  name: string
  productCode: string
  version: string
  status: 'Approved' | 'Draft' | 'Pending'
  lastUpdated: string
  createdBy: string
  components: Component[]
}

interface BOMState {
  boms: BOM[]
}

export const useBOMsStore = defineStore('boms', {
  state: (): BOMState => ({
    boms: [
      {
        id: '1',
        name: 'Motor Assembly',
        productCode: 'PROD-002',
        version: 'v2.1',
        status: 'Approved',
        lastUpdated: '2024-03-15',
        createdBy: 'John Doe',
        components: [
          { name: 'Main Motor', partNumber: 'MOT-001', quantity: 1, unit: 'pc', unitCost: 150 },
        ],
      },
    ],
  }),
  actions: {
    async createBOM(bom: BOM) {
      await delay(1500) // Simulate API delay
      this.boms.push(bom)
    },
    async deleteBOM(id: string) {
      await delay(1500) // Simulate API delay
      this.boms = this.boms.filter((bom) => bom.id !== id)
    },
    async editBOM(bomId: string, updatedBOM: Partial<BOM>) {
      await delay(1500) // Simulate API delay
      const index = this.boms.findIndex((bom) => bom.id === bomId)
      if (index >= 0) {
        this.boms[index] = { ...this.boms[index], ...updatedBOM }
      }
    },
    getBOMById(id: string): BOM | undefined {
      return this.boms.find((bom) => bom.id === id)
    },
  },
  getters: {
    getLastAndUniqueId: (state) => {
      const lastBOM = state.boms[state.boms.length - 1]
      if (lastBOM) {
        const lastId = parseInt(lastBOM.id)
        return (lastId + 1).toString()
      }
      return '1'
    },
  },
  persist: true,
})
