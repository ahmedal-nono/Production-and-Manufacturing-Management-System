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
    },
    async updateRework(id: string, updates: Partial<Rework>) {
      const index = this.reworks.findIndex((rework) => rework.id === id)
      if (index >= 0) {
        this.reworks[index] = { ...this.reworks[index], ...updates }
        console.log(`Rework ${id} updated successfully`, updates)
      } else {
        console.error(`Rework with ID ${id} not found`)
      }
    },
    // async fetchReworks() {
    //   if (this.reworks.length > 0) {
    //     console.log('Reworks already loaded, skipping fetch.')
    //     return
    //   }
    //   await delay(1500) // Simulate API delay
    //   this.reworks = [
    //     {
    //       id: 'RW-001',
    //       workOrder: 'WO-001',
    //       product: 'Steel Bracket',
    //       defectLevel: 'Critical',
    //       defectType: 'Crack',
    //       affectedComponent: 'Bracket Arm',
    //       description: 'A visible crack on the bracket arm.',
    //       assignedTo: null,
    //       dueDate: '2023-12-01',
    //       status: 'Open',
    //     },
    //     {
    //       id: 'RW-002',
    //       workOrder: 'WO-002',
    //       product: 'Aluminum Frame',
    //       defectLevel: 'Major',
    //       defectType: 'Dent',
    //       affectedComponent: 'Frame Edge',
    //       description: 'A dent on the edge of the frame.',
    //       assignedTo: 'John Doe',
    //       dueDate: '2023-12-05',
    //       status: 'Completed',
    //     },
    //   ]
    //   console.log('Reworks fetched successfully:', this.reworks)
    // },
    async saveFromQualityInspection(data: Partial<Rework>) {
      try {
        const existingRework = this.reworks.find((rework) => rework.workOrder === data.workOrder)
        if (existingRework) {
          console.log('Updating existing rework:', existingRework)
          Object.assign(existingRework, {
            defectLevel: data.defectLevel || existingRework.defectLevel,
            defectType: data.defectType || existingRework.defectType,
            affectedComponent: data.affectedComponent || existingRework.affectedComponent,
            description: data.description || existingRework.description,
          })
        } else {
          const newRework: Rework = {
            id: `RW-${Date.now()}`, // Generate a unique ID
            workOrder: data.workOrder || 'Unknown',
            product: data.product || 'Unknown',
            defectLevel: data.defectLevel || 'Minor',
            defectType: data.defectType || 'Unknown',
            affectedComponent: data.affectedComponent || 'Unknown',
            description: data.description || 'No description provided',
            assignedTo: data.assignedTo || null,
            dueDate: data.dueDate || new Date().toISOString().split('T')[0],
            status: 'Open',
          }
          this.reworks.push(newRework)
          console.log('Rework saved from QualityInspectionPopup:', newRework)
        }
        notificationStore.addNotification(
          'Rework saved from Quality Inspection successfully!',
          'success',
          'manager',
        )
      } catch (error) {
        console.error('Failed to save rework from Quality Inspection:', error)
        notificationStore.addNotification(
          'Failed to save rework from Quality Inspection.',
          'error',
          'manager',
        )
      }
    },
  },
  getters: {
    getReworkById: (state) => (id: string) => state.reworks.find((rework) => rework.id === id),
    getReworkByWorkOrder: (state) => (workOrder: string) =>
      state.reworks.find((rework) => rework.workOrder === workOrder),
  },
  persist: true,
})
