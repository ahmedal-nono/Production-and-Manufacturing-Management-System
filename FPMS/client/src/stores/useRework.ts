import { defineStore } from 'pinia'
import notificationStore from '@/stores/notificationStore'

interface Rework {
  id: string
  workOrder: string
  product: string
  defectLevel: 'Critical' | 'Major' | 'Minor'
  defectType: string
  affectedComponent: string
  description: string
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
        this.persistReworks() // Persist changes
        console.log('Rework created:', rework)
        notificationStore.addNotification('Rework created successfully!', 'success', 'manager')
      } catch (error) {
        notificationStore.addNotification('Failed to create rework.', 'error', 'manager')
        console.error('Failed to create rework:', error)
        throw error
      }
    },
    async deleteRework(id: string) {
      this.reworks = this.reworks.filter((rework) => rework.id !== id)
      this.persistReworks() // Persist changes
    },
    async updateRework(id: string, updates: Partial<Rework>) {
      const index = this.reworks.findIndex((rework) => rework.id === id)
      if (index >= 0) {
        this.reworks[index] = { ...this.reworks[index], ...updates }
        this.persistReworks() // Persist changes
        console.log(`Rework ${id} updated successfully`, updates)
      } else {
        console.error(`Rework with ID ${id} not found`)
      }
    },
    persistReworks() {
      localStorage.setItem('reworks', JSON.stringify(this.reworks))
    },
    loadReworks() {
      const savedReworks = localStorage.getItem('reworks')
      if (savedReworks) {
        this.reworks = JSON.parse(savedReworks)
        console.log('Reworks loaded from localStorage:', this.reworks)
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
          defectType: 'Crack',
          affectedComponent: 'Bracket Arm',
          description: 'A visible crack on the bracket arm.',
          assignedTo: null,
          dueDate: '2023-12-01',
          status: 'Open',
        },
        {
          id: 'RW-002',
          workOrder: 'WO-002',
          product: 'Aluminum Frame',
          defectLevel: 'Major',
          defectType: 'Dent',
          affectedComponent: 'Frame Edge',
          description: 'A dent on the edge of the frame.',
          assignedTo: 'John Doe',
          dueDate: '2023-12-05',
          status: 'Completed',
        },
      ]
      this.persistReworks() // Persist fetched data
    },
  },
  getters: {
    getReworkById: (state) => (id: string) => state.reworks.find((rework) => rework.id === id),
    getReworkByWorkOrder: (state) => (workOrder: string) =>
      state.reworks.find((rework) => rework.workOrder === workOrder),
  },
  persist: true,
})
