<template>
  <div class="m-2 flex flex-col justify-center rounded-2xl bg-gray-200 p-4">
    <p class="flex justify-center text-xl font-bold">System Administration</p>
    <div class="flex flex-row gap-20 py-4">
      <div class="flex w-3/6 flex-col rounded-lg bg-gray-100 p-2">
        <p class="font-bold">System Performance Monitoring</p>
        <div class="flex w-3/6 flex-col rounded-lg bg-gray-100 p-2">
          <div class="flex justify-between">
            <p class="font-bold">System Performance Monitoring</p>
            <button
              @click="fetchHealthMetrics"
              class="text-xs text-blue-600 hover:text-blue-800"
              :disabled="healthLoading"
            >
              {{ healthLoading ? 'Refreshing...' : 'Refresh' }}
            </button>
          </div>
          <div class="flex flex-col space-y-1 pt-2 text-[13px] font-bold">
            <p>
              CPU Usage:
              <span :class="{ 'text-red-500': healthMetrics.cpu_usage > 80 }">
                {{ healthMetrics.cpu_usage }}%
              </span>
            </p>
            <p>
              Memory Usage:
              <span :class="{ 'text-red-500': healthMetrics.memory_usage > 85 }">
                {{ healthMetrics.memory_usage }}%
              </span>
            </p>
            <p>
              Disk Usage:
              <span :class="{ 'text-red-500': healthMetrics.disk_usage > 90 }">
                {{ healthMetrics.disk_usage }}%
              </span>
            </p>
            <p>
              Disk Space:
              <span>{{ healthMetrics.disk_space }} GB available</span>
            </p>
            <p>
              Response Time:
              <span :class="{ 'text-red-500': healthMetrics.response_time > 100 }">
                {{ healthMetrics.response_time }} ms
              </span>
            </p>
            <p class="text-xs text-gray-500">
              Last updated: {{ formatDateTime(healthMetrics.timestamp) }}
            </p>
          </div>
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
      <div class="mb-4 flex items-center justify-between">
        <h3 class="text-xl font-bold">Activity Log</h3>
        <div class="flex items-center space-x-2">
          <select
            v-model="logFilter"
            class="rounded-md border p-1 text-sm"
            @change="fetchActivityLogs(1)"
          >
            <option value="all">All Actions</option>
            <option value="login">Login</option>
            <!-- Add other filter options as needed -->
          </select>
          <input
            type="text"
            v-model="logSearch"
            placeholder="Search..."
            class="rounded-md border p-1 text-sm"
            @input="fetchActivityLogs(1)"
          />
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr>
              <th class="border border-gray-700 px-4 py-2">ID</th>
              <th class="border border-gray-700 px-4 py-2">User</th>
              <th class="border border-gray-700 px-4 py-2">Action</th>
              <th class="border border-gray-700 px-4 py-2">Email</th>
              <th class="border border-gray-700 px-4 py-2">IP Address</th>
              <th class="border border-gray-700 px-4 py-2">Date/Time</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="activity in activityLogs" :key="activity.id" class="overflow-y-auto">
              <td class="border border-gray-700 px-4 py-2">{{ activity.id }}</td>
              <td class="border border-gray-700 px-4 py-2">
                {{ activity.user || 'N/A' }}
              </td>
              <td class="border border-gray-700 px-4 py-2 capitalize">
                {{ activity.action }}
              </td>
              <td class="border border-gray-700 px-4 py-2">
                {{ activity.details?.email || 'N/A' }}
              </td>
              <td class="border border-gray-700 px-4 py-2">
                {{ activity.ip_address }}
              </td>
              <td class="border border-gray-700 px-4 py-2">
                {{ formatDateTime(activity.timestamp) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-4 flex items-center justify-between">
        <div>Showing {{ activityLogs.length }} records</div>
        <div class="flex items-center space-x-4">
          <button
            @click="fetchActivityLogs(currentPage - 1)"
            :disabled="currentPage === 1"
            class="cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white disabled:opacity-50"
          >
            Prev
          </button>
          <span>Page {{ currentPage }} of {{ totalPages }}</span>
          <button
            @click="fetchActivityLogs(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white disabled:opacity-50"
          >
            Next
          </button>
        </div>
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
      <h3 class="mb-6 text-center text-2xl font-bold">Backup Management</h3>

      <button
        @click="createBackup"
        :disabled="loading"
        class="mb-4 w-full rounded-lg bg-green-600 p-2 text-white disabled:opacity-50"
      >
        {{ loading ? 'Creating...' : 'Create New Backup' }}
      </button>

      <div class="max-h-96 overflow-y-auto">
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr>
              <th class="border border-gray-700 px-4 py-2">ID</th>
              <th class="border border-gray-700 px-4 py-2">Created At</th>
              <th class="border border-gray-700 px-4 py-2">Name of the file</th>
              <th class="border border-gray-700 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="backup in backups" :key="backup.id">
              <td class="border border-gray-700 px-4 py-2">{{ backup.id }}</td>
              <td class="border border-gray-700 px-4 py-2">
                {{ formatDateTime(backup.created_at) }}
              </td>
              <td class="border border-gray-700 px-4 py-2 text-lg">
                {{ `fpms_backup_${backup.id}.sql` }}
              </td>
              <td class="space-x-2 border border-gray-700 px-4 py-2">
                <button
                  @click="downloadBackup(backup.id)"
                  class="rounded-lg bg-blue-600 px-3 py-1 text-white"
                >
                  Download
                </button>
                <button
                  @click="restoreBackup(backup.id)"
                  class="rounded-lg bg-yellow-600 px-3 py-1 text-white"
                >
                  Restore
                </button>
              </td>
            </tr>
          </tbody>
        </table>
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
  user: string | null
  action: string
  model: string
  object_id: string
  details: {
    email?: string
    // Add other possible detail fields here
  }
  ip_address: string
  timestamp: string
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
// Add this with your other ref declarations
const healthMetrics = ref({
  cpu_usage: 0,
  memory_usage: 0,
  disk_usage: 0,
  disk_space: 0,
  response_time: 0,
  timestamp: '',
})
const healthLoading = ref(false)
const showActivityLogPopup = ref(false)
const showUserMngtPopup = ref(false)
const showUserCrtPopup = ref(false)
// const showBackupPopup = ref(false)

const backups = ref<any[]>([])
const loading = ref(false)
const showBackupPopup = ref(false)
const backupLoading = ref(false) // Define the missing variable

const users = ref<User[]>([])
const activityLogs = ref<ActivityLog[]>([])
// const backups = ref<Backup[]>([])
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
  try {
    const params: any = {
      page: page,
      page_size: 3,
    }

    if (logFilter.value !== 'all') {
      params.action = logFilter.value
    }

    if (logSearch.value) {
      params.search = logSearch.value
    }

    const { data } = await useAxios(`${baseURL}/activity-logs/`, {
      params: params,
    })

    if (data.value) {
      activityLogs.value = data.value.results || data.value
      if (data.value.count) {
        totalPages.value = Math.ceil(data.value.count / 10)
      }
    }
  } catch (err) {
    console.error('Failed to fetch activity logs:', err)
  }
}
// const fetchBackups = async () => {
//   const { data } = await useAxios(`${baseURL}/backups/`, { method: 'GET' })
//   backups.value = data.value || []
// }

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

// const createBackup = async () => {
//   const { error } = await useAxios(`${baseURL}/backups/`, {
//     method: 'POST',
//   })

//   if (!error.value) {
//     await fetchBackups()
//   }
// }

// const downloadBackup = async (backupName: string) => {
//   const { data } = await useAxios(`${baseURL}/backups/${backupName}/download/`, {
//     method: 'GET',
//     responseType: 'blob',
//   })

//   if (data.value) {
//     const url = window.URL.createObjectURL(new Blob([data.value]))
//     const link = document.createElement('a')
//     link.href = url
//     link.setAttribute('download', backupName)
//     document.body.appendChild(link)
//     link.click()
//     document.body.removeChild(link)
//   }
// }

const handleFileUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    selectedBackupFile.value = input.files[0]
  }
}

// const restoreBackup = async () => {
//   if (!selectedBackupFile.value) return

//   const formData = new FormData()
//   formData.append('file', selectedBackupFile.value)

//   const { error } = await useAxios(`${baseURL}/backups/restore/`, {
//     method: 'POST',
//     data: formData,
//     headers: {
//       'Content-Type': 'multipart/form-data',
//     },
//   })

const fetchBackups = async () => {
  try {
    backupLoading.value = true
    const { data } = await useAxios(`${baseURL}/backups/`, {
      method: 'GET',
    })
    backups.value = data.value || []
  } catch (err) {
    console.error('Failed to fetch backups:', err)
  } finally {
    backupLoading.value = false
  }
}

const createBackup = async () => {
  try {
    backupLoading.value = true
    const { data } = await useAxios(`${baseURL}/backups/create_backup/`, {
      method: 'POST',
    })

    if (data.value?.status === 'success') {
      alert(`Backup created successfully!\nFile: ${data.value.file_path}`)
      await fetchBackups()
    }
  } catch (err) {
    console.error('Backup creation failed:', err)
    alert('Failed to create backup. Please check console for details.')
  } finally {
    backupLoading.value = false
  }
}

const downloadBackup = async (backup_Id: number) => {
  try {
    backupLoading.value = true
    const { data } = await useAxios(`${baseURL}/backups/${backup_Id}/download/`, {
      method: 'GET',
      responseType: 'blob',
    })

    if (data.value) {
      const url = window.URL.createObjectURL(new Blob([data.value]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `fpms_backup_${backup_Id}.sql`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  } catch (err) {
    console.error('Download failed:', err)
    alert('Failed to download backup. Please check console for details.')
  } finally {
    backupLoading.value = false
  }
}

const restoreBackup = async (backup_Id: number) => {
  if (!confirm('WARNING: This will overwrite current data. Are you sure?')) {
    return
  }

  try {
    backupLoading.value = true
    const { data } = await useAxios(`${baseURL}/backups/${backup_Id}/restore/`, {
      method: 'POST',
    })

    if (data.value?.status === 'success') {
      alert('Database restored successfully!')
    }
  } catch (err) {
    console.error('Restore failed:', err)
    alert('Failed to restore backup. Please check console for details.')
  } finally {
    backupLoading.value = false
  }
}
const fetchHealthMetrics = async () => {
  try {
    healthLoading.value = true
    const { data } = await useAxios(`${baseURL}/health-metrics/current/`)

    if (data.value) {
      healthMetrics.value = data.value
    }
  } catch (err) {
    console.error('Failed to fetch health metrics:', err)
  } finally {
    healthLoading.value = false
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
  // fetchBackups()
  // fetchBackups()
  fetchBackups()
  fetchHealthMetrics()
})
const logFilter = ref('all')
const logSearch = ref('')
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
