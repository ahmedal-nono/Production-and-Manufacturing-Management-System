<template>
  <div class="flex h-fit w-full flex-col pb-2 pl-3">
    <div class="flex w-full justify-between px-2 pt-4">
      <div>
        <img
          src="../assets/noti.png"
          class="size-11 cursor-pointer"
          alt="Notification"
          @click="showPopup = true"
        />
        <Popup
          :visible="showPopup"
          @update:visible="showPopup = $event"
          title="Notification Received"
        >
          <template v-for="noti of notifications">
            <NotificationCard
              :isRead="noti.isRead"
              :time="noti.time"
              :title="noti.title"
              :body="noti.body"
            ></NotificationCard>
          </template>
        </Popup>
      </div>

      <div class="flex h-9 w-3/12 cursor-pointer space-x-2 rounded-xl border-black bg-white">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="chakra-icon css-ugv5hc mt-1.5 ml-2"
        >
          <path d="M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0"></path>
          <path d="M21 21l-6 -6"></path>
        </svg>
        <input type="text" name="" id="" placeholder="Search" class="w-full rounded-xl p-1" />
      </div>

      <img
        src="../assets/avatar.png"
        alt=""
        class="size-12 cursor-pointer"
        @click="showAvatarPopup = true"
      />
      <Popup :visible="showAvatarPopup" @update:visible="showAvatarPopup = $event">
        <div class="flex flex-col items-center space-y-4">
          <div class="flex flex-col justify-center space-y-1">
            <img
              v-if="uploadedImage"
              :src="uploadedImage"
              alt="Profile Image"
              class="size-32 rounded-full border"
            />
            <img
              v-else
              src="../assets/avatar.png"
              alt="Default Avatar"
              class="ml-2 size-32 rounded-full border"
            />
            <p class="font-bold">Uplaod New Image</p>
          </div>
          <div>
            <label class="flex cursor-pointer items-center space-x-2">
              <input type="file" accept="image/*" class="hidden" @change="handleImageUpload" />
              <button class="rounded-lg bg-blue-600 p-2 text-white" @click="() => {}">
                Upload Image
              </button>
            </label>
          </div>
          <button class="w-full rounded-lg bg-blue-600 p-2 text-white">Save Profile Image</button>
          <div></div>
          <form @submit.prevent="() => {}" class="mt-6 w-full">
            <h3 class="mb-3 flex content-start text-lg font-bold">Change Password</h3>
            <div class="flex flex-col space-y-4">
              <div class="flex w-full flex-col items-start space-y-2">
                <label for="currentPassword" class="text-sm font-bold text-gray-700">
                  Current Password
                </label>
                <input
                  id="currentPassword"
                  type="password"
                  v-model="currentPassword"
                  class="mt-1 w-full rounded-md border border-gray-300 p-2 shadow-xs"
                  placeholder="Enter current password"
                />
              </div>
              <div class="flex w-full flex-col items-start space-y-2">
                <label for="newPassword" class="text-sm font-bold text-gray-700">
                  New Password
                </label>
                <input
                  id="newPassword"
                  type="password"
                  v-model="newPassword"
                  class="mt-1 block w-full rounded-md border border-gray-300 p-2 shadow-xs"
                  placeholder="Enter new password"
                />
              </div>
              <div class="flex w-full flex-col items-start space-y-2">
                <label for="confirmPassword" class="text-sm font-bold text-gray-700">
                  Confirm Password
                </label>
                <input
                  id="confirmPassword"
                  type="password"
                  v-model="confirmPassword"
                  class="mt-1 block w-full rounded-md border border-gray-300 p-2 shadow-xs"
                  placeholder="Confirm new password"
                />
              </div>
            </div>
          </form>
        </div>
        <div class="mt-4 flex flex-col items-start space-y-2">
          <h3 class="font-bold">Set Security Question</h3>
          <p class="text-sm font-bold">Security Question</p>
          <select name="" id="" class="rounded-md border border-gray-400 p-0 text-sm">
            <option value="">Select a security question</option>
          </select>
          <label class="font-bold">Answer</label>
          <input
            type="text"
            name=""
            id=""
            placeholder="Enter your answer"
            class="my-1 block w-full rounded-md border border-gray-300 p-2 shadow-xs"
          />
        </div>
        <button class="mt-4 w-full rounded-lg bg-blue-600 p-2 text-white">
          Update Password & Security Question
        </button>
      </Popup>
    </div>

    <slot />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Popup from '@/components/popup.vue'
import NotificationCard from '@/components/NotificationCard.vue'

const currentPassword = defineModel('currentPassword')
const newPassword = defineModel('newPassword')
const confirmPassword = defineModel('confirmPassword')

const notifications = [
  {
    isRead: false,
    time: '2 hours ago',
    title: 'New Message',
    body: 'You have a new message from John Doe.',
  },
]

const showPopup = ref(false)
const showAvatarPopup = ref(false)
const showUserCrtPopup = ref(false)
const isRead = ref(false)
const isReadSecond = ref(false)
const uploadedImage = ref<string | null>(null)

const users = ref([
  {
    name: 'John Doe',
    email: 'john.doe@example.com',
    department: 'Engineering',
    role: 'Admin',
    status: 'Active',
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

<style>
span {
  font-weight: normal;
}
</style>
