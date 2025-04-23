import { defineStore } from 'pinia'
import { useOrdersStore } from './useOrders'
import notificationStore from '@/stores/notificationStore'

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

interface Stage {
  name: string
  description: string
  workcenter: string
  duration: number | null
  workorder: string
}

interface Workflow {
  id: string
  name: string
  description: string
  product: string
  stages: Stage[]
}

interface WorkflowState {
  workflows: Workflow[]
  products: string[] // Store product names from useOrders
}

export const useWorkflowsStore = defineStore('workflows', {
  state: (): WorkflowState => ({
    workflows: [
      {
        id: '1',
        name: 'Workflow A',
        description: 'Description for Workflow A',
        product: 'Product A',
        stages: [
          {
            name: 'Stage 1',
            description: 'Description 1',
            workcenter: 'Workcenter 1',
            duration: 30,
            workorder: 'Workorder 1',
          },
        ],
      },
    ],
    products: [], // Initialize products array
  }),
  actions: {
    async createWorkflow(workflow: Workflow) {
      try {
        await delay(1500) // Simulate API delay
        this.workflows.push(workflow)
        notificationStore.addNotification(
          Date.now().toString(),
          'Workflow created successfully!',
          'success',
          'manager',
        )
      } catch (error) {
        notificationStore.addNotification(
          Date.now().toString(),
          'Failed to create workflow.',
          'error',
          'manager',
        )
        throw error
      }
    },
    async deleteWorkflow(id: string) {
      try {
        await delay(1500) // Simulate API delay
        this.workflows = this.workflows.filter((workflow) => workflow.id !== id)
        notificationStore.addNotification(
          Date.now().toString(),
          'Workflow deleted successfully!',
          'success',
          'manager',
        )
      } catch (error) {
        notificationStore.addNotification(
          Date.now().toString(),
          'Failed to delete workflow.',
          'error',
          'manager',
        )
        throw error
      }
    },
    async editWorkflow(workflowId: string, updatedWorkflow: Partial<Workflow>) {
      await delay(1500) // Simulate API delay
      const index = this.workflows.findIndex((workflow) => workflow.id === workflowId)
      if (index >= 0) {
        this.workflows[index] = { ...this.workflows[index], ...updatedWorkflow }
      }
    },
    async loadProductsFromOrders() {
      await delay(1500) // Simulate API delay
      const ordersStore = useOrdersStore()
      this.products = Array.from(new Set(ordersStore.orders.map((order) => order.product)))
    },
  },
  getters: {
    getLastAndUniqueId: (state) => {
      const lastWorkflow = state.workflows[state.workflows.length - 1]
      if (lastWorkflow) {
        const lastId = parseInt(lastWorkflow.id)
        return (lastId + 1).toString()
      }
      return '1'
    },
    getWorkflowById: (state) => (id: string) => {
      return state.workflows.find((workflow) => workflow.id === id)
    },
  },
  persist: true,
})
