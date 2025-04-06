<template>
  <div class="m-2 flex h-max flex-col justify-center rounded-2xl bg-gray-200 p-4">
    <p class="flex justify-center text-xl font-bold">Production & Workflow Management</p>
    <div class="flex flex-row gap-10 py-4">
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showProductionPopup = true"
      >
        <img src="@/assets/production.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Production</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showWorkflowsPopup = true"
      >
        <img src="@/assets/workflows.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Workflows</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showProductionOrdersPopup = true"
      >
        <img src="@/assets/production_line.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Production Lines</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showProductionOrdersPopup = true"
      >
        <img src="@/assets/bom.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">BOMs</p>
      </div>
    </div>
  </div>

  <Popup :visible="showProductionPopup" @update:visible="showProductionPopup = $event">
    <div class="m-2 flex h-max flex-col justify-center rounded-2xl bg-gray-200 p-4">
      <p class="flex justify-center text-xl font-bold">Production Management</p>
      <div class="flex flex-row gap-10 py-4">
        <div
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
          @click="showProductionSchedulePopup = true"
        >
          <img src="@/assets/production_schedule.png" class="size-20" alt="" />
          <p class="pt-2 text-[13px] font-bold">Production Schedule</p>
        </div>
        <div
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
          @click="showProductionOrdersPopup = true"
        >
          <img src="@/assets/production_orders.png" class="size-20" alt="" />
          <p class="pt-2 text-[13px] font-bold">Production Orders</p>
        </div>
        <div
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
          @click="showProductsPopup = true"
        >
          <img src="@/assets/products.png" class="size-20" alt="" />
          <p class="pt-2 text-[13px] font-bold">Products</p>
        </div>
      </div>
    </div>
  </Popup>

  <Popup
    :visible="showProductionSchedulePopup"
    @update:visible="showProductionSchedulePopup = $event"
  >
    <div class="rounded-lg bg-white p-4 shadow-md">
      <h2 class="mb-4 text-xl font-semibold">Production Orders</h2>

      <!-- Filters -->
      <div class="mb-4 flex gap-2">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search orders..."
          class="w-full rounded border p-2"
        />
        <select v-model="selectedStatus" class="rounded border p-2">
          <option>All Statuses</option>
          <option>On Track</option>
          <option>Delayed</option>
        </select>
        <select v-model="selectedLine" class="rounded border p-2">
          <option>All Lines</option>
          <option>Line 1</option>
          <option>Line 2</option>
        </select>
      </div>

      <!-- Table -->
      <table class="w-full border-collapse border">
        <thead class="bg-gray-100">
          <tr>
            <th class="border p-2">Order ID</th>
            <th class="border p-2">Product</th>
            <th class="border p-2">Quantity</th>
            <th class="border p-2">Status</th>
            <th class="border p-2">Start Date</th>
            <th class="border p-2">End Date</th>
            <th class="border p-2">Production Line</th>
            <th class="border p-2">Priority</th>
            <th class="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in filteredOrders" :key="order.id" class="text-center">
            <td @click="showProductInfoPopup = true" class="border p-2">{{ order.id }}</td>
            <td class="border p-2">{{ order.product }}</td>
            <td class="border p-2">{{ order.quantity }}</td>
            <td class="border p-2">
              <span
                @click="showProductInfoPopup = true"
                class="rounded px-2 py-1"
                :class="getStatusClass(order.status)"
              >
                {{ order.status }}
              </span>
            </td>
            <td class="border p-2">
              <input type="date" v-model="order.startDate" class="w-full rounded border p-1" />
            </td>
            <td class="border p-2">
              <input type="date" v-model="order.endDate" class="w-full rounded border p-1" />
            </td>
            <td class="border p-2">{{ order.productionLine }}</td>
            <td class="border p-2">
              <span :class="getPriorityClass(order.priority)"> ● {{ order.priority }} </span>
            </td>
            <td class="border p-2">
              <button
                @click="showReschedulePopup = true"
                class="mt-4 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
              >
                Reschedule
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </Popup>

  <Popup :visible="showReschedulePopup" @update:visible="showReschedulePopup = $event">
    <div>
      <h2 class="mb-1 text-xl font-bold">
        Reschedule Order: <span class="font-bold">{{ props.orderId }}</span>
        <p class="mt-2 mb-1 text-sm text-gray-600">
          Current Schedule: <span class="font-medium">{{ props.schedule }}</span>
        </p>
        <p class="mb-4 text-sm text-gray-600">
          Production Line: <span class="font-medium">{{ props.line }}</span>
        </p>
      </h2>
      <div class="">
        <div class="flex flex-col justify-between">
          <label class="mb-1 block text-sm">New Start Time </label>
          <input v-model="newStartTime" type="datetime-local" class="rounded border p-2" />
        </div>
        <div class="flex flex-col justify-between">
          <label class="mt-2 mb-1 text-sm">New End Time </label>
          <input v-model="newEndTime" type="datetime-local" class="rounded border p-2" />
        </div>
      </div>
      <div class="mt-2 mb-4 flex flex-col justify-between">
        <label class="mb-1 text-sm">Reason for Reschedule </label>
        <select v-model="reason" class="rounded border p-2">
          <option value="" disabled>Select a reason</option>
          <option v-for="r in reasons" :key="r" :value="r">{{ r }}</option>
        </select>
      </div>
      <div class="mb-4">
        <label class="mb-1 text-sm">Additional Notes</label>
        <input
          v-model="note"
          type="text"
          class="w-full rounded border p-2"
          placeholder="Add any notes..."
        />
      </div>

      <!-- Buttons -->

      <button
        @click="submitReschedule"
        class="mt-4 w-full cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
      >
        Reschedule
      </button>
    </div>
  </Popup>

  <Popup :visible="showProductInfoPopup" @update:visible="showProductInfoPopup = $event">
    <div class="rounded-lg bg-gray-100 p-4 shadow">
      <div class="mb-4">
        <h2 class="text-lg font-semibold">Order #{{ props.orderId }} - Product A</h2>
        <span
          :class="
            props.status === 'On Track' ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'
          "
          class="rounded px-2 py-1 text-sm font-medium"
        >
          {{ props.status }}
        </span>
        <p class="text-sm text-gray-600">Production Line: {{ props.line }}</p>
        <p class="text-sm text-gray-600">Quantity: {{ props.quantity }} units</p>
      </div>

      <!-- Progress Bar -->
      <div class="mb-4 h-2 w-full overflow-hidden rounded bg-gray-300">
        <div class="h-full bg-blue-600" :style="{ width: props.progress + '%' }"></div>
      </div>

      <!-- Stages -->
      <div class="grid grid-cols-2 gap-4">
        <div v-for="(stage, index) in stages" :key="index" class="rounded border bg-white p-3">
          <h3 class="font-semibold">{{ stage.name }}</h3>
          <p class="text-sm text-gray-700">Status: {{ stage.status }}</p>
          <p class="text-sm text-gray-700">Assigned to: {{ stage.team }}</p>
        </div>
      </div>
    </div>
  </Popup>

  <Popup :visible="showProductionOrdersPopup" @update:visible="showProductionOrdersPopup = $event">
    <div class="p-4">
      <div class="mb-4 flex items-center justify-between">
        <h2 class="rounded-t px-4 py-2 text-xl font-semibold">Production Order Management</h2>
        <button
          @click="showCreateProductionOrdersPopup = true"
          class="cursor-pointer rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          Create New Production Order
        </button>
      </div>

      <div class="">
        <h3 class="p-4 text-lg font-medium">Existing Production Orders</h3>
        <table class="min-w-full table-auto">
          <thead>
            <tr class="bg-blue-700 text-white">
              <th class="px-4 py-2 text-left">Order ID</th>
              <th class="px-4 py-2 text-left">Product name</th>
              <th class="px-4 py-2 text-left">Quantity</th>
              <th class="px-4 py-2 text-left">Due Date</th>
              <th class="px-4 py-2 text-left">Status</th>
              <th class="px-4 py-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.id" class="border-b">
              <td class="px-4 py-2">{{ order.id }}</td>
              <td class="px-4 py-2">{{ order.product }}</td>
              <td class="px-4 py-2">{{ order.quantity }}</td>
              <td class="px-4 py-2">{{ order.dueDate }}</td>
              <td class="px-4 py-2">
                <span
                  :class="getStatusClass(order.status)"
                  class="rounded px-2 py-1 text-sm font-medium"
                >
                  {{ order.status }}
                </span>
              </td>
              <td class="space-x-2 px-4 py-2">
                <button class="cursor-pointer rounded bg-gray-200 px-3 py-1 hover:bg-gray-300">
                  Edit
                </button>
                <button class="cursor-pointer rounded bg-gray-200 px-3 py-1 hover:bg-gray-300">
                  View
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Popup>

  <Popup
    :visible="showCreateProductionOrdersPopup"
    @update:visible="showCreateProductionOrdersPopup = $event"
  >
    <div>
      <h1 class="mb-6 text-2xl font-semibold">Create Production Order</h1>

      <!-- Order Details -->

      <div class="ml-4 flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <h2 class="mb-4 text-lg font-medium">Order Details</h2>
          <input
            v-model="orderName"
            type="text"
            placeholder="Order Name"
            class="rounded border p-2"
          />
        </div>
        <div class="flex w-full flex-col">
          <h2 class="mb-4 text-lg font-medium">Priority</h2>
          <select v-model="priority" class="rounded border p-2">
            <option>Normal</option>
            <option>High</option>
            <option>Low</option>
          </select>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-4 md:grid-cols-2"></div>
      <section class="mb-6 rounded p-4">
        <h2 class="mb-4 text-lg font-semibold">Product Selection</h2>
        <input
          v-model="searchProduct"
          type="text"
          placeholder="Search products..."
          class="mb-4 w-full rounded border p-2"
        />
        <div class="flex flex-col items-center gap-4 md:flex-row">
          <select v-model="selectedVariant" class="flex-1 rounded border p-2">
            <option>Blue - Medium</option>
            <option>Red - Large</option>
            <option>Green - Small</option>
          </select>
          <div class="flex items-center gap-2">
            <button @click="decreaseQty" class="rounded border px-3 py-1">-</button>
            <input v-model="quantity" type="number" class="w-16 rounded border p-1 text-center" />
            <button @click="increaseQty" class="rounded border px-3 py-1">+</button>
          </div>
        </div>
      </section>

      <section class="mb-6 rounded p-4">
        <h2 class="mb-4 text-lg font-semibold">Production Parameters</h2>
        <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
          <input v-model="startDate" type="date" class="rounded border p-2" />
          <input v-model="deadline" type="date" class="rounded border p-2" />
          <select v-model="productionLine" class="rounded border p-2">
            <option>Line 1</option>
            <option>Line 2</option>
            <option>Line 3</option>
          </select>
        </div>
      </section>

      <div class="flex justify-end gap-4">
        <button @click="submitOrder" class="rounded bg-blue-600 px-4 py-2 text-white">
          Create Production Order
        </button>
      </div>
    </div>
  </Popup>

  <Popup :visible="showProductsPopup" @update:visible="showProductsPopup = $event">
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
  <Popup :visible="showWorkflowsPopup" @update:visible="showWorkflowsPopup = $event">
    <div>
      <h1 class="mb-6 text-3xl font-extrabold">Existing Workflows</h1>
      <div class="overflow-x-auto">
        <table class="w-full border text-left">
          <thead>
            <tr class="bg-blue-500 text-white">
              <th class="p-2">Workflow Name</th>
              <th class="p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="product in filteredProducts"
              :key="product.sku"
              class="border-t hover:bg-gray-100"
            >
              <td class="p-2">{{ product.workflow }}</td>
              <td class="p-2">
                <button
                  @click="showViewWorkflowPopup = true"
                  class="mr-2 rounded bg-blue-600 px-3 py-1 text-white hover:bg-green-600"
                >
                  View
                </button>
                <button
                  @click="showEditWorkflowPopup = true"
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
    <button
      @click="showCreateWorkflowPopup = true"
      class="mr-2 rounded bg-blue-600 px-3 py-1 text-white hover:bg-green-600"
    >
      Create New Workflow
    </button>
  </Popup>

  <Popup :visible="showViewWorkflowPopup" @update:visible="showViewWorkflowPopup = $event">
    <div></div>
  </Popup>
  <Popup :visible="showEditWorkflowPopup" @update:visible="showEditWorkflowPopup = $event">
    <div></div>
  </Popup>
  <Popup :visible="showCreateWorkflowPopup" @update:visible="showCreateWorkflowPopup = $event">
    <div class="flex flex-col justify-start">
      <h1 class="mb-6 text-4xl font-extrabold">Create New Workflow</h1>
      <p class="mb-2 text-xl font-semibold">Workflow Details</p>
    </div>

    <div class="flex flex-row gap-4">
      <div class="flex w-full flex-col">
        <p class="font-medium">Workflow Name</p>
        <input type="text" class="rounded border p-2" placeholder="Enter Workflow Name" />
      </div>
    </div>
    <div class="flex flex-row gap-4">
      <div class="flex w-full flex-col">
        <p class="font-medium">Description</p>
        <textarea type="text" class="rounded border p-2" placeholder="Enter Workflow Description" />
      </div>
    </div>
    <div class="flex flex-row gap-4">
      <div class="flex w-full flex-col">
        <p class="font-medium">Product/Process Selection</p>
        <select v-model="selectedCategory" class="rounded border p-2">
          <option value="">Select Product</option>
          <option>Category 1</option>
          <option>Category 2</option>
        </select>
      </div>
    </div>

    <h1 class="mb-2 text-xl font-semibold">Define Stages</h1>

    <div class="overflow-x-auto">
      <table class="w-full border text-left">
        <thead>
          <tr class="bg-blue-500 text-white">
            <th class="p-2">Stage Name</th>
            <th class="p-2">Description</th>
            <th class="p-2">Assigned Workcenter</th>
            <th class="p-2">Duration (min)</th>
            <th class="p-2">Workorders</th>
            <th class="p-2">Inspection checkpoint</th>
            <th class="p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="product in filteredProducts"
            :key="product.sku"
            class="border-t hover:bg-gray-100"
          >
            <td class="p-2">
              <input
                class="rounded-xl border border-black p-1"
                type="text"
                placeholder="Stage Name"
              />
            </td>
            <td class="p-2">
              <input
                class="rounded-xl border border-black p-1"
                type="text"
                placeholder="Description"
              />
            </td>
            <td class="p-2">
              <select v-model="selectedCategory" class="rounded border p-2">
                <option value="">Select Workcenter</option>
                <option>Category 1</option>
                <option>Category 2</option>
              </select>
            </td>
            <td class="p-2">
              <input
                class="rounded-xl border border-black p-1"
                type="text"
                placeholder="Duration"
              />
            </td>
            <td class="p-2">
              <select v-model="selectedCategory" class="rounded border p-2">
                <option value="">Select Workorder</option>
                <option>Category 1</option>
                <option>Category 2</option>
              </select>
            </td>
            <td class="p-2">
              <button
                @click="showCreateQualityInspectionCheckpointPopup = true"
                class="w-9/12 rounded-md bg-gray-300 p-0.5"
              >
                Create
              </button>
            </td>
            <td class="p-2">
              <button class="rounded bg-red-600 px-3 py-1 text-white hover:bg-red-700">
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <button class="mt-4 w-2/12 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white">
        Add Stage
      </button>
    </div>

    <div class="flex justify-end">
      <button class="mt-4 w-2/12 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white">
        Save
      </button>
    </div>
  </Popup>

  <Popup
    :visible="showCreateQualityInspectionCheckpointPopup"
    @update:visible="showCreateQualityInspectionCheckpointPopup = $event"
  >
    <div>
      <div class="flex flex-col items-center justify-center">
        <h1 class="mb-6 text-4xl font-extrabold">Create Quality Inspection Checkpoints</h1>
      </div>

      <div class="mb-3 flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="mb-2 font-medium">Checkpoint Name</p>
          <input type="text" class="rounded border p-2" placeholder="Enter Checkpoint Name" />
        </div>
      </div>
      <div class="mb-3 flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="mb-2 font-medium">Inspection Criteria</p>
          <textarea
            type="text"
            class="rounded border p-2"
            placeholder="Describe inspection criteria (e.g., Dimensions, checks, material validation)"
          />
        </div>
      </div>
      <div class="flex flex-row gap-4">
        <div class="flex w-full flex-col">
          <p class="mb-2 font-medium">Tools/Equipment Required</p>
          <input
            type="text"
            class="rounded border p-2"
            placeholder="List tools or equipment required"
          />
        </div>
      </div>
    </div>
    <div class="flex justify-end">
      <button class="mt-4 w-2/12 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white">
        Save Checkpoint
      </button>
    </div>
  </Popup>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Popup from '@/components/popup.vue'

const showProductionPopup = ref(false)
const showProductionSchedulePopup = ref(false)
const showProductionOrdersPopup = ref(false)
const showReschedulePopup = ref(false)
const showProductsPopup = ref(false)
const showProductInfoPopup = ref(false)
const showCreateProductionOrdersPopup = ref(false)
const showCreateProductsPopup = ref(false)
const showEditProductsPopup = ref(false)
const showWorkflowsPopup = ref(false)
const showEditWorkflowPopup = ref(false)
const showViewWorkflowPopup = ref(false)
const showCreateWorkflowPopup = ref(false)
const showCreateQualityInspectionCheckpointPopup = ref(false)

interface Order {
  id: string
  product: string
  quantity: number
  status: 'On Track' | 'Delayed'
  startDate: string
  endDate: string
  productionLine: string
  priority: 'High' | 'Low'
  dueDate: string
}

const orders = ref<Order[]>([
  {
    id: '#1234',
    product: 'Product A',
    quantity: 500,
    status: 'On Track',
    startDate: '2024-03-15',
    endDate: '2024-03-20',
    productionLine: 'Line 1',
    priority: 'High',
    dueDate: '2024-03-20',
  },
  {
    id: '#1235',
    product: 'Product B',
    quantity: 1000,
    status: 'Delayed',
    startDate: '2024-03-18',
    endDate: '2024-03-22',
    productionLine: 'Line 2',
    priority: 'Low',
    dueDate: '2024-03-22',
  },
])

const searchQuery = ref('')
const selectedStatus = ref('All Statuses')
const selectedLine = ref('All Lines')

const filteredOrders = computed(() => {
  return orders.value.filter((order) => {
    return (
      (selectedStatus.value === 'All Statuses' || order.status === selectedStatus.value) &&
      (selectedLine.value === 'All Lines' || order.productionLine === selectedLine.value) &&
      order.product.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })
})

const getStatusClass = (status: string) => {
  return status === 'On Track' ? 'bg-green-200 text-green-700' : 'bg-red-200 text-red-700'
}

const getPriorityClass = (priority: string) => {
  return priority === 'High' ? 'text-red-600' : 'text-blue-600'
}

const props = defineProps<{
  orderId: string
  schedule: string
  line: string
  quantity: number
  status: 'On Track' | 'Delayed'
  progress: number
  stages: {
    name: string
    status: string
    team: string
  }[]
}>()

const emit = defineEmits(['close', 'submit'])

const newStartTime = ref<string>('')
const newEndTime = ref<string>('')
const reason = ref<string>('')
const note = ref<string>('')

const reasons = [
  'Machine Breakdown',
  'Material Shortage',
  'Staff Unavailable',
  'Power Outage',
  'Other',
]

const submitReschedule = () => {
  const payload = {
    orderId: props.orderId,
    newStartTime: newStartTime.value,
    newEndTime: newEndTime.value,
    reason: reason.value,
    note: note.value,
  }
  emit('submit', payload)
}
const stages = ref([
  { name: 'Material Preparation', status: 'Queued', team: 'Team A' },
  { name: 'Assembly Process', status: 'In Progress', team: 'Team B' },
])

const orderName = ref('')
const priority = ref('Normal')
const searchProduct = ref('')
const selectedVariant = ref('Blue - Medium')
const quantity = ref(1)
const startDate = ref('')
const deadline = ref('')
const productionLine = ref('Line 1')

const increaseQty = () => {
  quantity.value++
}

const decreaseQty = () => {
  if (quantity.value > 1) quantity.value--
}

const submitOrder = () => {
  const payload = {
    orderName: orderName.value,
    priority: priority.value,
    selectedVariant: selectedVariant.value,
    quantity: quantity.value,
    startDate: startDate.value,
    deadline: deadline.value,
    productionLine: productionLine.value,
  }
}

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
