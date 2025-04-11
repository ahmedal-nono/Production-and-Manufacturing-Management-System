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
            <table class="w-full border text-left">
              <thead>
                <tr class="bg-blue-500 text-white">
                  <th class="p-2">Name</th>
                  <th class="p-2">SKU</th>
                  <th class="p-2">Category</th>
                  <th class="p-2">BOM</th>
                  <th class="p-2">Workflow</th>
                  <th class="p-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="product in filteredProducts"
                  :key="product.sku"
                  class="border-t hover:bg-gray-100"
                >
                  <td class="p-2">{{ product.name }}</td>
                  <td class="p-2">{{ product.sku }}</td>
                  <td class="p-2">{{ product.category }}</td>
                  <td class="p-2">{{ product.bom }}</td>
                  <td class="p-2">{{ product.workflow }}</td>
                  <td class="p-2">
                    <button
                      @click="showEditProductsPopup = true"
                      class="mr-2 rounded bg-green-600 px-3 py-1 text-white hover:bg-green-600"
                    >
                      Edit
                    </button>
                    <button class="rounded bg-red-600 px-3 py-1 text-white hover:bg-red-700">
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

    <Popup :visible="showCreateProductsPopup" @update:visible="showCreateProductsPopup = $event">
      <div class="flex flex-col justify-start">
        <h1 class="mb-6 text-4xl font-extrabold">Create Product</h1>
        <p class="mb-2 text-xl font-semibold">Product Definition</p>
      </div>

      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Product Name</p>
          <input type="text" class="rounded border p-2" placeholder="Enter Product Name" />
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">SKU</p>
          <input
            type="text"
            class="rounded border p-2"
            placeholder="Leave Blank for auto generation"
          />
        </div>
      </div>
      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Category</p>
          <select v-model="selectedCategory" class="rounded border p-2">
            <option value="">Category</option>
            <option>Category 1</option>
            <option>Category 2</option>
          </select>
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">Specifications</p>
          <textarea type="text" class="rounded border p-2" placeholder="Weight, Dimensions, etc." />
        </div>
      </div>

      <h1 class="mb-2 text-xl font-semibold">Link Workflows/BOMs</h1>
      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Workflows</p>
          <input type="text" class="rounded border p-2" placeholder="Search Workflows" />
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">BOMs</p>
          <input type="text" class="rounded border p-2" placeholder="Search BOMs" />
        </div>
      </div>

      <button class="mt-4 w-2/12 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white">
        Save Product
      </button>
    </Popup>

    <Popup :visible="showEditProductsPopup" @update:visible="showEditProductsPopup = $event">
      <div class="flex flex-col justify-start">
        <h1 class="mb-6 text-4xl font-extrabold">Edit Product</h1>
        <p class="mb-2 text-xl font-semibold">Product Definition</p>
      </div>

      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Product Name</p>
          <input type="text" class="rounded border p-2" placeholder="Enter Product Name" />
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">SKU</p>
          <input
            type="text"
            class="rounded border p-2"
            placeholder="Leave Blank for auto generation"
          />
        </div>
      </div>
      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Category</p>
          <select v-model="selectedCategory" class="rounded border p-2">
            <option value="">Category</option>
            <option>Category 1</option>
            <option>Category 2</option>
          </select>
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">Specifications</p>
          <textarea type="text" class="rounded border p-2" placeholder="Weight, Dimensions, etc." />
        </div>
      </div>

      <h1 class="mb-2 text-xl font-semibold">Link Workflows/BOMs</h1>
      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="font-medium">Workflows</p>
          <input type="text" class="rounded border p-2" placeholder="Search Workflows" />
        </div>
        <div class="flex w-full flex-col">
          <p class="font-medium">BOMs</p>
          <input type="text" class="rounded border p-2" placeholder="Search BOMs" />
        </div>
      </div>

      <button class="mt-4 w-2/12 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white">
        Save Product
      </button>
    </Popup>
  </div>
</template>
<script setup lang="ts">
import { ref, computed } from 'vue'
import Popup from '@/components/popup.vue'

const showCreateProductsPopup = ref(false)
const showEditProductsPopup = ref(false)

defineProps<{
  showProductsPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showProductsPopup'])

const searchQuery = ref('')
const selectedCategory = ref('')
const variantAvailability = ref('')

const products = ref([
  {
    name: 'Product A',
    sku: 'SKU001',
    category: 'Category 1',
    bom: 'BOM name',
    workflow: 'Workflow name',
    variantAvailable: true,
  },
  {
    name: 'Product B',
    sku: 'SKU002',
    category: 'Category 2',
    bom: 'BOM name',
    workflow: 'Workflow name',
    variantAvailable: false,
  },
])

const filteredProducts = computed(() => {
  return products.value.filter((product) => {
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
</script>

<style scoped>
th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
</style>
