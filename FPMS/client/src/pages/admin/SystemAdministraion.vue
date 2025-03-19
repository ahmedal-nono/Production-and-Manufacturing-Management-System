<template>
  <!-- <div class="flex flex-col m-2 p-4 justify-center rounded-2xl bg-gray-200">
      <p class="text-xl font-bold flex justify-center">System Administration</p>
      <div class="flex flex-row py-4 gap-20">
        <div class="flex flex-col bg-gray-100 rounded-lg p-2 w-3/6">
          <p class="font-bold">System Performance Monitoring</p>
          <div class="flex flex-col font-bold text-[13px] pt-2 space-y-1">
            <p>Server Load: <span>75%</span></p>
            <p>Response Time: <span>120ms</span></p>
            <p>Errors: <span>3 errors</span></p>
            <p>CPU Usage: <span>65%</span></p>
            <p>Memory Usage: <span>80%</span></p>
            <p>Disk Space: <span>90 / 120GB</span></p>
          </div>
        </div>
        <div class="flex flex-col bg-gray-100 rounded-lg p-2">
          <p class="font-bold">User Activity Tracking</p>
          <div class="flex flex-col font-bold pt-2 space-y-1">
            <p>Activity Log</p>
            <button class="bg-green-600 h-fit w-fit p-2 rounded-md font-normal text-white" @click="showActivityLogPopup = true">View Full Activity Log</button>
            <p>Last Login Information</p>
            <span>Last Login: 11/24/2024, 10:30 AM</span>
            <p>Your Last Login</p>
            <span>Last Login: 11/24/2024, 09:45 AM</span>
          </div>
        </div>
      </div>
      <div class="flex flex-col items-center bg-[#bee8ea] border rounded-xl w-fit p-6 cursor-pointer shadow-md shadow-gray-500" @click="showUserMngtPopup = true">
        <img src="../assets/user_manage.png" class="size-20" alt="" />
        <p class="font-bold text-[13px] pt-2">User Management</p>
      </div>
      <div class="flex justify-end gap-10 py-2">
        <div class="flex flex-col items-center justify-evenly bg-[#bee8ea] border rounded-xl w-fit p-2 cursor-pointer shadow-md shadow-gray-500" @click="showLanguageTimezonePopup = true">
          <img src="../assets/settings.png" class="size-12" alt="" />
          <p class="font-bold text-[13px] pt-2">Language & Time</p>
        </div>
        <div class="flex flex-col items-center justify-evenly bg-[#bee8ea] border rounded-xl w-fit p-2 cursor-pointer shadow-md shadow-gray-500" @click="showBackupPopup = true">
          <img src="../assets/backup.png" class="size-12" alt="" />
          <p class="font-bold text-[13px] pt-2">Backup & Restore</p>
        </div>
      </div>
    </div> -->

  <Popup
    :visible="showActivityLogPopup"
    @update:visible="showActivityLogPopup = $event"
  >
    <div>
      <h3 class="font-bold text-xl mb-4">Filter Activity Log</h3>
      <h5 class="font-bold text-sm my-2">Start Date</h5>
      <input type="date" name="" id="" class="border-2 rounded-md p-1 w-full" />
      <h5 class="font-bold text-sm my-2">End Date</h5>
      <input type="date" name="" id="" class="border-2 rounded-md p-1 w-full" />
      <h5 class="font-bold text-sm my-2">Select User</h5>
      <select name="" id="" class="border-2 rounded-md p-1 w-full mb-2">
        <option value="">All Users</option>
      </select>
    </div>
    <h3 class="font-bold text-xl mb-4">Activity Log</h3>
    <div class="overflow-x-auto">
      <table class="min-w-full table-auto">
        <thead>
          <tr>
            <th class="px-4 py-2">User</th>
            <th class="px-4 py-2">Activity</th>
            <th class="px-4 py-2">Date</th>
            <th class="px-4 py-2">Time</th>
            <th class="px-4 py-2">IP Address</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(activity, index) in userActivities" :key="index">
            <td class="px-4 py-2">{{ activity.user }}</td>
            <td class="px-4 py-2">{{ activity.activity }}</td>
            <td class="px-4 py-2">{{ activity.date }}</td>
            <td class="px-4 py-2">{{ activity.time }}</td>
            <td class="px-4 py-2">{{ activity.ip }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="flex flex-row space-x-4 mt-2 justify-center">
      <button class="bg-blue-600 p-1.5 w-2/12 rounded-lg text-white">
        Prev
      </button>
      <p class="mt-2">Page 1 of 5</p>
      <button class="bg-blue-600 p-1.5 w-2/12 rounded-lg text-white">
        Next
      </button>
    </div>
  </Popup>
  <Popup
    :visible="showUserMngtPopup"
    @update:visible="showUserMngtPopup = $event"
  >
    <h3 class="font-bold text-2xl mb-4 justify-center flex">
      User Account Management
    </h3>
    <div class="flex justify-end">
      <button
        class="bg-blue-600 p-1.5 w-2/12 rounded-lg text-white"
        @click="showUserCrtPopup = true"
      >
        Create User
      </button>
    </div>
    <div>
      <h3 class="font-bold text-lg mb-4">Existing Users</h3>
      <table class="min-w-full table-auto">
        <thead>
          <tr>
            <th class="px-4 py-2">Name</th>
            <th class="px-4 py-2">Email</th>
            <th class="px-4 py-2">Department</th>
            <th class="px-4 py-2">Role</th>
            <th class="px-4 py-2">Status</th>
            <th class="px-4 py-2">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, index) in users" :key="index">
            <td class="px-4 py-2">{{ user.name }}</td>
            <td class="px-4 py-2">{{ user.email }}</td>
            <td class="px-4 py-2">{{ user.department }}</td>
            <td class="px-4 py-2">{{ user.role }}</td>
            <td class="px-4 py-2">{{ user.status }}</td>
            <td class="px-4 py-2 flex gap-2">
              <button class="bg-yellow-500 p-2 rounded-lg text-white">
                Edit
              </button>
              <button class="bg-red-600 p-2 rounded-lg text-white">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </Popup>
  <Popup
    :visible="showUserCrtPopup"
    @update:visible="showUserCrtPopup = $event"
  >
    <h3 class="font-bold text-2xl mb-4 justify-center flex">Create New User</h3>
    <div>
      <form @submit.prevent="createUser" class="space-y-4">
        <div class="flex flex-col">
          <label for="name" class="font-bold text-sm">Full Name</label>
          <input
            type="text"
            id="name"
            v-model="newUser.name"
            placeholder="Enter full name"
            class="p-2 border rounded-md"
            required
          />
        </div>
        <div class="flex flex-col">
          <label for="email" class="font-bold text-sm">Email</label>
          <input
            type="email"
            id="email"
            v-model="newUser.email"
            placeholder="Enter email"
            class="p-2 border rounded-md"
            required
          />
        </div>
        <div class="flex flex-col">
          <label for="department" class="font-bold text-sm"
            >Contact Number</label
          >
          <input
            type="text"
            id="number"
            v-model="newUser.department"
            placeholder="Enter contact number"
            class="p-2 border rounded-md"
            required
          />
        </div>
        <div class="flex flex-col">
          <label for="department" class="font-bold text-sm">Department</label>
          <input
            type="text"
            id="department"
            v-model="newUser.department"
            placeholder="Enter department"
            class="p-2 border rounded-md"
            required
          />
        </div>
        <div class="flex flex-col">
          <label for="role" class="font-bold text-sm">Role</label>
          <select
            id="status"
            v-model="newUser.status"
            class="p-2 border rounded-md"
            required
          >
            <option value="Active">Select a role</option>
          </select>
        </div>
        <div class="flex flex-col">
          <label for="status" class="font-bold text-sm">Status</label>
          <select
            id="status"
            v-model="newUser.status"
            class="p-2 border rounded-md"
            required
          >
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
        </div>
        <div class="flex flex-col">
          <label for="password" class="font-bold text-sm">Password</label>
          <input
            type="password"
            id="password"
            v-model="newUser.password"
            placeholder="Enter password"
            class="p-2 border rounded-md"
            required
          />
        </div>
        <div class="flex justify-end gap-4">
          <button
            type="button"
            class="bg-gray-500 text-white p-2 rounded-lg"
            @click="closePopup"
          >
            Cancel
          </button>
          <button type="submit" class="bg-blue-600 text-white p-2 rounded-lg">
            Create User
          </button>
        </div>
      </form>
    </div>
  </Popup>
  <Popup
    :visible="showLanguageTimezonePopup"
    @update:visible="showLanguageTimezonePopup = $event"
  >
    <h3 class="font-bold text-2xl mb-4 justify-center flex">
      Language & Time Zone Settings
    </h3>
    <div>
      <form @submit.prevent="saveSettings" class="space-y-4">
        <div class="flex flex-col">
          <label for="language" class="font-bold text-sm"
            >Preferred Language</label
          >
          <select
            id="language"
            v-model="settings.language"
            class="p-2 border rounded-md"
            required
          >
            <option value="English">English</option>
            <option value="Arabic">Arabic</option>
          </select>
        </div>

        <div class="flex flex-col">
          <label for="timezone" class="font-bold text-sm">Time Zone</label>
          <select
            id="timezone"
            v-model="settings.timezone"
            class="p-2 border rounded-md"
            required
          >
            <option value="UTC">UTC-12:00</option>
            <option value="GMT">GMT</option>
          </select>
        </div>
        <div class="flex justify-end gap-4">
          <button
            type="submit"
            class="bg-blue-600 text-white p-2 w-full rounded-lg"
          >
            Save Settings
          </button>
        </div>
      </form>
    </div>
  </Popup>
  <Popup :visible="showBackupPopup" @update:visible="showBackupPopup = $event">
    <h3 class="font-bold text-2xl mb-6 text-center">Backup and Restore</h3>

    <!-- Automated Backup Settings -->
    <div class="mb-6 p-4 border rounded-lg bg-gray-100">
      <h4 class="font-bold text-lg mb-4">Automated Backup Settings</h4>
      <div class="mb-4">
        <label for="backup-frequency" class="font-bold text-sm block mb-1"
          >Backup Frequency</label
        >
        <select
          id="backup-frequency"
          v-model="backupSettings.frequency"
          class="p-2 border rounded-md w-full"
        >
          <option value="Daily">Daily</option>
          <option value="Weekly">Weekly</option>
          <option value="Monthly">Monthly</option>
        </select>
      </div>
      <div class="mb-4">
        <label for="backup-time" class="font-bold text-sm block mb-1"
          >Backup Time</label
        >
        <input
          type="time"
          id="backup-time"
          v-model="backupSettings.time"
          class="p-2 border rounded-md w-full"
        />
      </div>
      <button
        @click="saveBackupSettings"
        class="bg-blue-600 text-white px-4 py-2 rounded-lg w-full"
      >
        Save Backup Settings
      </button>
    </div>

    <!-- Restore Data -->
    <div class="mb-6 p-4 border rounded-lg bg-gray-100">
      <h4 class="font-bold text-lg mb-4">Restore Data</h4>
      <div class="mb-4">
        <label for="restore-file" class="font-bold text-sm block mb-1"
          >Select Backup File</label
        >
        <input
          type="file"
          id="restore-file"
          @change="handleFileUpload"
          class="p-2 border rounded-md w-full"
        />
      </div>
      <button
        @click="restoreData"
        class="bg-red-600 text-white px-4 py-2 rounded-lg w-full"
      >
        Restore Data
      </button>
    </div>

    <!-- Backup History -->
    <div class="p-4 border rounded-lg bg-gray-100">
      <h4 class="font-bold text-lg mb-4">Backup History</h4>
      <table class="min-w-full table-auto border-collapse border">
        <thead>
          <tr class="bg-gray-200">
            <th class="px-4 py-2 border">Backup Name</th>
            <th class="px-4 py-2 border">Date</th>
            <th class="px-4 py-2 border">Status</th>
            <th class="px-4 py-2 border">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="backup in backupHistory" :key="backup.name">
            <td class="px-4 py-2 border">{{ backup.name }}</td>
            <td class="px-4 py-2 border">{{ backup.date }}</td>
            <td class="px-4 py-2 border">{{ backup.status }}</td>
            <td class="px-4 py-2 border">
              <button
                class="bg-green-600 w-full text-white px-3 py-1 rounded-lg"
                @click="downloadBackup(backup.name)"
              >
                Download
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </Popup>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Popup from "../components/popup.vue";

const showActivityLogPopup = ref(false);
const showUserMngtPopup = ref(false);

const newUser = ref({
  name: "",
  email: "",
  department: "",
  role: "",
  status: "Active",
  password: "",
});
const userActivities = ref([
  {
    user: "John Doe",
    activity: "Logged In",
    date: "2024-11-24",
    time: "10:30 AM",
    ip: "192.168.1.1",
  },
  {
    user: "Jane Smith",
    activity: "Changed Profile Picture",
    date: "2024-11-24",
    time: "09:45 AM",
    ip: "192.168.1.2",
  },
  {
    user: "John Doe",
    activity: "Updated Settings",
    date: "2024-11-23",
    time: "03:10 PM",
    ip: "192.168.1.3",
  },
]);
</script>
