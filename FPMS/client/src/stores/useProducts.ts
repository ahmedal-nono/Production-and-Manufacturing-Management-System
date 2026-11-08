import { defineStore } from 'pinia'
import notificationStore from '@/stores/notificationStore'

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

interface Product {
  id: string
  name: string
  sku: string
  category: string
  bom: string
  workflow: string
  variantAvailable: boolean
}

interface ProductState {
  products: Product[]
}

export const useProductsStore = defineStore('products', {
  state: (): ProductState => ({
    products: [
      {
        id: '1',
        name: 'Product A',
        sku: 'SKU001',
        category: 'Category 1',
        bom: 'BOM name',
        workflow: 'Workflow name',
        variantAvailable: true,
      },
      {
        id: '2',
        name: 'Product B',
        sku: 'SKU002',
        category: 'Category 2',
        bom: 'BOM name',
        workflow: 'Workflow name',
        variantAvailable: false,
      },
    ],
  }),
  actions: {
    async createProduct(product: Product) {
      try {
        await delay(1500) // Simulate API delay
        this.products.push(product)
        notificationStore.addNotification('Product created successfully!', 'success', 'admin')
      } catch (error) {
        notificationStore.addNotification('Failed to create product.', 'error', 'admin')
        throw error
      }
    },
    async deleteProduct(id: string) {
      try {
        await delay(1500) // Simulate API delay
        this.products = this.products.filter((product) => product.id !== id)
        notificationStore.addNotification('Product deleted successfully!', 'success', 'admin')
      } catch (error) {
        notificationStore.addNotification('Failed to delete product.', 'error', 'admin')
        throw error
      }
    },
    async editProduct(productId: string, updatedProduct: Partial<Product>) {
      await delay(1500) // Simulate API delay
      const index = this.products.findIndex((product) => product.id === productId)
      if (index >= 0) {
        this.products[index] = { ...this.products[index], ...updatedProduct }
      }
    },
    generateSKU() {
      const lastProduct = this.products[this.products.length - 1]
      const lastSkuNumber = lastProduct ? parseInt(lastProduct.sku.replace('SKU', '')) : 0
      const newSkuNumber = (lastSkuNumber + 1).toString().padStart(3, '0')
      return `SKU${newSkuNumber}`
    },
  },
  getters: {
    getProductById: (state) => (id: string) => state.products.find((product) => product.id === id),
    getLastAndUniqueId: (state) => {
      const lastProduct = state.products[state.products.length - 1]
      if (lastProduct) {
        const lastId = parseInt(lastProduct.id)
        return (lastId + 1).toString()
      }
      return '1'
    },
  },
  persist: true,
})
