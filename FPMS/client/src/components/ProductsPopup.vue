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
              <option value="">Category</option>
              <option>Category 1</option>
              <option>Category 2</option>
            </select>
            <select v-model="variantAvailability" class="rounded border p-2">
              <option value="">Variant Availability</option>
              <option>Available</option>
              <option>Unavailable</option>
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
                <tr
                  v-for="product in filteredProducts"
                  :key="product.id"
                  class="border-t hover:bg-gray-100"
                >
                  <td class="border border-gray-700 px-4 py-2">{{ product.name }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ product.sku }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ product.category }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ product.bom }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ product.workflow }}</td>
                  <td v-if="userRole === 'Production Manager'" class="border border-gray-700 px-4 py-2">
                    <button
                    v-if="userRole === 'Production Manager'"
                      @click="openEditPopup(product)"
                      class="mr-2 rounded bg-green-600 px-3 py-1 text-white hover:bg-green-600"
                    >
                      Edit
                    </button>
                    <button
                    v-if="userRole === 'Production Manager'"
                      @click="deleteProduct(product.id)"
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
          <p class="font-medium">Product Name</p>
          <input
            v-model="newProduct.name"
            type="text"
            class="rounded border p-2"
            placeholder="Enter Product Name"
          />
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
          <p class="font-medium">Category</p>
          <input
            v-model="newProduct.category"
            type="text"
            class="rounded border p-2"
            placeholder="Enter Category"
          />
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
          <p class="font-medium">Workflows</p>
          <select v-model="newProduct.workflow" class="rounded border p-2">
            <option value="">Select Workflow</option>
            <option v-for="workflow in workflows" :key="workflow.id" :value="workflow.name">
              {{ workflow.name }}
            </option>
          </select>
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">BOMs</p>
          <select v-model="newProduct.bom" class="rounded border p-2">
            <option value="">Select BOM</option>
            <option v-for="bom in boms" :key="bom.id" :value="bom.name">
              {{ bom.name }}
            </option>
          </select>
        </div>
      </div>

      <button
        @click="createProduct"
        class="mt-4 w-2/12 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
      >
        Save Product
      </button>
    </Popup>

    <!-- Edit Product Popup -->
    <Popup :visible="showEditProductsPopup" @update:visible="showEditProductsPopup = $event">
      <div class="flex flex-col justify-start">
        <h1 class="mb-6 text-4xl font-extrabold">Edit Product</h1>
        <p class="mb-2 text-xl font-semibold">Product Definition</p>
      </div>

      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Product Name</p>
          <input
            v-model="newProduct.name"
            type="text"
            class="rounded border p-2"
            placeholder="Enter Product Name"
          />
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
          <p class="font-medium">Category</p>
          <input
            v-model="newProduct.category"
            type="text"
            class="rounded border p-2"
            placeholder="Enter Category"
          />
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
          <p class="font-medium">Workflows</p>
          <select v-model="newProduct.workflow" class="rounded border p-2">
            <option value="">Select Workflow</option>
            <option v-for="workflow in workflows" :key="workflow.id" :value="workflow.name">
              {{ workflow.name }}
            </option>
          </select>
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">BOMs</p>
          <select v-model="newProduct.bom" class="rounded border p-2">
            <option value="">Select BOM</option>
            <option v-for="bom in boms" :key="bom.id" :value="bom.name">
              {{ bom.name }}
            </option>
          </select>
        </div>
      </div>

      <button
        @click="editProduct"
        class="mt-4 w-2/12 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
      >
        Save Changes
      </button>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Popup from '@/components/popup.vue'
import { useProductsStore } from '@/stores/useProducts'
import { useWorkflowsStore } from '@/stores/useWorkflows'
import { useBOMsStore } from '@/stores/useBOMs'
import { useOrdersStore } from '@/stores/useOrders'
import { useUserStore } from '@/stores/user'

const ordersStore = useOrdersStore()
const userStore = useUserStore()
const userRole = userStore.user?.role

const showCreateProductsPopup = ref(false)
const showEditProductsPopup = ref(false)
const selectedProductId = ref<string | null>(null)

defineProps<{
  showProductsPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showProductsPopup'])

const searchQuery = ref('')
const selectedCategory = ref('')
const variantAvailability = ref('')

const productsStore = useProductsStore()
const workflowsStore = useWorkflowsStore()
const bomsStore = useBOMsStore()

const filteredProducts = computed(() => {
  return productsStore.products.filter((product) => {
    const matchesSearch =
      product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      product.sku.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesCategory =
      selectedCategory.value === '' || product.category === selectedCategory.value

    const matchesVariant =
      variantAvailability.value === '' ||
      (variantAvailability.value === 'Available' && product.variantAvailable) ||
      (variantAvailability.value === 'Unavailable' && !product.variantAvailable)

    return matchesSearch && matchesCategory && matchesVariant
  })
})

const workflows = computed(() => workflowsStore.workflows)
const boms = computed(() => bomsStore.boms)

const newProduct = ref({
  name: '',
  sku: '',
  category: '',
  bom: '',
  workflow: '',
  variantAvailable: false,
})

const resetNewProduct = () => {
  Object.assign(newProduct.value, {
    name: '',
    sku: '',
    category: '',
    bom: '',
    workflow: '',
    variantAvailable: false,
  })
}

const createProduct = async () => {
  if (!newProduct.value.name || !newProduct.value.category) {
    alert('Please fill in all required fields.')
    return
  }
  if (!newProduct.value.sku) {
    newProduct.value.sku = productsStore.generateSKU()
  }
  await productsStore.createProduct({
    id: productsStore.getLastAndUniqueId,
    ...newProduct.value,
  })
  showCreateProductsPopup.value = false
  resetNewProduct()
}

const editProduct = async () => {
  if (!selectedProductId.value) return
  await productsStore.editProduct(selectedProductId.value, newProduct.value)
  showEditProductsPopup.value = false
}

const deleteProduct = async (id: string) => {
  if (confirm('Are you sure you want to delete this product?')) {
    await productsStore.deleteProduct(id)
  }
}

const openEditPopup = (product: any) => {
  selectedProductId.value = product.id
  Object.assign(newProduct.value, product)
  showEditProductsPopup.value = true
}
</script>

<style>
button {
  cursor: pointer;
}
</style>
