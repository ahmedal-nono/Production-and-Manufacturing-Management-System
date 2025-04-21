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
      <div class="flex flex-row space-x-6">
        <button class="mt-2 h-fit rounded-xl bg-red-500 px-6 py-1 text-white" @click="logout">
          Logout
        </button>
        <img
          src="../assets/avatar.png"
          alt=""
          class="size-12 cursor-pointer"
          @click="showAvatarPopup = true"
        />
      </div>
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
import { useUserStore } from '@/stores/user'
import router from '@/router'

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

const showNotificationPopup = ref(false)
const showAvatarPopup = ref(false)
const uploadedImage = ref<string | null>(null)

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

function logout() {
  useUserStore().logout()
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
