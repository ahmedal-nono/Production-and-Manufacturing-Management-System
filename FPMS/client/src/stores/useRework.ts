import { defineStore } from 'pinia'
import notificationStore from '@/stores/notificationStore'

interface Rework {
  id: string
  workOrder: string
  product: string
  defectLevel: 'Critical' | 'Major' | 'Minor'
  assignedTo: string | null
  dueDate: string
  status: 'Open' | 'Completed'
}

interface ReworkState {
  reworks: Rework[]
}

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

export const useReworkStore = defineStore('rework', {
  state: (): ReworkState => ({
    reworks: [],
  }),
  actions: {
    async createRework(rework: Rework) {
      try {
        await delay(1500) // Simulate API delay
        this.reworks.push(rework)
        notificationStore.addNotification('Rework created successfully!', 'success', 'manager')
      } catch (error) {
        notificationStore.addNotification('Failed to create rework.', 'error', 'manager')
        throw error
      }
    },
    async deleteRework(id: string) {
      await delay(1500) // Simulate API delay
      this.reworks = this.reworks.filter((rework) => rework.id !== id)
    },
    async updateRework(id: string, updates: Partial<Rework>) {
      const index = this.reworks.findIndex((rework) => rework.id === id)
      if (index >= 0) {
        this.reworks[index] = { ...this.reworks[index], ...updates }
      }
    },
    async fetchReworks() {
      await delay(1500) // Simulate API delay
      this.reworks = [
        {
          id: 'RW-001',
          workOrder: 'WO-001',
          product: 'Steel Bracket',
          defectLevel: 'Critical',
          assignedTo: null,
          dueDate: '2023-12-01',
          status: 'Open',
        },
        {
          id: 'RW-002',
          workOrder: 'WO-002',
          product: 'Aluminum Frame',
          defectLevel: 'Major',
          assignedTo: 'John Doe',
          dueDate: '2023-12-05',
          status: 'Completed',
        },
      ]
    },
  },
  getters: {
    getReworkById: (state) => (id: string) => state.reworks.find((rework) => rework.id === id),
  },
  persist: true,
})
