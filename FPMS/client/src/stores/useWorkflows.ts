import { defineStore } from 'pinia'
import { useOrdersStore } from './useOrders'

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
    createWorkflow(workflow: Workflow) {
      this.workflows.push(workflow)
    },
    deleteWorkflow(id: string) {
      this.workflows = this.workflows.filter((workflow) => workflow.id !== id)
    },
    editWorkflow(workflowId: string, updatedWorkflow: Partial<Workflow>) {
      const index = this.workflows.findIndex((workflow) => workflow.id === workflowId)
      if (index >= 0) {
        this.workflows[index] = { ...this.workflows[index], ...updatedWorkflow }
      }
    },
    getWorkflowById(id: string): Workflow | undefined {
      return this.workflows.find((workflow) => workflow.id === id)
    },
    loadProductsFromOrders() {
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
  },
  persist: true,
})
