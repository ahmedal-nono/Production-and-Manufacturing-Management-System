<template>
  <div class="m-2 flex flex-col justify-center rounded-2xl bg-gray-200 p-4">
    <p class="flex justify-center text-xl font-bold">System Administration</p>
    <div class="flex flex-row gap-20 py-4">
      <div class="flex w-3/6 flex-col rounded-lg bg-gray-100 p-2">
        <p class="font-bold">System Performance Monitoring</p>
        <div class="flex flex-col space-y-1 pt-2 text-[13px] font-bold">
          <p>Server Load: <span>75%</span></p>
          <p>Response Time: <span>120ms</span></p>
          <p>Errors: <span>3 errors</span></p>
          <p>CPU Usage: <span>65%</span></p>
          <p>Memory Usage: <span>80%</span></p>
          <p>Disk Space: <span>90 / 120GB</span></p>
        </div>
      </div>
      <div class="flex flex-col rounded-lg bg-gray-100 p-2">
        <p class="font-bold">User Activity Tracking</p>
        <div class="flex flex-col space-y-1 pt-2 font-bold">
          <p>Activity Log</p>
          <button
            class="h-fit w-fit cursor-pointer rounded-md bg-green-600 p-2 font-normal text-white"
            @click="showActivityLogPopup = true"
          >
            View Full Activity Log
          </button>
          <p>Last Login Information</p>
          <span>Last Login: 11/24/2024, 10:30 AM</span>
          <p>Your Last Login</p>
          <span>Last Login: 11/24/2024, 09:45 AM</span>
        </div>
      </div>
    </div>
    <div
      class="flex w-fit cursor-pointer flex-col items-center rounded-xl border bg-[#bee8ea] p-6 shadow-md shadow-gray-500"
      @click="showUserMngtPopup = true"
    >
      <img src="@/assets/user_manage.png" class="size-20" alt="" />
      <p class="pt-2 text-[13px] font-bold">User Management</p>
    </div>
    <div class="flex justify-end gap-10 py-2">
      <div
        class="flex w-fit cursor-pointer flex-col items-center justify-evenly rounded-xl border bg-[#bee8ea] p-2 shadow-md shadow-gray-500"
        @click="showBackupPopup = true"
      >
        <img src="@/assets/backup.png" class="size-12" alt="" />
        <p class="pt-2 text-[13px] font-bold">Backup & Restore</p>
      </div>
    </div>

    <!-- Activity Log Popup -->
    <Popup :visible="showActivityLogPopup" @update:visible="showActivityLogPopup = $event">
      <h3 class="mb-4 text-xl font-bold">Activity Log</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr>
              <th class="border border-gray-700 px-4 py-2">User</th>
              <th class="border border-gray-700 px-4 py-2">Activity</th>
              <th class="border border-gray-700 px-4 py-2">Date</th>
              <th class="border border-gray-700 px-4 py-2">Time</th>
              <th class="border border-gray-700 px-4 py-2">IP Address</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(activity, index) in activityLogs" :key="index" class="overflow-y-auto">
              <td class="border border-gray-700 px-4 py-2">{{ activity.user }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ activity.action }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ formatDate(activity.timestamp) }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ formatTime(activity.timestamp) }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ activity.ip_address }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="mt-2 flex flex-row justify-center space-x-4">
        <button
          @click="fetchActivityLogs(currentPage - 1)"
          :disabled="currentPage === 1"
          class="w-2/12 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white disabled:opacity-50"
        >
          Prev
        </button>
        <p class="mt-2">Page {{ currentPage }} of {{ totalPages }}</p>
        <button
          @click="fetchActivityLogs(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="w-2/12 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </Popup>

    <!-- User Management Popup -->
    <Popup :visible="showUserMngtPopup" @update:visible="showUserMngtPopup = $event">
      <h3 class="mb-4 flex justify-center text-2xl font-bold">User Account Management</h3>
      <div class="flex justify-end">
        <button
          class="w-2/12 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
          @click="openCreateUserPopup()"
        >
          Create User
        </button>
      </div>
      <div>
        <h3 class="mb-4 text-lg font-bold">Existing Users</h3>
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr class="">
              <th class="border border-gray-700 px-4 py-2">Name</th>
              <th class="border border-gray-700 px-4 py-2">Email</th>
              <th class="border border-gray-700 px-4 py-2">Department</th>
              <th class="border border-gray-700 px-4 py-2">Role</th>
              <th class="border border-gray-700 px-4 py-2">Status</th>
              <th class="border border-gray-700 px-4 py-2">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(user, index) in users"
              :key="index"
              class="border border-gray-700 text-center"
            >
              <td class="border border-gray-700 px-4 py-2">{{ user.full_name }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ user.email }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ user.department }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ user.role }}</td>
              <td class="border border-gray-700 px-4 py-2">
                {{ user.account_status ? 'Active' : 'Inactive' }}
              </td>
              <td class="flex justify-center gap-2 border border-gray-700 px-4 py-2">
                <button
                  @click="openEditUserPopup(user)"
                  class="cursor-pointer rounded-lg bg-yellow-500 p-2 text-white"
                >
                  Edit
                </button>
                <button
                  @click="deleteUser(user.id)"
                  class="cursor-pointer rounded-lg bg-red-600 p-2 text-white"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Popup>

    <!-- Create User Popup -->
    <Popup :visible="showUserCrtPopup" @update:visible="showUserCrtPopup = $event">
      <h3 class="mb-4 flex justify-center text-2xl font-bold">Create New User</h3>
      <div>
        <form @submit.prevent="submitUserForm" class="space-y-4">
          <div class="flex flex-col">
            <label for="name" class="text-sm font-bold">Full Name</label>
            <input
              type="text"
              id="name"
              v-model="userForm.full_name"
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
              v-model="userForm.email"
              placeholder="Enter email"
              class="rounded-md border p-2"
              required
            />
          </div>
          <div class="flex flex-col">
            <label for="contact" class="text-sm font-bold">Contact Number</label>
            <input
              type="text"
              id="contact"
              v-model="userForm.contact_number"
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
              v-model="userForm.department"
              placeholder="Enter department"
              class="rounded-md border p-2"
              required
            />
          </div>
          <div class="flex flex-col">
            <label for="role" class="text-sm font-bold">Role</label>
            <select id="role" v-model="userForm.role" class="rounded-md border p-2" required>
              <option value="">Select a role</option>
              <option value="quality_control_manager">Quality Control Manager</option>
              <option value="quality_control_inspector">Quality Control Inspector</option>
              <option value="supervisor">Supervisor</option>
              <option value="operator">Operator</option>
              <option value="production_planner">Production Planner</option>
              <option value="production_manager">Production Manager</option>
            </select>
          </div>
          <div class="flex flex-col">
            <label for="status" class="text-sm font-bold">Status</label>
            <select
              id="status"
              v-model="userForm.account_status"
              class="rounded-md border p-2"
              required
            >
              <option :value="true">Active</option>
              <option :value="false">Inactive</option>
            </select>
          </div>
          <div class="flex flex-col">
            <label for="password" class="text-sm font-bold">Password</label>
            <input
              type="password"
              id="password"
              v-model="userForm.password"
              placeholder="Enter password"
              class="rounded-md border p-2"
              :required="!editingUserId"
            />
          </div>
          <div class="flex justify-end gap-4">
            <button type="submit" class="cursor-pointer rounded-lg bg-blue-600 p-2 text-white">
              {{ editingUserId ? 'Update User' : 'Create User' }}
            </button>
          </div>
        </form>
      </div>
    </Popup>

    <!-- Backup Popup -->
    <Popup :visible="showBackupPopup" @update:visible="showBackupPopup = $event">
      <h3 class="mb-6 text-center text-2xl font-bold">Backup</h3>
      <div class="mb-4">
        <button
          @click="createBackup()"
          class="w-full cursor-pointer rounded-lg bg-green-600 p-2 text-white"
        >
          Create New Backup
        </button>
      </div>
      <div class="">
        <h4 class="mb-4 text-lg font-bold">Backup History</h4>
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr class="">
              <th class="border border-gray-700 px-4 py-2">Backup Name</th>
              <th class="border border-gray-700 px-4 py-2">Date</th>
              <th class="border border-gray-700 px-4 py-2">Status</th>
              <th class="border border-gray-700 px-4 py-2">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="backup in backups" :key="backup.name">
              <td class="border border-gray-700 px-4 py-2">{{ backup.name }}</td>
              <td class="border border-gray-700 px-4 py-2">
                {{ formatDateTime(backup.created_at) }}
              </td>
              <td class="border border-gray-700 px-4 py-2">{{ backup.status }}</td>
              <td class="border border-gray-700 px-4 py-2">
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
      <div class="mt-4">
        <h4 class="mb-2 text-lg font-bold">Restore Backup</h4>
        <input type="file" @change="handleFileUpload" class="mb-2 w-full rounded-md border p-2" />
        <button
          @click="restoreBackup()"
          :disabled="!selectedBackupFile"
          class="w-full cursor-pointer rounded-lg bg-blue-600 p-2 text-white disabled:opacity-50"
        >
          Restore
        </button>
      </div>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAxios } from '@vueuse/integrations/useAxios'
import Popup from '@/components/popup.vue'
import { useUserStore } from '@/stores/user'

// Types
interface User {
  id: number
  full_name: string
  email: string
  contact_number: string
  department: string
  role: string
  account_status: boolean
}

interface ActivityLog {
  id: number
  user: string
  action: string
  timestamp: string
  ip_address: string
}

interface Backup {
  id: number
  name: string
  created_at: string
  status: string
}

// Store
const userStore = useUserStore()

// State
const showActivityLogPopup = ref(false)
const showUserMngtPopup = ref(false)
const showUserCrtPopup = ref(false)
const showBackupPopup = ref(false)

const users = ref<User[]>([])
const activityLogs = ref<ActivityLog[]>([])
const backups = ref<Backup[]>([])
const selectedBackupFile = ref<File | null>(null)

const currentPage = ref(1)
const totalPages = ref(1)

const editingUserId = ref<number | null>(null)
const userForm = ref({
  full_name: '',
  email: '',
  contact_number: '',
  department: '',
  account_status: true,
  role: '',
  password: '',
})

// API Configuration
const baseURL = 'http://localhost:8000/api/admin'

// Formatting functions
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const formatTime = (dateString: string) => {
  return new Date(dateString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const formatDateTime = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

  
// API Functions
const fetchUsers = async () => {
  const { data } = await useAxios(`${baseURL}/users/`, { method: 'GET' })
  users.value = data.value || []
}

const fetchActivityLogs = async (page = 1) => {
  const { data } = await useAxios(`${baseURL}/activity-logs/?page=${page}`, { method: 'GET' })
  if (data.value) {
    activityLogs.value = data.value.results
    currentPage.value = page
    totalPages.value = Math.ceil(data.value.count / 10) // Assuming 10 items per page
  }
}

const fetchBackups = async () => {
  const { data } = await useAxios(`${baseURL}/backups/`, { method: 'GET' })
  backups.value = data.value || []
}

const submitUserForm = async () => {
  
  if (editingUserId.value) {
    await updateUser()
  } else {
    await createUser()
  }
}

const createUser = async () => {
  const { error } = await useAxios(`${baseURL}/users/`, {
    method: 'POST',
    data: userForm.value,
  })

  if (!error.value) {
    await fetchUsers()
    showUserCrtPopup.value = false
    resetUserForm()
  }
}

const updateUser = async () => {
  if (!editingUserId.value) return

  const { error } = await useAxios(`${baseURL}/users/${editingUserId.value}/`, {
    method: 'PUT',
    data: userForm.value,
  })

  if (!error.value) {
    await fetchUsers()
    showUserCrtPopup.value = false
    resetUserForm()
  }
}

const deleteUser = async (userId: number) => {
  if (confirm('Are you sure you want to delete this user?')) {
    const { error } = await useAxios(`${baseURL}/users/${userId}/`, {
      method: 'DELETE',
    })

    if (!error.value) {
      await fetchUsers()
    }
  }
}

const createBackup = async () => {
  const { error } = await useAxios(`${baseURL}/backups/`, {
    method: 'POST',
  })

  if (!error.value) {
    await fetchBackups()
  }
}

const downloadBackup = async (backupName: string) => {
  const { data } = await useAxios(`${baseURL}/backups/${backupName}/download/`, {
    method: 'GET',
    responseType: 'blob',
  })

  if (data.value) {
    const url = window.URL.createObjectURL(new Blob([data.value]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', backupName)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

const handleFileUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    selectedBackupFile.value = input.files[0]
  }
}

const restoreBackup = async () => {
  if (!selectedBackupFile.value) return

  const formData = new FormData()
  formData.append('file', selectedBackupFile.value)

  const { error } = await useAxios(`${baseURL}/backups/restore/`, {
    method: 'POST',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  if (!error.value) {
    alert('Backup restored successfully')
    selectedBackupFile.value = null
    await fetchBackups()
  }
}

// Helper functions
const resetUserForm = () => {
  userForm.value = {
    full_name: '',
    email: '',
    contact_number: '',
    department: '',
    role: '',
    account_status: true,
    password: '',
  }
  editingUserId.value = null
}

const openCreateUserPopup = () => {
  resetUserForm()
  showUserCrtPopup.value = true
}

const openEditUserPopup = (user: User) => {
  userForm.value = {
    full_name: user.full_name,
    email: user.email,
    contact_number: user.contact_number,
    department: user.department,
    role: user.role,
    account_status: user.account_status,
    password: '',
  }
  editingUserId.value = user.id
  showUserCrtPopup.value = true
}

// Initialize data
onMounted(() => {
  fetchUsers()
  fetchActivityLogs()
  fetchBackups()
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
