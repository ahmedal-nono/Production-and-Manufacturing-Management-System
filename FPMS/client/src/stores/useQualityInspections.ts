import { defineStore } from 'pinia'
import notificationStore from '@/stores/notificationStore'
import { useWorkflowsStore } from '@/stores/useWorkflows'

interface QualityInspection {
  id: string
  workOrderId: string
  product: string
  quantity: number
  dueDate: string
  status: 'Active' | 'Inactive'
}

interface QualityInspectionState {
  inspections: QualityInspection[]
}

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

export const useQualityInspectionsStore = defineStore('qualityInspections', {
  state: (): QualityInspectionState => ({
    inspections: [],
  }),
  actions: {
    async fetchInspections() {
      await delay(1500) // Simulate API delay
      this.inspections = [
        {
          id: 'WO-001',
          workOrderId: 'WO-001',
          product: 'Steel Bracket',
          quantity: 100,
          dueDate: '2023-12-01',
          status: 'Inactive',
        },
        {
          id: 'WO-002',
          workOrderId: 'WO-002',
          product: 'Aluminum Frame',
          quantity: 50,
          dueDate: '2023-12-05',
          status: 'Active',
        },
      ]
    },
    async createInspection(inspection: QualityInspection) {
      try {
        await delay(1500) // Simulate API delay
        this.inspections.push(inspection)
        notificationStore.addNotification('Inspection created successfully!', 'success', 'manager')
      } catch (error) {
        notificationStore.addNotification('Failed to create inspection.', 'error', 'manager')
        throw error
      }
    },
    async deleteInspection(id: string) {
      await delay(1500) // Simulate API delay
      this.inspections = this.inspections.filter((inspection) => inspection.id !== id)
    },
    async updateInspection(id: string, updates: Partial<QualityInspection>) {
      const index = this.inspections.findIndex((inspection) => inspection.id === id)
      if (index >= 0) {
        this.inspections[index] = { ...this.inspections[index], ...updates }
      }
    },
    async getInspectionCheckpointByWorkflowId(workflowId: string) {
      try {
        const checkpoint = this.inspections.find(
          (inspection) => inspection.workOrderId === workflowId,
        )
        if (!checkpoint) throw new Error('Checkpoint not found')
        return checkpoint
      } catch (error) {
        console.error('Error fetching inspection checkpoint:', error)
        throw error
      }
    },
  },
  getters: {
    getInspectionById: (state) => (id: string) =>
      state.inspections.find((inspection) => inspection.id === id),
  },
  persist: true,
})
