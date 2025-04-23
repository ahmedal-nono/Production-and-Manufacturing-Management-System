import { defineStore } from 'pinia'

interface Employee {
  id: string
  name: string
  role: string
}

interface EmployeeState {
  employees: Employee[]
}

export const useEmployeeStore = defineStore('employee', {
  state: (): EmployeeState => ({
    employees: [
      { id: '1', name: 'John Doe', role: 'Technician' },
      { id: '2', name: 'Jane Smith', role: 'Engineer' },
      { id: '3', name: 'Alice Johnson', role: 'Supervisor' },
    ],
  }),
  actions: {
    addEmployee(employee: Employee) {
      this.employees.push(employee)
    },
    removeEmployee(id: string) {
      this.employees = this.employees.filter((employee) => employee.id !== id)
    },
  },
})
