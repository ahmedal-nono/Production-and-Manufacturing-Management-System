import { defineStore } from 'pinia'
import axios from 'axios'
import notificationStore from '@/stores/notificationStore'
import { baseApiUrl } from '@/api'

export interface Rework {
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
  loading: boolean
  error: string
}

const API_URL = `${baseApiUrl}/rework-requests/`

const SEVERITY_LABELS: Record<string, Rework['defectLevel']> = {
  critical: 'Critical',
  major: 'Major',
  minor: 'Minor',
}

const fromApi = (item: any): Rework => ({
  id: String(item.id),
  workOrder: item.workorder_id != null ? `WO-${item.workorder_id}` : '',
  product: item.product_name || '',
  defectLevel: SEVERITY_LABELS[String(item.severity).toLowerCase()] || 'Minor',
  defectType: item.defect_type || '',
  affectedComponent: item.affected_component || '',
  description: item.description || '',
  assignedTo: null,
  dueDate: String(item.updated_at || item.created_at || '').split('T')[0],
  status: item.status === 'pending' ? 'Open' : 'Completed',
})

const toApiStatus = (status: Rework['status']): string =>
  status === 'Open' ? 'pending' : 'approved'

export const useReworkStore = defineStore('rework', {
  state: (): ReworkState => ({
    reworks: [],
    loading: false,
    error: '',
  }),
  actions: {
    async fetchReworks() {
      this.loading = true
      this.error = ''
      try {
        const { data } = await axios.get(API_URL)
        this.reworks = (Array.isArray(data) ? data : []).map(fromApi)
      } catch (error) {
        this.error = 'Failed to load rework requests'
        console.error('Failed to fetch reworks:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    async deleteRework(id: string) {
      // The backend has no delete endpoint for reworks; they follow inspections.
      this.reworks = this.reworks.filter((rework) => rework.id !== id)
    },
    async updateRework(id: string, updates: Partial<Rework>) {
      const index = this.reworks.findIndex((rework) => rework.id === id)
      if (index < 0) {
        console.error(`Rework with ID ${id} not found`)
        return
      }
      const previous = this.reworks[index]
      // Apply the change immediately so the UI responds instantly.
      this.reworks[index] = { ...previous, ...updates }
      if (updates.status) {
        try {
          await axios.patch(`${API_URL}${id}/`, { status: toApiStatus(updates.status) })
        } catch (error) {
          // Roll back to the previous state when the server rejects the change.
          this.reworks[index] = previous
          notificationStore.addNotification('Failed to update rework.', 'error', 'manager')
          console.error('Failed to update rework status:', error)
          throw error
        }
      }
      notificationStore.addNotification('Rework updated successfully!', 'success', 'manager')
    },
    async saveFromQualityInspection() {
      // Rework requests are created server-side when an inspection decision is
      // "rework"; just refresh the list so the new request shows up.
      try {
        await this.fetchReworks()
        notificationStore.addNotification(
          'Rework saved from Quality Inspection successfully!',
          'success',
          'manager',
        )
      } catch (error) {
        notificationStore.addNotification(
          'Failed to save rework from Quality Inspection.',
          'error',
          'manager',
        )
        console.error('Failed to save rework from Quality Inspection:', error)
      }
    },
  },
  getters: {
    getReworkById: (state) => (id: string) =>
      state.reworks.find((rework) => rework.id === id),
    getReworkByWorkOrder: (state) => (workOrder: string) =>
      state.reworks.find((rework) => rework.workOrder === workOrder),
  },
  persist: true,
})
