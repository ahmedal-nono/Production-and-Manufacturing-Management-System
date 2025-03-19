<template>
  <div class="w-full">
    <div class="pl-3 pb-2 h-fit">
      <div class="flex w-full flex-col">
        <div class="flex w-full justify-between px-2 pt-4">
          <div>
            <img
              src="../assets/noti.png"
              class="size-11 cursor-pointer"
              alt="Notification"
              @click="showPopup = true"
            />
            <Popup :visible="showPopup" @update:visible="showPopup = $event">
              <h3 class="font-bold text-xl mb-4">Notification Received</h3>
              <div
                :class="
                  isRead
                    ? 'flex flex-col space-y-4 bg-gray-100 p-4 rounded-lg border-l-8 border-gray-500'
                    : 'flex flex-col space-y-4 bg-blue-50 p-4 rounded-lg border-l-8 border-blue-500'
                "
              >
                <div class="flex justify-between">
                  <p class="font-bold text-lg">Workflow Stage Completion</p>
                  <p class="font-light text-sm text-gray-400">2 hours ago</p>
                </div>
                <div class="flex justify-start">
                  <p class="text-gray-500">
                    The "Assembly" stage has been completed for Order #12345.
                  </p>
                </div>
                <div class="flex justify-around gap-5">
                  <button
                    v-if="!isRead"
                    class="bg-green-600 text-white p-2 rounded-lg w-full"
                    @click.stop="markAsRead()"
                  >
                    Mark As Read
                  </button>
                  <button class="bg-blue-600 text-white p-2 rounded-lg w-full">
                    View Details
                  </button>
                </div>
              </div>
              <div
                :class="
                  isReadSecond
                    ? 'flex flex-col space-y-4 bg-gray-100 p-4 rounded-lg border-l-8 border-gray-500 mt-4'
                    : 'flex flex-col space-y-4 bg-blue-50 p-4 rounded-lg border-l-8 border-blue-500 mt-4'
                "
              >
                <div class="flex justify-between">
                  <p class="font-bold text-lg">Delay Notification</p>
                  <p class="font-light text-sm text-gray-400">Yesterday</p>
                </div>
                <div class="flex justify-start">
                  <p class="text-gray-500">
                    Order #12346 has been delayed due to material shortage.
                  </p>
                </div>
                <div class="flex justify-around gap-5">
                  <button
                    v-if="!isReadSecond"
                    class="bg-green-600 text-white p-2 rounded-lg w-full"
                    @click.stop="markAsReadSecond()"
                  >
                    Mark As Read
                  </button>
                  <button class="bg-blue-600 text-white p-2 rounded-lg w-full">
                    View Details
                  </button>
                </div>
              </div>
            </Popup>
          </div>
          <div
            class="flex cursor-pointer space-x-2 border-black bg-white rounded-xl w-3/12 h-9"
          >
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
            <input
              type="text"
              name=""
              id=""
              placeholder="Search"
              class="w-full p-1 rounded-xl"
            />
          </div>
          <img
            src="../assets/avatar.png"
            alt=""
            class="size-12 cursor-pointer"
            @click="showAvatarPopup = true"
          />
          <Popup
            :visible="showAvatarPopup"
            @update:visible="showAvatarPopup = $event"
          >
            <h3 class="font-bold text-xl mb-4 flex justify-center">
              Change Profile Image
            </h3>
            <div class="flex flex-col items-center space-y-4">
              <div class="flex flex-col space-y-1 justify-center">
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
                  class="size-32 ml-2 rounded-full border"
                />
                <p class="font-bold">Uplaod New Image</p>
              </div>
              <div>
                <label class="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="handleImageUpload"
                  />
                  <button class="bg-blue-600 text-white p-2 rounded-lg">
                    Upload Image
                  </button>
                </label>
              </div>
              <button class="w-full bg-blue-600 text-white p-2 rounded-lg">
                Save Profile Image
              </button>
              <div></div>
              <form @submit.prevent="handlePasswordChange" class="w-full mt-6">
                <h3 class="font-bold text-lg flex content-start mb-3">
                  Change Password
                </h3>
                <div class="flex flex-col space-y-4">
                  <div class="flex flex-col items-start space-y-2 w-full">
                    <label
                      for="currentPassword"
                      class="text-sm font-bold text-gray-700"
                    >
                      Current Password
                    </label>
                    <input
                      id="currentPassword"
                      type="password"
                      v-model="currentPassword"
                      class="mt-1 p-2 w-full rounded-md border border-gray-300 shadow-sm"
                      placeholder="Enter current password"
                    />
                  </div>
                  <div class="flex flex-col items-start space-y-2 w-full">
                    <label
                      for="newPassword"
                      class="text-sm font-bold text-gray-700"
                    >
                      New Password
                    </label>
                    <input
                      id="newPassword"
                      type="password"
                      v-model="newPassword"
                      class="mt-1 p-2 block w-full rounded-md border border-gray-300 shadow-sm"
                      placeholder="Enter new password"
                    />
                  </div>
                  <div class="flex flex-col items-start space-y-2 w-full">
                    <label
                      for="confirmPassword"
                      class="text-sm font-bold text-gray-700"
                    >
                      Confirm Password
                    </label>
                    <input
                      id="confirmPassword"
                      type="password"
                      v-model="confirmPassword"
                      class="mt-1 p-2 block w-full rounded-md border border-gray-300 shadow-sm"
                      placeholder="Confirm new password"
                    />
                  </div>
                </div>
              </form>
            </div>
            <div class="flex flex-col items-start mt-4 space-y-2">
              <h3 class="font-bold">Set Security Question</h3>
              <p class="text-sm font-bold">Security Question</p>
              <select
                name=""
                id=""
                class="border rounded-md p-0 text-sm border-gray-400"
              >
                <option value="">Select a security question</option>
              </select>
              <label class="font-bold">Answer</label>
              <input
                type="text"
                name=""
                id=""
                placeholder="Enter your answer"
                class="my-1 p-2 block w-full rounded-md border border-gray-300 shadow-sm"
              />
            </div>
            <button class="w-full bg-blue-600 text-white p-2 rounded-lg mt-4">
              Update Password & Security Question
            </button>
          </Popup>
        </div>
      </div>
    </div>

    
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Popup from "../components/popup.vue";

const showPopup = ref(false);
const showAvatarPopup = ref(false);
const showUserCrtPopup = ref(false);
const isRead = ref(false);
const isReadSecond = ref(false);
const uploadedImage = ref<string | null>(null);


const users = ref([
  {
    name: "John Doe",
    email: "john.doe@example.com",
    department: "Engineering",
    role: "Admin",
    status: "Active",
  },
]);

function markAsRead() {
  isRead.value = true;
}

function markAsReadSecond() {
  isReadSecond.value = true;
}

function handleImageUpload(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      uploadedImage.value = reader.result as string;
    };
    reader.readAsDataURL(file);
  }
}
const newUser = ref({
  name: "",
  email: "",
  department: "",
  role: "",
  status: "Active",
  password: "",
});

const createUser = () => {
  if (
    newUser.value.name &&
    newUser.value.email &&
    newUser.value.department &&
    newUser.value.role &&
    newUser.value.password
  ) {
    users.value.push({ ...newUser.value });

    newUser.value = {
      name: "",
      email: "",
      department: "",
      role: "",
      status: "Active",
      password: "",
    };

    showUserCrtPopup.value = false;
  }
};

const closePopup = () => {
  showUserCrtPopup.value = false;
};

const showLanguageTimezonePopup = ref(false);

const settings = ref({
  language: "English",
  timezone: "UTC",
});

const saveSettings = () => {
  console.log("Settings Saved:", settings.value);
  showLanguageTimezonePopup.value = false;
};
const showBackupPopup = ref(false);

// Backup settings state
const backupSettings = ref({
  frequency: "Daily",
  time: "",
});

// Backup history data
const backupHistory = ref([
  { name: "Backup_2024_11_25.zip", date: "25 Nov 2024", status: "Completed" },
  { name: "Backup_2024_11_24.zip", date: "24 Nov 2024", status: "Completed" },
]);

const saveBackupSettings = () => {
  console.log("Backup Settings Saved:", backupSettings.value);
};

const handleFileUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    console.log("Selected file for restore:", file.name);
  }
};

const restoreData = () => {
  console.log("Restore data initiated.");
};

const downloadBackup = (fileName: string) => {
  console.log("Downloading backup:", fileName);
};
</script>

<style>
span {
  font-weight: normal;
}
</style>
