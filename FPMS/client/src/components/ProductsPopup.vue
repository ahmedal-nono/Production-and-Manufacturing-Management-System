<template>
  <div>
    <Popup
      :visible="showProductsPopup"
      @update:visible="(value: boolean) => emitEvent('update:showProductsPopup', value)"
    >
      <div class="p-6">
        <!-- Header -->
        <div class="rounded-t-lg py-4 text-center">
          <h1 class="text-2xl font-bold">Products Management</h1>
        </div>

        <!-- Add New Button -->
        <div class="px-4 pt-4">
          <div class="mb-4 flex items-center justify-between">
            <button
              v-if="userRole === 'Production Manager'"
              @click="showCreateProductsPopup = true"
              class="rounded bg-green-600 px-4 py-2 text-white hover:bg-green-600"
            >
              + Add New Product
            </button>
          </div>

          <!-- Filters -->
          <div class="mb-4 flex flex-col gap-4 md:flex-row">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by product name or SKU"
              class="flex-1 rounded border p-2"
            />
            <select v-model="selectedCategory" class="rounded border p-2">
              <option value="">All Categories</option>
              <option v-for="category in categoryOptions" :key="category.value" :value="category.value">
                {{ category.label }}
              </option>
            </select>
          </div>

          <!-- Products Table -->
          <div class="overflow-x-auto">
            <table class="w-full border text-center">
              <thead>
                <tr class="bg-blue-500 text-white">
                  <th class="border border-gray-700 px-4 py-2">Name</th>
                  <th class="border border-gray-700 px-4 py-2">SKU</th>
                  <th class="border border-gray-700 px-4 py-2">Category</th>
                  <th class="border border-gray-700 px-4 py-2">BOM</th>
                  <th class="border border-gray-700 px-4 py-2">Workflow</th>
                  <th v-if="userRole === 'Production Manager'" class="border border-gray-700 px-4 py-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                <SkeletonRows
                  v-if="loading"
                  :rows="4"
                  :cols="userRole === 'Production Manager' ? 6 : 5"
                />
                <tr v-else-if="filteredProducts.length === 0">
                  <td colspan="6" class="py-4 text-center">No products found</td>
                </tr>
                <tr
                  v-for="product in filteredProducts"
                  v-else
                  :key="product.id"
                  class="border-t hover:bg-gray-100"
                >
                  <td class="border border-gray-700 px-4 py-2">{{ product.name }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ product.sku || '-' }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ product.category }}</td>
                  <td class="border border-gray-700 px-4 py-2">
                    {{ product.bom ? `${product.bom.name} (${product.bom.status})` : 'Not assigned' }}
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    {{ product.workflow ? product.workflow.name : 'Not assigned' }}
                  </td>
                  <td v-if="userRole === 'Production Manager'" class="border border-gray-700 px-4 py-2">
                    <button
                      @click="openEditPopup(product)"
                      class="mr-2 rounded bg-green-600 px-3 py-1 text-white hover:bg-green-600"
                    >
                      Edit
                    </button>
                    <button
                      @click="deleteProduct(product.id!)"
                      class="rounded bg-red-600 px-3 py-1 text-white hover:bg-red-700"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Popup>

    <!-- Create Product Popup -->
    <Popup :visible="showCreateProductsPopup" @update:visible="showCreateProductsPopup = $event">
      <div class="flex flex-col justify-start">
        <h1 class="mb-6 text-4xl font-extrabold">Create Product</h1>
        <p class="mb-2 text-xl font-semibold">Product Definition</p>
      </div>

      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Product Name*</p>
          <input
            v-model="newProduct.name"
            type="text"
            class="rounded border p-2"
            placeholder="Enter Product Name"
            required
          />
          <p v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</p>
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">SKU</p>
          <input
            v-model="newProduct.sku"
            type="text"
            class="rounded border p-2"
            placeholder="Auto-generated if left blank"
          />
        </div>
      </div>
      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Category*</p>
          <select v-model="newProduct.category" class="rounded border p-2" required>
            <option v-for="category in categoryOptions" :key="category.value" :value="category.value">
              {{ category.label }}
            </option>
          </select>
          <p v-if="errors.category" class="text-red-500 text-sm">{{ errors.category }}</p>
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">Specifications</p>
          <textarea
            v-model="newProduct.specifications"
            class="rounded border p-2"
            placeholder="Weight, Dimensions, etc."
          ></textarea>
        </div>
      </div>

      <h1 class="mb-2 text-xl font-semibold">Link Workflows/BOMs</h1>
      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Workflow</p>
          <select 
            v-model="newProduct.workflow_id" 
            class="rounded border p-2"
            :disabled="workflowsLoading"
          >
            <option :value="null">Select Workflow</option>
            <option 
              v-for="workflow in workflows" 
              :key="workflow.id" 
              :value="workflow.id"
            >
              {{ workflow.name }} (Product: {{ workflow.product }})
            </option>
          </select>
          <p v-if="workflowsLoading" class="text-sm text-gray-500">Loading workflows...</p>
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">BOM</p>
          <select 
            v-model="newProduct.bom_id" 
            class="rounded border p-2"
            :disabled="bomsLoading"
          >
            <option :value="null">Select BOM</option>
            <option 
              v-for="bom in boms" 
              :key="bom.id" 
              :value="bom.id"
            >
              {{ bom.name }} ({{ bom.status }})
            </option>
          </select>
          <p v-if="bomsLoading" class="text-sm text-gray-500">Loading BOMs...</p>
        </div>
      </div>

      <div class="mt-4 flex justify-between">
        <button
          @click="showCreateProductsPopup = false"
          class="rounded-lg bg-gray-500 px-4 py-2 text-white hover:bg-gray-600"
        >
          Cancel
        </button>
        <button
          @click="createProduct"
          class="rounded-lg bg-green-600 px-4 py-2 text-white hover:bg-green-700"
          :disabled="creatingProduct"
        >
          <span v-if="creatingProduct">Saving...</span>
          <span v-else>Save Product</span>
        </button>
      </div>
    </Popup>

    <!-- Edit Product Popup -->
    <Popup :visible="showEditProductsPopup" @update:visible="showEditProductsPopup = $event">
      <div class="flex flex-col justify-start">
        <h1 class="mb-6 text-4xl font-extrabold">Edit Product</h1>
        <p class="mb-2 text-xl font-semibold">Product Definition</p>
      </div>

      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Product Name*</p>
          <input
            v-model="newProduct.name"
            type="text"
            class="rounded border p-2"
            placeholder="Enter Product Name"
            required
          />
          <p v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</p>
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">SKU</p>
          <input
            v-model="newProduct.sku"
            type="text"
            class="rounded border p-2"
            placeholder="Leave Blank for auto generation"
          />
        </div>
      </div>
      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Category*</p>
          <select v-model="newProduct.category" class="rounded border p-2" required>
            <option v-for="category in categoryOptions" :key="category.value" :value="category.value">
              {{ category.label }}
            </option>
          </select>
          <p v-if="errors.category" class="text-red-500 text-sm">{{ errors.category }}</p>
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">Specifications</p>
          <textarea
            v-model="newProduct.specifications"
            class="rounded border p-2"
            placeholder="Weight, Dimensions, etc."
          ></textarea>
        </div>
      </div>

      <h1 class="mb-2 text-xl font-semibold">Link Workflows/BOMs</h1>
      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Workflow</p>
          <select 
            v-model="newProduct.workflow_id" 
            class="rounded border p-2"
            :disabled="workflowsLoading"
          >
            <option :value="null">Select Workflow</option>
            <option 
              v-for="workflow in workflows" 
              :key="workflow.id" 
              :value="workflow.id"
            >
              {{ workflow.name }} (Product: {{ workflow.product }})
            </option>
          </select>
          <p v-if="workflowsLoading" class="text-sm text-gray-500">Loading workflows...</p>
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">BOM</p>
          <select 
            v-model="newProduct.bom_id" 
            class="rounded border p-2"
            :disabled="bomsLoading"
          >
            <option :value="null">Select BOM</option>
            <option 
              v-for="bom in boms" 
              :key="bom.id" 
              :value="bom.id"
            >
              {{ bom.name }} ({{ bom.status }})
            </option>
          </select>
          <p v-if="bomsLoading" class="text-sm text-gray-500">Loading BOMs...</p>
        </div>
      </div>

      <div class="mt-4 flex justify-between">
        <button
          @click="showEditProductsPopup = false"
          class="rounded-lg bg-gray-500 px-4 py-2 text-white hover:bg-gray-600"
        >
          Cancel
        </button>
        <button
          @click="editProduct"
          class="rounded-lg bg-green-600 px-4 py-2 text-white hover:bg-green-700"
          :disabled="updatingProduct"
        >
          <span v-if="updatingProduct">Saving...</span>
          <span v-else>Save Changes</span>
        </button>
      </div>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Popup from '@/components/popup.vue'
import SkeletonRows from '@/components/SkeletonRows.vue'
import { useUserStore } from '@/stores/user'
import { baseApiUrl } from '@/api'

const API_BASE_URL = `${baseApiUrl}/`

interface Product {
  id?: number
  name: string
  sku: string
  category: string
  specifications: string
  bom: {
    id: number
    name: string
    status: string
    product_code: string
    version: string
  } | null
  workflow: {
    id: number
    name: string
    description: string
    product: number
  } | null
  bom_id?: number | null
  workflow_id?: number | null
}

interface Workflow {
  id: number
  name: string
  description: string
  product: number
  assigned_work_center: number
  stages: any[]
}

interface BOM {
  id: number
  name: string
  product_code: string
  version: string
  status: string
  last_updated: string
  components: Component[]
}

interface Component {
  id: number
  name: string
  part_number: string
  quantity: number
  unit: string
  unit_cost: string
}

interface CategoryOption {
  value: string
  label: string
}

// State
const showCreateProductsPopup = ref(false)
const showEditProductsPopup = ref(false)
const selectedProductId = ref<number | null>(null)
const products = ref<Product[]>([])
const workflows = ref<Workflow[]>([])
const boms = ref<BOM[]>([])
const loading = ref(false)
const workflowsLoading = ref(false)
const bomsLoading = ref(false)
const creatingProduct = ref(false)
const updatingProduct = ref(false)
const error = ref<string | null>(null)
const errors = ref<Record<string, string>>({})

const userStore = useUserStore()
const userRole = userStore.user?.role

// Props & Emits
defineProps<{
  showProductsPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showProductsPopup'])

// Filters
const searchQuery = ref('')
const selectedCategory = ref('')

const categoryOptions: CategoryOption[] = [
  { value: 'Electronics', label: 'Electronics' },
  { value: 'Furniture', label: 'Furniture' },
  { value: 'Automotive', label: 'Automotive' },
  { value: 'Clothing', label: 'Clothing' },
  { value: 'Food', label: 'Food' },
  { value: 'Other', label: 'Other' }
]

// Computed
const filteredProducts = computed(() => {
  return products.value.filter((product) => {
    const matchesSearch =
      product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (product.sku && product.sku.toLowerCase().includes(searchQuery.value.toLowerCase()))

    const matchesCategory =
      selectedCategory.value === '' || product.category === selectedCategory.value

    return matchesSearch && matchesCategory
  })
})

// Form data
const newProduct = ref<Product>({
  name: '',
  sku: '',
  category: 'Other',
  specifications: '',
  bom: null,
  workflow: null,
  bom_id: null,
  workflow_id: null
})

// Methods
const resetNewProduct = () => {
  newProduct.value = {
    name: '',
    sku: '',
    category: 'Other',
    specifications: '',
    bom: null,
    workflow: null,
    bom_id: null,
    workflow_id: null
  }
  errors.value = {}
}

const validateProduct = (): boolean => {
  errors.value = {}
  let isValid = true

  if (!newProduct.value.name.trim()) {
    errors.value.name = 'Product name is required'
    isValid = false
  }

  if (!newProduct.value.category) {
    errors.value.category = 'Category is required'
    isValid = false
  }

  return isValid
}

const fetchProducts = async () => {
  try {
    loading.value = true
    const response = await axios.get(`${API_BASE_URL}products/`)
    products.value = response.data.map((product: any) => ({
      ...product,
      bom_id: product.bom?.id || null,
      workflow_id: product.workflow?.id || null
    }))
  } catch (err) {
    error.value = 'Failed to fetch products'
    console.error('Error fetching products:', err)
  } finally {
    loading.value = false
  }
}

const fetchWorkflows = async () => {
  try {
    workflowsLoading.value = true
    const response = await axios.get(`${API_BASE_URL}workflows/`)
    workflows.value = response.data
  } catch (err) {
    console.error('Error fetching workflows:', err)
  } finally {
    workflowsLoading.value = false
  }
}

const fetchBOMs = async () => {
  try {
    bomsLoading.value = true
    const response = await axios.get(`${API_BASE_URL}boms/`)
    boms.value = response.data
  } catch (err) {
    console.error('Error fetching BOMs:', err)
  } finally {
    bomsLoading.value = false
  }
}

const createProduct = async () => {
  if (!validateProduct()) return

  try {
    creatingProduct.value = true
    const payload = {
      name: newProduct.value.name,
      sku: newProduct.value.sku || undefined, // Send undefined if empty to let backend handle
      category: newProduct.value.category,
      specifications: newProduct.value.specifications,
      bom_id: newProduct.value.bom_id,
      workflow_id: newProduct.value.workflow_id
    }

    const response = await axios.post(`${API_BASE_URL}products/`, payload)
    
    // Fetch the complete product with relationships
    const completeProduct = await fetchProductDetails(response.data.id)
    if (completeProduct) {
      products.value.push(completeProduct)
    }
    
    showCreateProductsPopup.value = false
    resetNewProduct()
  } catch (err: any) {
    if (err.response?.data) {
      if (typeof err.response.data === 'object') {
        errors.value = err.response.data
      } else {
        error.value = err.response.data
      }
    } else {
      error.value = 'Failed to create product'
    }
    console.error('Error creating product:', err)
  } finally {
    creatingProduct.value = false
  }
}

const editProduct = async () => {
  if (!selectedProductId.value || !validateProduct()) return

  try {
    updatingProduct.value = true
    const payload = {
      name: newProduct.value.name,
      sku: newProduct.value.sku || undefined,
      category: newProduct.value.category,
      specifications: newProduct.value.specifications,
      bom_id: newProduct.value.bom_id,
      workflow_id: newProduct.value.workflow_id
    }

    await axios.put(`${API_BASE_URL}products/${selectedProductId.value}/`, payload)
    
    // Refresh the product list to get updated relationships
    await fetchProducts()
    
    showEditProductsPopup.value = false
    resetNewProduct()
  } catch (err: any) {
    if (err.response?.data) {
      if (typeof err.response.data === 'object') {
        errors.value = err.response.data
      } else {
        error.value = err.response.data
      }
    } else {
      error.value = 'Failed to update product'
    }
    console.error('Error updating product:', err)
  } finally {
    updatingProduct.value = false
  }
}

const deleteProduct = async (id: number) => {
  if (!confirm('Are you sure you want to delete this product?')) return

  const index = products.value.findIndex((product) => product.id === id)
  if (index === -1) return
  const removed = products.value[index]
  products.value.splice(index, 1) // optimistic removal

  try {
    await axios.delete(`${API_BASE_URL}products/${id}/`)
  } catch (err) {
    products.value.splice(index, 0, removed) // rollback on failure
    error.value = 'Failed to delete product'
    console.error('Error deleting product:', err)
  }
}

const fetchProductDetails = async (productId: number) => {
  try {
    const response = await axios.get(`${API_BASE_URL}products/${productId}/`)
    return {
      ...response.data,
      bom_id: response.data.bom?.id || null,
      workflow_id: response.data.workflow?.id || null
    }
  } catch (err) {
    console.error('Error fetching product details:', err)
    return null
  }
}

const openEditPopup = async (product: Product) => {
  selectedProductId.value = product.id || null
  const fullProduct = await fetchProductDetails(product.id!)
  if (fullProduct) {
    newProduct.value = { 
      ...fullProduct,
      bom_id: fullProduct.bom?.id || null,
      workflow_id: fullProduct.workflow?.id || null
    }
  } else {
    newProduct.value = { ...product }
  }
  showEditProductsPopup.value = true
}

// Lifecycle
onMounted(() => {
  fetchProducts()
  fetchWorkflows()
  fetchBOMs()
})
</script>

<style>
button {
  cursor: pointer;
}
button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>