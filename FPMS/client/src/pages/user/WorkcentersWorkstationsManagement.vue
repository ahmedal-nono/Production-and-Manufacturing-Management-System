<template>
  <div class="m-2 flex flex-col justify-center rounded-2xl bg-gray-200 p-4">
    <p class="flex justify-center text-xl font-bold">Workcenters & Workstations Management</p>
    <div class="flex flex-row gap-10 py-4">
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showWorkCenterPopup = true"
      >
        <img src="@/assets/wokrcenter.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">WorkCenters</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showRealTimePerformancePopup = true"
      >
        <img src="@/assets/performance.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Real-Time Performance</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showMaintenancePopup = true"
      >
        <img src="@/assets/maintenance.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Maintenance</p>
      </div>
    </div>
    <div class="flex justify-end gap-10 py-2">
      <div
        class="flex w-fit cursor-pointer flex-col items-center justify-evenly rounded-xl border bg-[#bee8ea] p-2 shadow-md shadow-gray-500"
        @click="showCreateWorkCenterPopup = true"
      >
        <img src="@/assets/add.png" class="size-12" alt="" />
      </div>
    </div>
  </div>

  <Popup :visible="showWorkCenterPopup" @update:visible="showWorkCenterPopup = $event">
    <div>
      <h3 class="mb-4 text-center text-2xl font-bold">Workcenters</h3>
      <div class="grid grid-cols-5 gap-6">
        <div
          v-for="(workcenter, index) in workCenters"
          :key="index"
          class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        >
          <div @click="showWorkCenterPopup2 = true">
            <p class="font-bold">{{ workcenter.name || 'No Workcenter' }}</p>
            <p>{{ workcenter.type || 'N/A' }}</p>
            <p>{{ workcenter.location || 'N/A' }}</p>
            <p
              :class="{
                'text-green-600': workcenter.status === 'Active',
                'text-red-600': workcenter.status !== 'Active',
              }"
            >
              {{ workcenter.status || 'Inactive' }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <p class="flex justify-end text-6xl font-extrabold">+</p>
  </Popup>

  <Popup :visible="showWorkCenterPopup2" @update:visible="showWorkCenterPopup2 = $event">
    <div>
      <h3 class="flex justify-center pb-2 text-2xl font-extrabold">Workcenter Details</h3>
      <div>
        <p class="py-2 text-xl font-bold">General Information</p>
        <div class="flex flex-row gap-0.5">
          <p>Name:</p>
          <p>Ass</p>
        </div>
        <div class="flex flex-row gap-0.5">
          <p>Type:</p>
          <p>Ass</p>
        </div>
        <div class="flex flex-row gap-0.5">
          <p>Capacity:</p>
          <p>Ass</p>
        </div>
        <div class="flex flex-row gap-0.5">
          <p>Description:</p>
          <p>Ass</p>
        </div>
      </div>
      <div class="flex flex-col pt-8">
        <h3 class="text-xl font-bold">Workstations</h3>
        <table class="mt-2.5 w-full border-collapse">
          <thead>
            <tr class="text-white">
              <th class="bg-blue-600">Workstation</th>
              <th class="bg-blue-600">Status</th>
              <th class="bg-blue-600">Capacity</th>
              <th class="bg-blue-600">Current Task</th>
              <th class="bg-blue-600">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(station, index) in workstations" :key="index">
              <td>{{ station.name }}</td>
              <td>{{ station.status }}</td>
              <td>{{ station.output }}</td>
              <td>{{ station.task }}</td>
              <td>
                <button
                  @click="showViewWorkStationPopup = true"
                  class="m-2 mt-4 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
                >
                  View
                </button>
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
      </div>
      <button
        class="mt-4 w-4/12 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
        @click="showAddWorkstationPopup = true"
      >
        Add New Workstation
      </button>
    </div>
  </Popup>

  <Popup :visible="showAddWorkstationPopup" @update:visible="showAddWorkstationPopup = $event">
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
                  @click="showEditMachinePopup = true"
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
        <button
          @click="showAddMachinePopup = true"
          class="mt-4 w-full cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
        >
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
                @click="showEditToolPopup = true"
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
      <button
        @click="showAddToolPopup = true"
        class="mt-4 w-full cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
      >
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
        <select class="rounded-lg border-2 border-gray-400 p-0.5" id="workcenter">
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
  <Popup :visible="showEditMachinePopup" @update:visible="showEditMachinePopup = $event">
    <div>
      <h3 class="flex justify-center text-2xl font-extrabold">Edit Machine</h3>
    </div>
    <div>
      <div class="flex flex-col gap-2">
        <label for=""> Machine Id</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Machine Id"
          disabled
        />
      </div>

      <div class="flex flex-col gap-2">
        <label for="">Machine Name</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Machine Name"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Description</label>
        <textarea
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          name=""
          id=""
          placeholder="Enter Machine Description"
        ></textarea>
      </div>
    </div>
    <button class="mt-4 w-full cursor-pointer rounded-lg bg-green-600 p-1.5 text-white">
      Save Changes
    </button>
  </Popup>
  <Popup :visible="showAddMachinePopup" @update:visible="showAddMachinePopup = $event">
    <div>
      <h3 class="flex justify-center text-2xl font-extrabold">Add a New Machine</h3>
    </div>
    <div>
      <div class="flex flex-col gap-2">
        <label for=""> Machine Id</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Machine Id"
          disabled
        />
      </div>

      <div class="flex flex-col gap-2">
        <label for="">Machine Name</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Machine Name"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Description</label>
        <textarea
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          name=""
          id=""
          placeholder="Enter Machine Description"
        ></textarea>
      </div>
    </div>
    <button class="mt-4 w-full cursor-pointer rounded-lg bg-green-600 p-1.5 text-white">
      Save Changes
    </button>
  </Popup>
  <Popup :visible="showEditToolPopup" @update:visible="showEditToolPopup = $event">
    <div>
      <h3 class="flex justify-center text-2xl font-extrabold">Edit Tool</h3>
    </div>
    <div>
      <div class="flex flex-col gap-2">
        <label for=""> Tool Id</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Tool Id"
          disabled
        />
      </div>

      <div class="flex flex-col gap-2">
        <label for="">Tool Name</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Tool Name"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Description</label>
        <textarea
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          name=""
          id=""
          placeholder="Enter Tool Description"
        ></textarea>
      </div>
    </div>
    <button class="mt-4 w-full cursor-pointer rounded-lg bg-green-600 p-1.5 text-white">
      Save Changes
    </button>
  </Popup>
  <Popup :visible="showAddToolPopup" @update:visible="showAddToolPopup = $event">
    <div>
      <h3 class="flex justify-center text-2xl font-extrabold">Add a New Tool</h3>
    </div>
    <div>
      <div class="flex flex-col gap-2">
        <label for=""> Tool Id</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Tool Id"
          disabled
        />
      </div>

      <div class="flex flex-col gap-2">
        <label for="">Tool Name</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Tool Name"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Description</label>
        <textarea
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          name=""
          id=""
          placeholder="Enter Tool Description"
        ></textarea>
      </div>
    </div>
    <button class="mt-4 w-full cursor-pointer rounded-lg bg-green-600 p-1.5 text-white">
      Save Changes
    </button>
  </Popup>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Popup from '@/components/popup.vue'

const showWorkCenterPopup = ref(false)
const showWorkCenterPopup2 = ref(false)
const showAddWorkstationPopup = ref(false)
const showViewWorkStationPopup = ref(false)
const showEditWorkStationPopup = ref(false)
const showRealTimePerformancePopup = ref(false)
const showMaintenancePopup = ref(false)
const showCreateWorkCenterPopup = ref(false)
const showEditMachinePopup = ref(false)
const showAddMachinePopup = ref(false)
const showEditToolPopup = ref(false)
const showAddToolPopup = ref(false)

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
</script>

<style scoped>
th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
</style>
