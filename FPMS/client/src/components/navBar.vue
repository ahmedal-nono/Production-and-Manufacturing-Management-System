<template>
  <div class="flex h-fit w-full flex-col pb-2 pl-3">
    <div class="flex w-full justify-between px-2 pt-4">
      <div>
        <img
          src="../assets/noti.png"
          class="size-11 cursor-pointer"
          alt="Notification"
          @click="showNotificationPopup = true"
        />
        <Popup
          :visible="showNotificationPopup"
          @update:visible="showNotificationPopup = $event"
          title="Notification Received"
        >
          <template v-for="noti in notifications" :key="noti.id">
            <NotificationCard
              :isRead="noti.isRead"
              :time="noti.time"
              :title="noti.message"
              :body="noti.type"
              @mark-as-read="notificationStore.markNotificationAsRead(noti.id)"
            ></NotificationCard>
          </template>
        </Popup>
      </div>
      <div class="flex flex-row space-x-6">
        <button class="mt-2 h-fit rounded-xl bg-red-500 px-6 py-1 text-white" @click="logout">
          Logout
        </button>
        <img
          :src="profileImageUrl"
          alt="Profile"
          class="size-12 cursor-pointer rounded-full border"
          @click="showAvatarPopup = true"
        />
      </div>
      <Popup :visible="showAvatarPopup" @update:visible="showAvatarPopup = $event">
        <div class="flex flex-col items-center space-y-4">
          <div class="flex flex-col justify-center space-y-1">
            <img
              v-if="uploadedImage || currentProfilePic"
              :src="uploadedImage || fullProfilePicUrl"
              alt="Profile Image"
              class="size-32 rounded-full border"
            />
            <img
              v-else
              src="../assets/avatar.png"
              alt="Default Avatar"
              class="ml-2 size-32 rounded-full border"
            />
            <p class="font-bold">Upload New Image</p>
          </div>
          <div>
            <label class="flex cursor-pointer items-center space-x-2">
              <input
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleImageUpload"
                ref="fileInput"
              />
              <button
                type="button"
                class="rounded-lg bg-blue-600 p-2 text-white"
                @click="triggerFileInput"
              >
                Upload Image
              </button>
            </label>
          </div>
          <button
            class="w-full rounded-lg bg-blue-600 p-2 text-white"
            @click="updateProfilePicture"
            :disabled="!uploadedImage || isUpdatingProfile"
          >
            {{ isUpdatingProfile ? 'Saving...' : 'Save Profile Image' }}
          </button>

          <form @submit.prevent="changePassword" class="mt-6 w-full">
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
                  required
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
                  required
                  minlength="8"
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
                  required
                  minlength="8"
                />
              </div>
              <div v-if="passwordError" class="text-sm text-red-500">{{ passwordError }}</div>
              <button
                type="submit"
                class="w-full rounded-lg bg-blue-600 p-2 text-white"
                :disabled="isChangingPassword"
              >
                {{ isChangingPassword ? 'Updating...' : 'Update Password' }}
              </button>
            </div>
          </form>
        </div>

        <div class="mt-4 flex flex-col items-start space-y-2">
          <h3 class="font-bold">Set Security Question</h3>
          <p class="text-sm font-bold">Security Question</p>
          <select
            v-model="selectedSecurityQuestion"
            class="w-full rounded-md border border-gray-400 p-2 text-sm"
          >
            <option value="" disabled>Select a security question</option>
            <option value="pet">What's your pet's name?</option>
            <option value="city">What city were you born in?</option>
            <option value="mother_maiden">Mother's maiden name?</option>
            <option value="school">First school name?</option>
          </select>
          <label class="font-bold">Answer</label>
          <input
            type="text"
            v-model="securityAnswer"
            placeholder="Enter your answer"
            class="my-1 block w-full rounded-md border border-gray-300 p-2 shadow-xs"
          />
          <button
            class="mt-2 w-full rounded-lg bg-blue-600 p-2 text-white"
            @click="updateSecurityQuestion"
            :disabled="!selectedSecurityQuestion || !securityAnswer || isUpdatingSecurity"
          >
            {{ isUpdatingSecurity ? 'Updating...' : 'Update Security Question' }}
          </button>
        </div>

        <div v-if="errorMessage" class="mt-4 text-center text-red-500">
          {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="mt-4 text-center text-green-500">
          {{ successMessage }}
        </div>
      </Popup>
    </div>

    <slot />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Popup from '@/components/popup.vue'
import NotificationCard from '@/components/NotificationCard.vue'
import { useUserStore } from '@/stores/user'
import notificationStore from '@/stores/notificationStore'
import router from '@/router'
import type { UserType } from '@/stores/user'
import useNotificationStore from '@/stores/notificationStore'

interface ProfileData {
  profile_pic: string | null
  security_question: string | null
  security_answer: string | null
}

// Stores
const userStore = useUserStore()

// User data
const currentUser = computed(() => userStore.user)
const userId = computed(() => currentUser.value?.id)
const profileImageUrl = computed(() => {
  if (currentProfilePic.value) {
    return `http://localhost:8000${currentProfilePic.value}`
  }
  return '../assets/avatar.png'
})

// Popup states
const showNotificationPopup = ref(false)
const showAvatarPopup = ref(false)
const currentPassword = ref('')
// Duplicate declaration removed
// Notifications
const notifications = computed(() =>
  notificationStore.getNotificationsForRole(currentUser.value?.role || ''),
)

// Profile image
const fileInput = ref<HTMLInputElement | null>(null)
const uploadedImage = ref<string | null>(null)
const selectedFile = ref<File | null>(null)
const currentProfilePic = ref<string | null>(null)
const fullProfilePicUrl = computed(() =>
  currentProfilePic.value ? `http://localhost:8000${currentProfilePic.value}` : '',
)
const isUpdatingProfile = ref(false)

// Password fields
const newPassword = ref('')
const confirmPassword = ref('')
const passwordError = ref('')
const isChangingPassword = ref(false)

// Security question fields
const selectedSecurityQuestion = ref('')
const securityAnswer = ref('')
const isUpdatingSecurity = ref(false)

// Messages
const errorMessage = ref('')
const successMessage = ref('')

// Fetch user profile data when component mounts or user changes
onMounted(async () => {
  if (!userId.value) {
    errorMessage.value = 'User not authenticated'
    return
  }
  await fetchProfileData()
})

async function fetchProfileData() {
  try {
    const response = await axios.get<ProfileData>(
      `http://localhost:8000/profile/${userId.value}/`,
      {
        headers: {
          Authorization: `Bearer ${userStore.access}`,
        },
      },
    )
    currentProfilePic.value = response.data.profile_pic
    selectedSecurityQuestion.value = response.data.security_question || ''
    securityAnswer.value = response.data.security_answer || ''
  } catch (error) {
    console.error('Error fetching profile data:', error)
    errorMessage.value = 'Failed to load profile data'
    setTimeout(() => (errorMessage.value = ''), 3000)
  }
}

const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

const handleImageUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    selectedFile.value = input.files[0]
    const reader = new FileReader()
    reader.onload = (e) => {
      uploadedImage.value = e.target?.result as string
    }
    reader.readAsDataURL(input.files[0])
  }
}

const updateProfilePicture = async () => {
  if (!selectedFile.value || !userId.value) return

  isUpdatingProfile.value = true
  errorMessage.value = ''

  const formData = new FormData()
  formData.append('profile_pic', selectedFile.value)

  try {
    const response = await axios.put(`http://localhost:8000/profile/${userId.value}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${userStore.access}`,
      },
    })

    currentProfilePic.value = response.data.profile_pic
    uploadedImage.value = null
    selectedFile.value = null

    successMessage.value = 'Profile picture updated successfully!'
    setTimeout(() => (successMessage.value = ''), 3000)
  } catch (error) {
    console.error('Error updating profile picture:', error)
    errorMessage.value = 'Failed to update profile picture'
    setTimeout(() => (errorMessage.value = ''), 3000)
  } finally {
    isUpdatingProfile.value = false
  }
}

const changePassword = async () => {
  // Check if user is authenticated
  if (!userId.value) {
    errorMessage.value = 'You must be logged in to change your password'
    setTimeout(() => (errorMessage.value = ''), 3000)
    return
  }

  // Validate current password
  if (!currentPassword.value) {
    passwordError.value = 'Current password is required'
    return
  }

  // Validate new password
  if (!newPassword.value) {
    passwordError.value = 'New password is required'
    return
  }

  // Check password match
  if (newPassword.value !== confirmPassword.value) {
    passwordError.value = 'New passwords do not match'
    return
  }

  // Check password length
  if (newPassword.value.length < 8) {
    passwordError.value = 'Password must be at least 8 characters'
    return
  }

  // Clear previous errors
  passwordError.value = ''
  isChangingPassword.value = true
  errorMessage.value = ''

  try {
    const response = await axios.post(
      `http://localhost:8000/change-password/${userId.value}/`,
      {
        old_password: currentPassword.value,
        new_password: newPassword.value,
      },
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${userStore.access}`,
        },
      },
    )

    // Handle successful password change
    successMessage.value = 'Password changed successfully!'

    // Clear form fields
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''

    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (error: any) {
    console.error('Error changing password:', error)

    // Handle specific backend validation errors
    if (error.response?.data?.old_password) {
      passwordError.value = error.response.data.old_password.join(' ')
    } else if (error.response?.data?.new_password) {
      passwordError.value = error.response.data.new_password.join(' ')
    } else {
      errorMessage.value = error.response?.data?.detail || 'Failed to change password'
    }

    // Clear error messages after 3 seconds
    setTimeout(() => {
      errorMessage.value = ''
      passwordError.value = ''
    }, 3000)
  } finally {
    isChangingPassword.value = false
  }
}

const updateSecurityQuestion = async () => {
  if (!selectedSecurityQuestion.value || !securityAnswer.value || !userId.value) return

  isUpdatingSecurity.value = true
  errorMessage.value = ''

  try {
    await axios.put(
      `http://localhost:8000/profile/${userId.value}/`,
      {
        security_question: selectedSecurityQuestion.value,
        security_answer: securityAnswer.value,
      },
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${userStore.access}`,
        },
      },
    )

    successMessage.value = 'Security question updated successfully!'
    setTimeout(() => (successMessage.value = ''), 3000)
  } catch (error) {
    console.error('Error updating security question:', error)
    errorMessage.value = 'Failed to update security question'
    setTimeout(() => (errorMessage.value = ''), 3000)
  } finally {
    isUpdatingSecurity.value = false
  }
}

function logout() {
  userStore.logout()
  router.push({ name: 'login' })
}
</script>

<style>
span {
  font-weight: normal;
}
button {
  cursor: pointer;
}
</style>
