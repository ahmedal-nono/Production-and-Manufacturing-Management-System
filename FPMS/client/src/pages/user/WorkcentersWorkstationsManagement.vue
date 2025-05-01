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
        <p class="pt-2 text-[13px] font-bold">Performance</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showMaintenanceTablePopup = true"
      >
        <img src="@/assets/maintenance.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Maintenance</p>
      </div>
    </div>
  </div>

  <Popup :visible="showWorkCenterPopup" @update:visible="showWorkCenterPopup = $event">
    <div>
      <h3 class="mb-4 text-center text-2xl font-bold">Work Centers</h3>
      <div class="grid grid-cols-5 gap-6">
        <div
          v-for="(workcenter, index) in workCenters"
          :key="index"
          class="flex w-full cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        >
          <div
            @click="
              () => {
                showWorkCenterId = workcenter.id
                showWorkCenterPopup2 = true
              }
            "
          >
            <p class="font-bold">{{ workcenter.name || 'No Workcenter' }}</p>
            <p>{{ workcenter.remarks || 'N/A' }}</p>
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

    <div class="flex justify-end gap-10 py-2">
      <div
        class="flex w-fit cursor-pointer flex-col items-center justify-evenly rounded-xl border bg-[#bee8ea] p-2 shadow-md shadow-gray-500"
        @click="showCreateWorkCenterPopup = true"
      >
        <img src="@/assets/add.png" class="size-12" alt="" />
      </div>
    </div>
  </Popup>

  <Popup :visible="showWorkCenterPopup2" @update:visible="showWorkCenterPopup2 = $event">
    <div>
      <h3 class="flex justify-center pb-2 text-2xl font-extrabold">Workcenter Details</h3>
      <div>
        <p class="py-2 text-xl font-bold">General Information</p>
        <div class="flex flex-row gap-0.5">
          <p>Name:</p>
          <p>{{ showWorkCenterObject.name }}</p>
        </div>
        <div class="flex flex-row gap-0.5">
          <p>Type:</p>
          <p>{{ showWorkCenterObject.location }}</p>
        </div>
        <div class="flex flex-row gap-0.5">
          <p>Capacity:</p>
          <p>{{ showWorkCenterObject.status }}</p>
        </div>
        <div class="flex flex-row gap-0.5">
          <p>Description:</p>
          <p>{{ showWorkCenterObject.remarks }}</p>
        </div>
      </div>
      <div class="flex flex-col pt-8">
        <h3 class="text-xl font-bold">Workstations</h3>
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr class="">
              <th class="border border-gray-700 px-4 py-2">Workstation</th>
              <th class="border border-gray-700 px-4 py-2">Status</th>
              <th class="border border-gray-700 px-4 py-2">Capacity</th>
              <th class="border border-gray-700 px-4 py-2">Description</th>
              <th class="border border-gray-700 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(station, index) in allWorkstations"
              :key="index"
              class="border border-gray-700 px-4 py-2"
            >
              <td class="border border-gray-700 px-4 py-2">{{ station.name }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ station.status }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ station.capacity }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ station.description }}</td>
              <td class="border border-gray-700 px-4 py-2">
                <button
                  @click="
                    () => {
                      showWorkStationId = station.id
                      showViewWorkStationPopup = true
                    }
                  "
                  class="m-2 mt-4 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
                >
                  View
                </button>
                <button
                  @click="
                    () => {
                      showWorkStationId = station.id
                      showEditWorkStationPopup = true
                    }
                  "
                  class="m-2 mt-4 cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
                >
                  Edit
                </button>
                <button
                  @click="() => deleteWorkStation(station.id)"
                  class="m-2 mt-4 cursor-pointer rounded-lg bg-red-600 p-1.5 text-white"
                >
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
          v-model="newWorkstation.name"
          @change="(e) => (newWorkstation.name = e.target.value)"
          required
          minlength="5"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Status</label>
        <select
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          v-model="newWorkstation.status"
          @change="(e) => (newWorkstation.status = e.target.value)"
          required
        >
          <optgroup>
            <option value="1">Active</option>
            <option value="2">Inactive</option>
          </optgroup>
        </select>
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Capacity (Units/Hour)</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Capacity"
          v-model="newWorkstation.capacity"
          @change="(e) => (newWorkstation.capacity = e.target.value)"
          required
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Description</label>
        <textarea
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          name=""
          id=""
          placeholder="Enter Workstation Description"
          v-model="newWorkstation.description"
          @change="(e) => (newWorkstation.description = e.target.value)"
          required
          minlength="10"
        ></textarea>
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Assign Machines</label>
        <select
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          v-model="newWorkstation.machines"
          @change="(e) => (newWorkstation.machines = e.target.value)"
        >
          <optgroup v-for="(machine, index) in allWorkstations">
            <option>{{ machine.machine }}</option>
          </optgroup>
        </select>
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Assign Tools</label>
        <select
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          v-model="newWorkstation.tools"
          @change="(e) => (newWorkstation.tools = (e.target as HTMLSelectElement).value)"
        >
          <optgroup v-for="(tool, index) in allWorkstations">
            <option>{{ tool.tool }}</option>
          </optgroup>
        </select>
      </div>
      <button
        @click="submitworkst"
        class="mt-4 w-full cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
      >
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
          placeholder="Enter Capacity"
          disabled
          :value="showWorkStationObject.name"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Status</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" disabled>
          <optgroup>
            <option>Active</option>
            <option>Inactive</option>
          </optgroup>
        </select>
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Capacity (Units/Hour)</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Capacity"
          disabled
          :value="showWorkStationObject.capacity"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Description</label>
        <textarea
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          name=""
          id=""
          placeholder="Enter Workstation Description"
          disabled
          :value="showWorkStationObject.description"
        ></textarea>
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Assign Machines</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" disabled>
          <optgroup v-for="(machine, index) in allWorkstations">
            <option>{{ machine.machine }}</option>
          </optgroup>
        </select>
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Assign Tools</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" disabled>
          <optgroup v-for="(tool, index) in allWorkstations">
            <option>{{ tool.tool }}</option>
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
          placeholder="Enter Workstation Id"
          v-model="showWorkStationObject.name"
          @change="(e) => (showWorkStationObject.name = e.target.value)"
          required
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Workstation Name</label>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Enter Workstation Name"
          v-model="showWorkStationObject.name"
          @change="(e) => (showWorkStationObject.name = e.target.value)"
          required
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Associated Workcenter</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" required>
          <optgroup v-for="(workcenter, index) in workCenters">
            <option value="">{{ workcenter.name }}</option>
          </optgroup>
        </select>
      </div>
      <div class="flex flex-col gap-2">
        <label for=""> Status</label>
        <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" required>
          <optgroup>
            <option>Active</option>
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
          v-model="showWorkStationObject.capacity"
          @change="(e) => (showWorkStationObject.capacity = e.target.value)"
          required
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="">Workstation Description</label>
        <textarea
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          name=""
          id=""
          placeholder="Enter Workstation Description"
          v-model="showWorkStationObject.description"
          @change="(e) => (showWorkStationObject.description = e.target.value)"
          required
          minlength="10"
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
            <tr v-for="(station, index) in allWorkstations" :key="index">
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
      <button
        @click="() => updateWorkStation(showWorkStationObject.id)"
        class="mt-4 w-full cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
      >
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
        <h3 class="flex justify-start py-2 text-lg font-bold">Workcenter Performance</h3>
        <label class="py-1 text-gray-500" for="workcenter">Select Workcenter:</label>
        <select
          v-model="currentWorkCentersNames"
          @change="(e) => (currentWorkCentersNames = e.target.value)"
          class="rounded-lg border-2 border-gray-400 p-0.5"
        >
          <option v-for="(n, index) in workCentersNames" :value="n" :key="index">
            {{ n.name || n }}
            <!-- Handle both objects and strings -->
          </option>
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
        <h3 class="flex justify-start py-1 text-lg font-bold">Workstation Availability</h3>
        <h3 class="flex justify-start py-1 text-gray-500">Filter by Workstation or Location:</h3>
        <input
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          type="text"
          placeholder="Search by Workstation or Location"
        />

        <table class="w-full">
          <thead class="bg-blue-500 text-white">
            <tr class="">
              <th class="border border-gray-700 px-4 py-2">Workstation</th>
              <th class="border border-gray-700 px-4 py-2">Status</th>
              <th class="border border-gray-700 px-4 py-2">Capacity</th>
              <th class="border border-gray-700 px-4 py-2">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(station, index) in allWorkstations"
              class="border border-gray-700 px-4 py-2"
            >
              <td class="border border-gray-700 px-4 py-2">{{ station.name }}</td>
              <td class="border border-gray-700 px-4 py-2" :class="getStatusClass(station.status)">
                {{ station.status }}
              </td>
              <td class="border border-gray-700 px-4 py-2">{{ station.capacity }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ station.description }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Popup>

  <Popup :visible="showCreateWorkCenterPopup" @update:visible="showCreateWorkCenterPopup = $event">
    <div class="flex flex-col gap-2">
      <p class="flex justify-center text-2xl font-extrabold">Create New Workcenter</p>
      <label for=""> Workcenter Name</label>
      <input
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        type="text"
        placeholder="Enter Workcenter Name"
        v-model="newWorkCenter.name"
        @change="(e) => (newWorkCenter.name = e.target.value)"
        required
        minlength="5"
      />
    </div>
    <div class="flex flex-col gap-2">
      <label for=""> Workcenter Code</label>
      <input
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        type="text"
        placeholder="Enter Workcenter Code"
        v-model="newWorkCenter.code"
        @change="(e) => (newWorkCenter.code = e.target.value)"
        required
        minlength="1"
      />
    </div>
    <div class="flex flex-col gap-2">
      <label for="">Location</label>
      <textarea
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        name=""
        id=""
        placeholder="Enter Workcenter Location"
        v-model="newWorkCenter.location"
        @change="(e) => (newWorkCenter.location = e.target.value)"
        required
        minlength="5"
      ></textarea>
    </div>
    <div class="flex flex-col gap-2">
      <label for="">Status</label>
      <select
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        v-model="newWorkCenter.status"
        @change="(e) => (newWorkCenter.status = e.target.value)"
        required
      >
        <optgroup>
          <option>Active</option>
          <option>Inactive</option>
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
        v-model="newWorkCenter.remarks"
        @change="(e) => (newWorkCenter.remarks = e.target.value)"
        required
        minlength="5"
      ></textarea>
    </div>
    <button
      @click="CreateWorkCenter"
      class="mt-4 w-full cursor-pointer rounded-lg bg-green-600 p-1.5 text-white"
    >
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
          name=""
          class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
          id=""
          placeholder="Enter Tool Description"
        ></textarea>
      </div>
    </div>
    <button class="mt-4 w-full cursor-pointer rounded-lg bg-green-600 p-1.5 text-white">
      Save Changes
    </button>
  </Popup>
  <Popup :visible="showMaintenanceTablePopup" @update:visible="showMaintenanceTablePopup = $event">
    <div class="">
      <div class="flex flex-row justify-between">
        <h2 class="mb-4 text-2xl font-semibold">Maintenances</h2>
        <button
          @click="showCreateMaintenancePopup = true"
          class="j my-2 w-fit cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
        >
          New Issue
        </button>
      </div>
      <!-- Table -->
      <table class="w-full text-center">
        <thead class="bg-blue-500 text-white">
          <tr>
            <th class="border border-gray-700 px-4 py-2">Workstation ID</th>
            <th class="border border-gray-700 px-4 py-2">Maintenance Date</th>
            <th class="border border-gray-700 px-4 py-2">Maintenance Time</th>
            <th class="border border-gray-700 px-4 py-2">Recurrence</th>
            <th class="border border-gray-700 px-4 py-2">Description</th>
            <th class="border border-gray-700 px-4 py-2">Staff Notes</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(main, index) in allMaintenances">
            <td class="border border-gray-700 px-4 py-2">
              {{ main.workstation }}
            </td>
            <td class="border border-gray-700 px-4 py-2">{{ main.maintenance_date }}</td>
            <td class="border border-gray-700 px-4 py-2">{{ main.maintenance_time }}</td>
            <td class="border border-gray-700 px-4 py-2">{{ main.recurrence }}</td>
            <td class="border border-gray-700 px-4 py-2">{{ main.description }}</td>
            <td class="border border-gray-700 px-4 py-2">
              {{ main.staff_notes }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </Popup>

  <Popup
    :visible="showCreateMaintenancePopup"
    @update:visible="showCreateMaintenancePopup = $event"
  >
    <!-- <div class="flex flex-col gap-2">
       <p class="flex justify-center text-2xl font-extrabold">Schedule Workstation Maintenance</p>
      <label for=""> Select Workcenter</label>
      <select class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5" >
        <optgroup v-for ="(workcenter,index) in workCenters">
          <option>{{workcenter.name}}</option>

        </optgroup>
      </select>
    </div> -->
    <div class="flex flex-col gap-2">
      <p class="flex justify-center text-2xl font-extrabold">Schedule a Maintenance</p>
      <label for=""> Select Workstation</label>
      <select
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        v-model="newSchedule.workstation"
        @change="(e) => (newSchedule.workstation = e.target.value)"
        required
      >
        <optgroup v-for="(workstation, index) in allWorkstations">
          <option>{{ workstation.id }}</option>
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
        v-model="newSchedule.maintenance_date"
        @change="(e) => (newSchedule.maintenance_date = e.target.value)"
        required
      />
    </div>
    <div class="flex flex-col gap-2">
      <label for="">Maintenance Time</label>
      <input
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        type="time"
        name=""
        id=""
        v-model="newSchedule.maintenance_time"
        @change="(e) => (newSchedule.maintenance_time = e.target.value)"
        required
      />
    </div>
    <div class="flex flex-col gap-2">
      <label for="">Recurrence</label>
      <select
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        v-model="newSchedule.recurrence"
        @change="(e) => (newSchedule.recurrence = e.target.value)"
        required
      >
        <optgroup>
          <option>None</option>
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
        v-model="newSchedule.description"
        @change="(e) => (newSchedule.description = e.target.value)"
        required
      ></textarea>
    </div>
    <div class="flex flex-col gap-2">
      <label for="">Assign Maintenance Staff</label>
      <input
        class="mb-2.5 w-full rounded-lg border-2 border-gray-400 p-1.5"
        type="text"
        placeholder="Enter staff names or roles"
        v-model="newSchedule.staff_notes"
        @change="(e) => (newSchedule.staff_notes = e.target.value)"
        required
      />
    </div>
    <button
      @click="scheduleMaintenance"
      class="mt-4 w-full cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
    >
      Schedule Maintenance
    </button>
  </Popup>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import Popup from '@/components/popup.vue'
import { baseApiUrl } from '@/api.ts'
import { useAxios } from '@vueuse/integrations/useAxios'

const showWorkCenterId = ref(0)
const showWorkCenterObject = computed(() =>
  workCenters.value.find((w: any) => w.id === showWorkCenterId.value),
)

const showWorkStationId = ref(0)
const showWorkStationObject = computed(() =>
  allWorkstations.value.find((w: any) => w.id === showWorkStationId.value),
)

const showWorkCenterPopup = ref(false)
const showWorkCenterPopup2 = ref(false)
const showAddWorkstationPopup = ref(false)
const showViewWorkStationPopup = ref(false)
const showEditWorkStationPopup = ref(false)
const showRealTimePerformancePopup = ref(false)

const showCreateWorkCenterPopup = ref(false)
const showEditMachinePopup = ref(false)
const showAddMachinePopup = ref(false)
const showEditToolPopup = ref(false)
const showAddToolPopup = ref(false)

const showMaintenanceTablePopup = ref(false)
const showCreateMaintenancePopup = ref(false)

interface Workstation {
  name: string
  status: 'Active' | 'Idle' | 'Under Maintenance'
  task: string
  time: string
}
const currentWorkCentersNames = defineModel('currentWorkCentersNames', { default: '' })
const { data: workCenters } = useAxios(`${baseApiUrl}/workcentre/workcenters/`, { method: 'GET' })
const { data: allWorkstations } = useAxios(`${baseApiUrl}/workcentre/workstations/`, {
  method: 'GET',
})
const { data: allMaintenances } = useAxios(`${baseApiUrl}/workcentre/maintenances/`, {
  method: 'GET',
})
const workCentersNames = computed(() => {
  if (!workCenters.value) return []
  return workCenters.value.map((w) => w.name)
})
const s = computed(() => workCenters.value.find((w) => w.name === currentWorkCentersNames.value))
const workstations = computed(() => {
  if (!allWorkstations.value || !workCenters.value || !s.value) return []
  return allWorkstations.value.filter((ws) => ws.work_center === s.value.id)
})

const newWorkstation = reactive({
  name: '',
  status: '',
  capacity: '',
  description: '',
  work_center: '',
  machines: '',
  tools: '',
})
const newWorkCenter = reactive({
  name: '',
  code: '',
  location: '',
  status: '',
  remarks: '',
})
const newSchedule = reactive({
  workstation: '',
  maintenance_date: '',
  maintenance_time: '',
  recurrence: '',
  description: '',
  staff_notes: '',
})

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

function submitworkst() {
  const { data } = useAxios(`${baseApiUrl}/workcentre/workstations/`, {
    method: 'POST',
    data: newWorkstation,
  })
  //location.reload()
}

function deleteWorkStation(id: number) {
  useAxios(`${baseApiUrl}/workcentre/workstations/${id}/`, { method: 'DELETE' })
}

function updateWorkStation(id: number) {
  useAxios(`${baseApiUrl}/workcentre/workstations/${id}/`, {
    method: 'PUT',
    data: { ...showWorkStationObject.value },
  })
}
function CreateWorkCenter() {
  console.log(newWorkCenter)

  const { data } = useAxios(`${baseApiUrl}/workcentre/workcenters/`, {
    method: 'POST',
    data: newWorkCenter,
  })
  //location.reload()
}
function scheduleMaintenance() {
  useAxios(`${baseApiUrl}/workcentre/maintenances/`, { method: 'POST', data: newSchedule })
  //location.reload()
}
</script>

<style>
button {
  cursor: pointer;
}
</style>
