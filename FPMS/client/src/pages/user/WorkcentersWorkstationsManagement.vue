<template>
  <div class="m-2 flex flex-col justify-center rounded-2xl bg-gray-200 p-4">
    <p class="flex justify-center text-xl font-bold">Workcenters & Workstations Management</p>
    <div class="flex flex-row gap-10 py-4">
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showUserMngtPopup = true"
      >
        <img src="../assets/user_manage.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Work Centers</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showUserMngtPopup = true"
      >
        <img src="../assets/user_manage.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Real-Time Performance</p>
      </div>
      <div
        class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
        @click="showUserMngtPopup = true"
      >
        <img src="../assets/user_manage.png" class="size-20" alt="" />
        <p class="pt-2 text-[13px] font-bold">Maintenance</p>
      </div>
    </div>
    <div class="flex justify-end gap-10 py-2">
      <div
        class="flex w-fit cursor-pointer flex-col items-center justify-evenly rounded-xl border bg-[#bee8ea] p-2 shadow-md shadow-gray-500"
        @click="showBackupPopup = true"
      >
        <img src="../assets/backup.png" class="size-12" alt="" />
        <p class="pt-2 text-[13px] font-bold">Backup & Restore</p>
      </div>
    </div>
  </div>

  <Popup :visible="showActivityLogPopup" @update:visible="showActivityLogPopup = $event">
    <div>
      <h3 class="mb-4 text-xl font-bold">Filter Activity Log</h3>
      <h5 class="my-2 text-sm font-bold">Start Date</h5>
      <input type="date" name="" id="" class="w-full rounded-md border-2 p-1" />
      <h5 class="my-2 text-sm font-bold">End Date</h5>
      <input type="date" name="" id="" class="w-full rounded-md border-2 p-1" />
      <h5 class="my-2 text-sm font-bold">Select User</h5>
      <select name="" id="" class="mb-2 w-full rounded-md border-2 p-1">
        <option value="">All Users</option>
      </select>
    </div>
    <h3 class="mb-4 text-xl font-bold">Activity Log</h3>
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
    <div class="mt-2 flex flex-row justify-center space-x-4">
      <button class="w-2/12 rounded-lg bg-blue-600 p-1.5 text-white">Prev</button>
      <p class="mt-2">Page 1 of 5</p>
      <button class="w-2/12 rounded-lg bg-blue-600 p-1.5 text-white">Next</button>
    </div>
  </Popup>
  <Popup :visible="showUserMngtPopup" @update:visible="showUserMngtPopup = $event">
    <h3 class="mb-4 flex justify-center text-2xl font-bold">User Account Management</h3>
    <div class="flex justify-end">
      <button
        class="w-2/12 rounded-lg bg-blue-600 p-1.5 text-white"
        @click="showUserCrtPopup = true"
      >
        Create User
      </button>
    </div>
    <div>
      <h3 class="mb-4 text-lg font-bold">Existing Users</h3>
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
            <td class="flex gap-2 px-4 py-2">
              <button class="rounded-lg bg-yellow-500 p-2 text-white">Edit</button>
              <button class="rounded-lg bg-red-600 p-2 text-white">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </Popup>
  <Popup :visible="showUserCrtPopup" @update:visible="showUserCrtPopup = $event">
    <h3 class="mb-4 flex justify-center text-2xl font-bold">Create New User</h3>
    <div>
      <form @submit.prevent="createUser" class="space-y-4">
        <div class="flex flex-col">
          <label for="name" class="text-sm font-bold">Full Name</label>
          <input
            type="text"
            id="name"
            v-model="newUser.name"
            placeholder="Enter full name"
            class="rounded-md border p-2"
            required
          />
        </div>
        <div class="flex flex-col">
          <label for="email" class="text-sm font-bold">Email</label>
          <input
            type="email"
            id="email"
            v-model="newUser.email"
            placeholder="Enter email"
            class="rounded-md border p-2"
            required
          />
        </div>
        <div class="flex flex-col">
          <label for="department" class="text-sm font-bold">Contact Number</label>
          <input
            type="text"
            id="number"
            v-model="newUser.department"
            placeholder="Enter contact number"
            class="rounded-md border p-2"
            required
          />
        </div>
        <div class="flex flex-col">
          <label for="department" class="text-sm font-bold">Department</label>
          <input
            type="text"
            id="department"
            v-model="newUser.department"
            placeholder="Enter department"
            class="rounded-md border p-2"
            required
          />
        </div>
        <div class="flex flex-col">
          <label for="role" class="text-sm font-bold">Role</label>
          <select id="status" v-model="newUser.status" class="rounded-md border p-2" required>
            <option value="Active">Select a role</option>
          </select>
        </div>
        <div class="flex flex-col">
          <label for="status" class="text-sm font-bold">Status</label>
          <select id="status" v-model="newUser.status" class="rounded-md border p-2" required>
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
        </div>
        <div class="flex flex-col">
          <label for="password" class="text-sm font-bold">Password</label>
          <input
            type="password"
            id="password"
            v-model="newUser.password"
            placeholder="Enter password"
            class="rounded-md border p-2"
            required
          />
        </div>
        <div class="flex justify-end gap-4">
          <button type="button" class="rounded-lg bg-gray-500 p-2 text-white" @click="closePopup">
            Cancel
          </button>
          <button type="submit" class="rounded-lg bg-blue-600 p-2 text-white">Create User</button>
        </div>
      </form>
    </div>
  </Popup>
  <Popup :visible="showLanguageTimezonePopup" @update:visible="showLanguageTimezonePopup = $event">
    <h3 class="mb-4 flex justify-center text-2xl font-bold">Language & Time Zone Settings</h3>
    <div>
      <form @submit.prevent="saveSettings" class="space-y-4">
        <div class="flex flex-col">
          <label for="language" class="text-sm font-bold">Preferred Language</label>
          <select id="language" v-model="settings.language" class="rounded-md border p-2" required>
            <option value="English">English</option>
            <option value="Arabic">Arabic</option>
          </select>
        </div>

        <div class="flex flex-col">
          <label for="timezone" class="text-sm font-bold">Time Zone</label>
          <select id="timezone" v-model="settings.timezone" class="rounded-md border p-2" required>
            <option value="UTC">UTC-12:00</option>
            <option value="GMT">GMT</option>
          </select>
        </div>
        <div class="flex justify-end gap-4">
          <button type="submit" class="w-full rounded-lg bg-blue-600 p-2 text-white">
            Save Settings
          </button>
        </div>
      </form>
    </div>
  </Popup>
  <Popup :visible="showBackupPopup" @update:visible="showBackupPopup = $event">
    <h3 class="mb-6 text-center text-2xl font-bold">Backup and Restore</h3>

    <!-- Automated Backup Settings -->
    <div class="mb-6 rounded-lg border bg-gray-100 p-4">
      <h4 class="mb-4 text-lg font-bold">Automated Backup Settings</h4>
      <div class="mb-4">
        <label for="backup-frequency" class="mb-1 block text-sm font-bold">Backup Frequency</label>
        <select
          id="backup-frequency"
          v-model="backupSettings.frequency"
          class="w-full rounded-md border p-2"
        >
          <option value="Daily">Daily</option>
          <option value="Weekly">Weekly</option>
          <option value="Monthly">Monthly</option>
        </select>
      </div>
      <div class="mb-4">
        <label for="backup-time" class="mb-1 block text-sm font-bold">Backup Time</label>
        <input
          type="time"
          id="backup-time"
          v-model="backupSettings.time"
          class="w-full rounded-md border p-2"
        />
      </div>
      <button
        @click="saveBackupSettings"
        class="w-full rounded-lg bg-blue-600 px-4 py-2 text-white"
      >
        Save Backup Settings
      </button>
    </div>

    <!-- Restore Data -->
    <div class="mb-6 rounded-lg border bg-gray-100 p-4">
      <h4 class="mb-4 text-lg font-bold">Restore Data</h4>
      <div class="mb-4">
        <label for="restore-file" class="mb-1 block text-sm font-bold">Select Backup File</label>
        <input
          type="file"
          id="restore-file"
          @change="handleFileUpload"
          class="w-full rounded-md border p-2"
        />
      </div>
      <button @click="restoreData" class="w-full rounded-lg bg-red-600 px-4 py-2 text-white">
        Restore Data
      </button>
    </div>

    <!-- Backup History -->
    <div class="rounded-lg border bg-gray-100 p-4">
      <h4 class="mb-4 text-lg font-bold">Backup History</h4>
      <table class="min-w-full table-auto border-collapse border">
        <thead>
          <tr class="bg-gray-200">
            <th class="border px-4 py-2">Backup Name</th>
            <th class="border px-4 py-2">Date</th>
            <th class="border px-4 py-2">Status</th>
            <th class="border px-4 py-2">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="backup in backupHistory" :key="backup.name">
            <td class="border px-4 py-2">{{ backup.name }}</td>
            <td class="border px-4 py-2">{{ backup.date }}</td>
            <td class="border px-4 py-2">{{ backup.status }}</td>
            <td class="border px-4 py-2">
              <button
                class="w-full rounded-lg bg-green-600 px-3 py-1 text-white"
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
import { ref } from 'vue'
import Popup from '@/components/popup.vue'

const showActivityLogPopup = ref(false)
const showUserMngtPopup = ref(false)
const showPopup = ref(false)
const showAvatarPopup = ref(false)
const showUserCrtPopup = ref(false)
const isRead = ref(false)
const isReadSecond = ref(false)
const uploadedImage = ref<string | null>(null)

const userActivities = ref([
  {
    user: 'John Doe',
    activity: 'Logged In',
    date: '2024-11-24',
    time: '10:30 AM',
    ip: '192.168.1.1',
  },
  {
    user: 'Jane Smith',
    activity: 'Changed Profile Picture',
    date: '2024-11-24',
    time: '09:45 AM',
    ip: '192.168.1.2',
  },
  {
    user: 'John Doe',
    activity: 'Updated Settings',
    date: '2024-11-23',
    time: '03:10 PM',
    ip: '192.168.1.3',
  },
])

function markAsRead() {
  isRead.value = true
}

function markAsReadSecond() {
  isReadSecond.value = true
}

function handleImageUpload(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => {
      uploadedImage.value = reader.result as string
    }
    reader.readAsDataURL(file)
  }
}
const newUser = ref({
  name: '',
  email: '',
  department: '',
  role: '',
  status: 'Active',
  password: '',
})

const users = ref([
  {
    name: 'John Doe',
    email: 'john.doe@example.com',
    department: 'Engineering',
    role: 'Admin',
    status: 'Active',
  },
])

const createUser = () => {
  if (
    newUser.value.name &&
    newUser.value.email &&
    newUser.value.department &&
    newUser.value.role &&
    newUser.value.password
  ) {
    users.value.push({ ...newUser.value })

    newUser.value = {
      name: '',
      email: '',
      department: '',
      role: '',
      status: 'Active',
      password: '',
    }

    showUserCrtPopup.value = false
  }
}

const closePopup = () => {
  showUserCrtPopup.value = false
}

const showLanguageTimezonePopup = ref(false)

const settings = ref({
  language: 'English',
  timezone: 'UTC',
})

const saveSettings = () => {
  console.log('Settings Saved:', settings.value)
  showLanguageTimezonePopup.value = false
}
const showBackupPopup = ref(false)

// Backup settings state
const backupSettings = ref({
  frequency: 'Daily',
  time: '',
})

// Backup history data
const backupHistory = ref([
  { name: 'Backup_2024_11_25.zip', date: '25 Nov 2024', status: 'Completed' },
  { name: 'Backup_2024_11_24.zip', date: '24 Nov 2024', status: 'Completed' },
])

const saveBackupSettings = () => {
  console.log('Backup Settings Saved:', backupSettings.value)
}

const handleFileUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    console.log('Selected file for restore:', file.name)
  }
}

const restoreData = () => {
  console.log('Restore data initiated.')
}

const downloadBackup = (fileName: string) => {
  console.log('Downloading backup:', fileName)
}
</script>
