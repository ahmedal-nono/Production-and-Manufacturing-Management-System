<template>
  <div class="m-2 flex h-max flex-col justify-center rounded-2xl bg-gray-200 p-4">
    <p class="flex justify-center text-xl font-bold">Production & Workflow Management</p>
    <div class="flex flex-row gap-10 py-4">
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showWorkCenterPopup = true"
      >
        <img src="@/assets/production.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Production</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showRealTimePerformancePopup = true"
      >
        <img src="@/assets/workflows.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Workflows</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showMaintenancePopup = true"
      >
        <img src="@/assets/production_line.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Production Lines</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showMaintenancePopup = true"
      >
        <img src="@/assets/bom.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">BOMs</p>
      </div>
    </div>
  </div>

  <Popup :visible="showWorkCenterPopup" @update:visible="showWorkCenterPopup = $event">
    <div class="m-2 flex h-max flex-col justify-center rounded-2xl bg-gray-200 p-4">
      <p class="flex justify-center text-xl font-bold">Production Management</p>
      <div class="flex flex-row gap-10 py-4">
        <div
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
          @click="showWorkCenterPopup2 = true"
        >
          <img src="@/assets/production_schedule.png" class="size-20" alt="" />
          <p class="pt-2 text-[13px] font-bold">Production Schedule</p>
        </div>
        <div
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
          @click="showRealTimePerformancePopup = true"
        >
          <img src="@/assets/production_orders.png" class="size-20" alt="" />
          <p class="pt-2 text-[13px] font-bold">Production Orders</p>
        </div>
        <div
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
          @click="showMaintenancePopup = true"
        >
          <img src="@/assets/products.png" class="size-20" alt="" />
          <p class="pt-2 text-[13px] font-bold">Products</p>
        </div>
      </div>
    </div>
  </Popup>

  <Popup :visible="showWorkCenterPopup2" @update:visible="showWorkCenterPopup2 = $event">
    <div class="p-4 bg-white rounded-lg shadow-md">
    <h2 class="text-xl font-semibold mb-4">Production Orders</h2>

    <!-- Filters -->
    <div class="flex gap-2 mb-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search orders..."
        class="border p-2 rounded w-full"
      />
      <select v-model="selectedStatus" class="border p-2 rounded">
        <option>All Statuses</option>
        <option>On Track</option>
        <option>Delayed</option>
      </select>
      <select v-model="selectedLine" class="border p-2 rounded">
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
          <td class="border p-2">{{ order.id }}</td>
          <td class="border p-2">{{ order.product }}</td>
          <td class="border p-2">{{ order.quantity }}</td>
          <td class="border p-2">
            <span class="px-2 py-1 rounded" :class="getStatusClass2(order.status)">
              {{ order.status }}
            </span>
          </td>
          <td class="border p-2">
            <input type="date" v-model="order.startDate" class="border p-1 rounded w-full" />
          </td>
          <td class="border p-2">
            <input type="date" v-model="order.endDate" class="border p-1 rounded w-full" />
          </td>
          <td class="border p-2">{{ order.productionLine }}</td>
          <td class="border p-2">
            <span :class="getPriorityClass(order.priority)">
              ● {{ order.priority }}
            </span>
          </td>
          <td class="border p-2">
            <button
              @click="openReschedule(order)"
              class="bg-blue-600 text-white px-3 py-1 rounded"
            >
              Reschedule
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>  </Popup>

  <Popup :visible="showWorkCenterPopup3" @update:visible="showWorkCenterPopup3 = $event">
    <div>
      <h3 class="flex justify-center text-2xl font-extrabold">Create New Workstation</h3>
    </div>
    <div>
      <div class="flex flex-col gap-2">
        <label for=""> Workstation Name</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Workstation Name"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Status</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" name="" id="">
          <optgroup>
            <option value="">Active</option>
            <option value="">Inactive</option>
          </optgroup>
        </select>
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Capacity (Units/Hour)</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Capacity"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Description</label>
        <textarea
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          name=""
          id=""
          placeholder="Enter Workstation Description"
        ></textarea>
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Assign Machines</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" name="" id="">
          <optgroup>
            <option value="">Select</option>
          </optgroup>
        </select>
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Assign Tools</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" name="" id="">
          <optgroup>
            <option value="">Select</option>
          </optgroup>
        </select>
      </div>
      <button class="mt-4 w-full cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white">
        Create Workstation
      </button>
    </div>
  </Popup>
  <Popup :visible="showViewWorkStationPopup" @update:visible="showViewWorkStationPopup = $event">
    <div>
      <h3 class="flex justify-center text-2xl font-extrabold">Workstation Details</h3>
    </div>
    <div>
      <div class="flex flex-col gap-2">
        <label for=""> Workstation Name</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Workstation Name"
          disabled
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Status</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" name="" id="">
          <optgroup>
            <option value="">Active</option>
            <option value="">Inactive</option>
          </optgroup>
        </select>
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Capacity (Units/Hour)</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Capacity"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Description</label>
        <textarea
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          name=""
          id=""
          placeholder="Enter Workstation Description"
        ></textarea>
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Assign Machines</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" name="" id="">
          <optgroup>
            <option value="">Select</option>
          </optgroup>
        </select>
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Assign Tools</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" name="" id="">
          <optgroup>
            <option value="">Select</option>
          </optgroup>
        </select>
      </div>
    </div>
  </Popup>
  <Popup :visible="showEditWorkStationPopup" @update:visible="showEditWorkStationPopup = $event">
    <div>
      <h3 class="flex justify-center text-2xl font-extrabold">Edit Workstation</h3>
    </div>
    <div>
      <div class="flex flex-col gap-2">
        <label for=""> Workstation Id</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Workstation Name"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Workstation Name</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Workstation Name"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Associated Workcenter</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" name="" id="">
          <optgroup>
            <option value="">Active</option>
            <option value="">Inactive</option>
          </optgroup>
        </select>
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Status</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" name="" id="">
          <optgroup>
            <option value="">Active</option>
            <option value="">Inactive</option>
          </optgroup>
        </select>
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Workstation Capacity</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Capacity"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Workstation Description</label>
        <textarea
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          name=""
          id=""
          placeholder="Enter Workstation Description"
        ></textarea>
      </div>
      <div class="flex flex-col gap-2">
        <h4>Machines</h4>
        <table class="mt-2.5 w-full border-collapse">
          <thead>
            <tr class="text-white">
              <th class="bg-blue-600">Machine Id</th>
              <th class="bg-blue-600">Machine Name</th>
              <th class="bg-blue-600">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(station, index) in workstations" :key="index">
              <td>{{ station.name }}</td>
              <td>{{ station.status }}</td>
              <td>
                <button
                  @click="showEditWorkStationPopup = true"
                  class="m-2 mt-4 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
                >
                  Edit
                </button>
                <button class="m-2 mt-4 cursor-pointer rounded-lg bg-red-600 p-1.5 text-white">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <button class="mt-4 w-full cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white">
          Add a Machine
        </button>
      </div>
    </div>
    <div class="flex flex-col gap-2">
      <h4>Tools</h4>
      <table class="mt-2.5 w-full border-collapse">
        <thead>
          <tr class="text-white">
            <th class="bg-blue-600">Tool Id</th>
            <th class="bg-blue-600">Tool Name</th>
            <th class="bg-blue-600">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(station, index) in workstations" :key="index">
            <td>{{ station.name }}</td>
            <td>{{ station.status }}</td>
            <td>
              <button
                @click="showEditWorkStationPopup = true"
                class="m-2 mt-4 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
              >
                Edit
              </button>
              <button class="m-2 mt-4 cursor-pointer rounded-lg bg-red-600 p-1.5 text-white">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <button class="mt-4 w-full cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white">
        Add a Tool
      </button>
      <button class="mt-4 w-full cursor-pointer rounded-lg bg-green-600 p-1.5 text-white">
        Save Changes
      </button>
    </div>
  </Popup>

  <Popup
    :visible="showRealTimePerformancePopup"
    @update:visible="showRealTimePerformancePopup = $event"
  >
    <div class="flex flex-col">
      <h2 class="flex justify-center text-3xl font-extrabold">
        Workcenter and Workstation Monitoring
      </h2>

      <div class="flex flex-col">
        <h3 class="flex justify-start py-2 text-lg font-bold">Real-Time Workcenter Performance</h3>
        <label class="py-1 text-gray-500" for="workcenter">Select Workcenter:</label>
        <select
          class="rounded-lg border-2 border-gray-400 p-0.5"
          id="workcenter"
          v-model="selectedWorkcenter"
        >
          <option>Workcenter 1</option>
          <option>Workcenter 2</option>
        </select>

        <div class="flex justify-between py-4">
          <div class="w-64 rounded-xl bg-gray-100 p-2.5 text-center">
            <strong>Efficiency</strong>
            <p class="text-[#0000ff]">85%</p>
          </div>
          <div class="w-64 rounded-xl bg-gray-100 p-2.5 text-center">
            <strong>Downtime</strong>
            <p class="text-[#0000ff]">1h 15m</p>
          </div>
          <div class="w-64 rounded-xl bg-gray-100 p-2.5 text-center">
            <strong>Task Progress</strong>
            <p class="text-[#0000ff]">65%</p>
          </div>
        </div>
      </div>

      <div class="mt-2">
        <h3 class="flex justify-start py-1 text-lg font-bold">
          Real-Time Workstation Availability
        </h3>
        <h3 class="flex justify-start py-1 text-gray-500">Filter by Workcenter or Location:</h3>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Search by Workcenter or Location"
        />

        <table class="mt-2.5 w-full border-collapse">
          <thead>
            <tr>
              <th class="bg-gray-200">Workstation</th>
              <th class="bg-gray-200">Status</th>
              <th class="bg-gray-200">Current Task</th>
              <th class="bg-gray-200">Upcoming Schedule</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(station, index) in workstationss" :key="index">
              <td>{{ station.name }}</td>
              <td :class="getStatusClass(station.status)">{{ station.status }}</td>
              <td>{{ station.task }}</td>
              <td>{{ station.time }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Popup>

  <Popup :visible="showMaintenancePopup" @update:visible="showMaintenancePopup = $event">
    <div class="flex flex-col gap-2">
      <p class="flex justify-center text-2xl font-extrabold">Schedule Workstation Maintenance</p>
      <label for=""> Select Workcenter</label>
      <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" name="" id="">
        <optgroup>
          <option value="">Active</option>
          <option value="">Inactive</option>
        </optgroup>
      </select>
    </div>
    <div class="flex flex-col gap-2">
      <label for=""> Select Workstation</label>
      <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" name="" id="">
        <optgroup>
          <option value="">Active</option>
          <option value="">Inactive</option>
        </optgroup>
      </select>
    </div>
    <div class="flex flex-col gap-2">
      <label for="">Maintenance Date</label>
      <input
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        type="date"
        name=""
        id=""
      />
    </div>
    <div class="flex flex-col gap-2">
      <label for="">Maintenance Time</label>
      <input
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        type="time"
        name=""
        id=""
      />
    </div>
    <div class="flex flex-col gap-2">
      <label for="">Recurrence</label>
      <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" name="" id="">
        <optgroup>
          <option value="">None</option>
        </optgroup>
      </select>
    </div>
    <div class="flex flex-col gap-2">
      <label for="">Maintenance Description</label>
      <textarea
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        name=""
        id=""
        placeholder="Provide details about the maintenance task"
      ></textarea>
    </div>
    <div class="flex flex-col gap-2">
      <label for="">Assign Maintenance Staff</label>
      <input
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        type="text"
        placeholder="Enter staff names or roles"
      />
    </div>
    <button class="mt-4 w-full cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white">
      Schedule Maintenance
    </button>
  </Popup>

  <Popup :visible="showCreateWorkCenterPopup" @update:visible="showCreateWorkCenterPopup = $event">
    <div class="flex flex-col gap-2">
      <p class="flex justify-center text-2xl font-extrabold">Create New Workcenter</p>
      <label for=""> Workcenter Name</label>
      <input
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        type="text"
        placeholder="Enter Workcenter Name"
      />
    </div>
    <div class="flex flex-col gap-2">
      <label for=""> Workcenter Code</label>
      <input
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        type="text"
        placeholder="Enter Workcenter Code"
      />
    </div>
    <div class="flex flex-col gap-2">
      <label for="">Location</label>
      <textarea
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        name=""
        id=""
        placeholder="Enter Workcenter Location"
      ></textarea>
    </div>
    <div class="flex flex-col gap-2">
      <label for=""> Status</label>
      <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" name="" id="">
        <optgroup>
          <option value="">Active</option>
          <option value="">Inactive</option>
        </optgroup>
      </select>
    </div>
    <div class="flex flex-col gap-2">
      <label for="">Remarks</label>
      <textarea
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        name=""
        id=""
        placeholder="Enter Additional Details (Optional)"
      ></textarea>
    </div>
    <button class="mt-4 w-full cursor-pointer rounded-lg bg-green-600 p-1.5 text-white">
      Create Workcenter
    </button>
  </Popup>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Popup from '@/components/popup.vue'

const selectedWorkcenter = ref('Workcenter 1')

const showWorkCenterPopup = ref(false)
const showWorkCenterPopup2 = ref(false)
const showWorkCenterPopup3 = ref(false)
const showViewWorkStationPopup = ref(false)
const showEditWorkStationPopup = ref(false)
const showRealTimePerformancePopup = ref(false)
const showMaintenancePopup = ref(false)
const showCreateWorkCenterPopup = ref(false)

const workCenters = ref([
  { name: 'Workcenter A', type: 'Type 1', location: 'Location 1', status: 'Active' },
  { name: 'Workcenter B', type: 'Type 2', location: 'Location 2', status: 'Inactive' },
  { name: 'Workcenter C', type: 'Type 3', location: 'Location 3', status: 'Active' },
  { name: 'Workcenter D', type: 'Type 4', location: 'Location 4', status: 'Active' },
  { name: 'Workcenter E', type: 'Type 5', location: 'Location 5', status: 'Inactive' },
  { name: 'Workcenter F', type: 'Type 6', location: 'Location 6', status: 'Active' },
])

const workstations = ref([
  {
    id: 1,
    name: 'Workstation 1',
    status: 'Active',
    output: '50 Units/Hour',
    task: 'Assembling Component A',
  },
  {
    id: 2,
    name: 'Workstation 2',
    status: 'Idle',
    output: '-',
    task: 'No Task Assigned',
  },
  {
    id: 3,
    name: 'Workstation 3',
    status: 'Under Maintenance',
    output: '-',
    task: 'Repair in Progress',
  },
])

interface Workstation {
  name: string
  status: 'Active' | 'Idle' | 'Under Maintenance'
  task: string
  time: string
}

const workstationss: Workstation[] = [
  {
    name: 'Workstation 1',
    status: 'Active',
    task: 'Assembling Unit A',
    time: '10:00 AM - 12:00 PM',
  },
  {
    name: 'Workstation 2',
    status: 'Idle',
    task: '-',
    time: '12:30 PM - 2:00 PM',
  },
  {
    name: 'Workstation 3',
    status: 'Under Maintenance',
    task: '-',
    time: '2:00 PM - 4:00 PM',
  },
  {
    name: 'Workstation 3',
    status: 'Under Maintenance',
    task: '-',
    time: '2:00 PM - 4:00 PM',
  },
]

function getStatusClass(status: string): string {
  switch (status) {
    case 'Active':
      return 'text-green-500'
    case 'Idle':
      return 'text-orange-300'
    case 'Under Maintenance':
      return 'text-red-500'
    default:
      return 'text-gray-500'
  }
}


interface Order {
  id: string;
  product: string;
  quantity: number;
  status: "On Track" | "Delayed";
  startDate: string;
  endDate: string;
  productionLine: string;
  priority: "High" | "Low";
}

const orders = ref<Order[]>([
  {
    id: "#1234",
    product: "Product A",
    quantity: 500,
    status: "On Track",
    startDate: "2024-03-15",
    endDate: "2024-03-20",
    productionLine: "Line 1",
    priority: "High",
  },
  {
    id: "#1235",
    product: "Product B",
    quantity: 1000,
    status: "Delayed",
    startDate: "2024-03-18",
    endDate: "2024-03-22",
    productionLine: "Line 2",
    priority: "Low",
  },
]);

const searchQuery = ref("");
const selectedStatus = ref("All Statuses");
const selectedLine = ref("All Lines");

const filteredOrders = computed(() => {
  return orders.value.filter((order) => {
    return (
      (selectedStatus.value === "All Statuses" || order.status === selectedStatus.value) &&
      (selectedLine.value === "All Lines" || order.productionLine === selectedLine.value) &&
      order.product.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  });
});

const getStatusClass2 = (status: string) => {
  return status === "On Track" ? "bg-green-200 text-green-700" : "bg-red-200 text-red-700";
};

const getPriorityClass = (priority: string) => {
  return priority === "High" ? "text-red-600" : "text-blue-600";
};

const emit = defineEmits(["openReschedulePopup"]);

const openReschedule = (order: Order) => {
  emit("openReschedulePopup", order);
};
</script>

<style scoped>
th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
</style>
