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
                :class="isRead ? 'flex flex-col space-y-4 bg-gray-100 p-4 rounded-lg border-l-8 border-gray-500' : 'flex flex-col space-y-4 bg-blue-50 p-4 rounded-lg border-l-8 border-blue-500'"
              >
                <div class="flex justify-between">
                  <p class="font-bold text-lg">Workflow Stage Completion</p>
                  <p class="font-light text-sm text-gray-400">2 hours ago</p>
                </div>
                <div class="flex justify-start">
                  <p class="text-gray-500">The "Assembly" stage has been completed for Order #12345.</p>
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
                :class="isReadSecond ? 'flex flex-col space-y-4 bg-gray-100 p-4 rounded-lg border-l-8 border-gray-500 mt-4' : 'flex flex-col space-y-4 bg-blue-50 p-4 rounded-lg border-l-8 border-blue-500 mt-4'"
              >
                <div class="flex justify-between">
                  <p class="font-bold text-lg">Delay Notification</p>
                  <p class="font-light text-sm text-gray-400">Yesterday</p>
                </div>
                <div class="flex justify-start">
                  <p class="text-gray-500">Order #12346 has been delayed due to material shortage.</p>
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
          <div class="flex cursor-pointer space-x-2 border-black bg-white rounded-xl w-3/12 h-9">
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
            <input type="text" name="" id="" placeholder="Search" class="w-full rounded-xl">
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
            <h3 class="font-bold text-xl mb-4 flex justify-center">Change Profile Image</h3>
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
              <button class="w-full bg-blue-600 text-white p-2 rounded-lg ">Save Profile Image</button>
              <div>
                
              </div>
              <form @submit.prevent="handlePasswordChange" class="w-full  mt-6">
                <h3 class="font-bold text-lg flex content-start mb-3">Change Password</h3>
                <div class="flex flex-col space-y-4">
                  <div class="flex flex-col items-start space-y-2 w-full">
                    <label
                      for="currentPassword"
                      class=" text-sm font-bold text-gray-700"
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
                      class=" text-sm font-bold text-gray-700"
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
                      class=" text-sm font-bold text-gray-700"
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
              <select name="" id="" class="border rounded-md p-0 text-sm border-gray-400">
                <option value="">Select a security question</option>
              </select>
              <label class="font-bold">Answer</label>
              <input type="text" name="" id="" placeholder="Enter your answer" class="my-1 p-2 block w-full rounded-md border border-gray-300 shadow-sm">
            </div>
            <button class="w-full bg-blue-600 text-white p-2 rounded-lg mt-4">Update Password & Security Question</button>
          </Popup>
        </div>
      </div>
    </div>
    <!-- sys admin module-->
    <div class="flex flex-col m-2 p-4 justify-center rounded-2xl bg-gray-200">
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
    </div>

    <Popup :visible="showActivityLogPopup" @update:visible="showActivityLogPopup = $event">
      <div>
        <h3 class="font-bold text-xl mb-4">Filter Activity Log</h3>
        <h5 class="font-bold text-sm my-2">Start Date</h5>
        <input type="date" name="" id="" class="border-2 rounded-md p-1 w-full">
        <h5 class="font-bold text-sm my-2">End Date</h5>
        <input type="date" name="" id="" class="border-2 rounded-md p-1 w-full">
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
        <button class="bg-blue-600 p-1.5 w-2/12 rounded-lg text-white">Prev</button>
        <p class="mt-2">Page 1 of 5</p>
        <button class="bg-blue-600 p-1.5 w-2/12 rounded-lg text-white">Next</button>
      </div>
    </Popup>
    <Popup :visible="showUserMngtPopup" @update:visible="showUserMngtPopup = $event">
  <h3 class="font-bold text-2xl mb-4 justify-center flex">User Account Management</h3>
  <div class="flex justify-end">
    <button class="bg-blue-600 p-1.5 w-2/12 rounded-lg text-white" @click="showUserCrtPopup = true">Create User</button>
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
            <button class="bg-yellow-500 p-2 rounded-lg text-white">Edit</button>
            <button class="bg-red-600 p-2 rounded-lg text-white">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</Popup>
<Popup :visible="showUserCrtPopup" @update:visible="showUserCrtPopup = $event">
  <h3 class="font-bold text-2xl mb-4 justify-center flex">Create New User</h3>
  <div>
    <form @submit.prevent="createUser" class="space-y-4">
      <div class="flex flex-col">
        <label for="name" class="font-bold text-sm">Full Name</label>
        <input type="text" id="name" v-model="newUser.name" placeholder="Enter full name" class="p-2 border rounded-md" required />
      </div>
      <div class="flex flex-col">
        <label for="email" class="font-bold text-sm">Email</label>
        <input type="email" id="email" v-model="newUser.email" placeholder="Enter email" class="p-2 border rounded-md" required />
      </div>
      <div class="flex flex-col">
        <label for="department" class="font-bold text-sm">Contact Number</label>
        <input type="text" id="number" v-model="newUser.department" placeholder="Enter contact number" class="p-2 border rounded-md" required />
      </div>
      <div class="flex flex-col">
        <label for="department" class="font-bold text-sm">Department</label>
        <input type="text" id="department" v-model="newUser.department" placeholder="Enter department" class="p-2 border rounded-md" required />
      </div>
      <div class="flex flex-col">
        <label for="role" class="font-bold text-sm">Role</label>
        <select id="status" v-model="newUser.status" class="p-2 border rounded-md" required>
          <option value="Active">Select a role</option>
          </select>
      </div>
      <div class="flex flex-col">
        <label for="status" class="font-bold text-sm">Status</label>
        <select id="status" v-model="newUser.status" class="p-2 border rounded-md" required>
          <option value="Active">Active</option>
          <option value="Inactive">Inactive</option>
        </select>
      </div>
      <div class="flex flex-col">
        <label for="password" class="font-bold text-sm">Password</label>
        <input type="password" id="password" v-model="newUser.password" placeholder="Enter password" class="p-2 border rounded-md" required />
      </div>
      <div class="flex justify-end gap-4">
        <button type="button" class="bg-gray-500 text-white p-2 rounded-lg" @click="closePopup">Cancel</button>
        <button type="submit" class="bg-blue-600 text-white p-2 rounded-lg">Create User</button>
      </div>
    </form>
  </div>
</Popup>
<Popup :visible="showLanguageTimezonePopup" @update:visible="showLanguageTimezonePopup = $event">
  <h3 class="font-bold text-2xl mb-4 justify-center flex">Language & Time Zone Settings</h3>
  <div>
    <form @submit.prevent="saveSettings" class="space-y-4">

      <div class="flex flex-col">
        <label for="language" class="font-bold text-sm">Preferred Language</label>
        <select id="language" v-model="settings.language" class="p-2 border rounded-md" required>
          <option value="English">English</option>
          <option value="Arabic">Arabic</option>
        </select>
      </div>

      <div class="flex flex-col">
        <label for="timezone" class="font-bold text-sm">Time Zone</label>
        <select id="timezone" v-model="settings.timezone" class="p-2 border rounded-md" required>
          <option value="UTC">UTC-12:00</option>
          <option value="GMT">GMT</option>
        </select>
      </div>
      <div class="flex justify-end gap-4">
        <button type="submit" class="bg-blue-600 text-white p-2 w-full rounded-lg">Save Settings</button>
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
      <label for="backup-frequency" class="font-bold text-sm block mb-1">Backup Frequency</label>
      <select id="backup-frequency" v-model="backupSettings.frequency" class="p-2 border rounded-md w-full">
        <option value="Daily">Daily</option>
        <option value="Weekly">Weekly</option>
        <option value="Monthly">Monthly</option>
      </select>
    </div>
    <div class="mb-4">
      <label for="backup-time" class="font-bold text-sm block mb-1">Backup Time</label>
      <input
        type="time"
        id="backup-time"
        v-model="backupSettings.time"
        class="p-2 border rounded-md w-full"
      />
    </div>
    <button @click="saveBackupSettings" class="bg-blue-600 text-white px-4 py-2 rounded-lg w-full">
      Save Backup Settings
    </button>
  </div>

  <!-- Restore Data -->
  <div class="mb-6 p-4 border rounded-lg bg-gray-100">
    <h4 class="font-bold text-lg mb-4">Restore Data</h4>
    <div class="mb-4">
      <label for="restore-file" class="font-bold text-sm block mb-1">Select Backup File</label>
      <input type="file" id="restore-file" @change="handleFileUpload" class="p-2 border rounded-md w-full" />
    </div>
    <button @click="restoreData" class="bg-red-600 text-white px-4 py-2 rounded-lg w-full">
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
            <button class="bg-green-600 w-full text-white px-3 py-1 rounded-lg" @click="downloadBackup(backup.name)">
              Download
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
import { ref } from 'vue';
import Popup from '../components/popup.vue';

const showPopup = ref(false);
const showAvatarPopup = ref(false);
const showActivityLogPopup = ref(false);
const showUserMngtPopup = ref(false);
const showUserCrtPopup = ref(false);
const isRead = ref(false);
const isReadSecond = ref(false);
const uploadedImage = ref<string | null>(null);

const userActivities = ref([
  { user: 'John Doe', activity: 'Logged In', date: '2024-11-24', time: '10:30 AM', ip: '192.168.1.1' },
  { user: 'Jane Smith', activity: 'Changed Profile Picture', date: '2024-11-24', time: '09:45 AM', ip: '192.168.1.2' },
  { user: 'John Doe', activity: 'Updated Settings', date: '2024-11-23', time: '03:10 PM', ip: '192.168.1.3' },
]);

const users = ref([
  { name: 'John Doe', email: 'john.doe@example.com', department: 'Engineering', role: 'Admin', status: 'Active' },

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
  name: '',
  email: '',
  department: '',
  role: '',
  status: 'Active',
  password: '', 
});

const createUser = () => {
  if (newUser.value.name && newUser.value.email && newUser.value.department && newUser.value.role && newUser.value.password) {
    users.value.push({ ...newUser.value });

    newUser.value = { name: '', email: '', department: '', role: '', status: 'Active', password: '' };

    showUserCrtPopup.value = false;
  }
};

const closePopup = () => {
  showUserCrtPopup.value = false;
};

const showLanguageTimezonePopup = ref(false);


const settings = ref({
  language: 'English',
  timezone: 'UTC',
});

const saveSettings = () => {
  console.log('Settings Saved:', settings.value);
  showLanguageTimezonePopup.value = false;
};
const showBackupPopup = ref(false);

// Backup settings state
const backupSettings = ref({
  frequency: 'Daily',
  time: '',
});

// Backup history data
const backupHistory = ref([
  { name: 'Backup_2024_11_25.zip', date: '25 Nov 2024', status: 'Completed' },
  { name: 'Backup_2024_11_24.zip', date: '24 Nov 2024', status: 'Completed' },
]);

const saveBackupSettings = () => {
  console.log('Backup Settings Saved:', backupSettings.value);
};

const handleFileUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    console.log('Selected file for restore:', file.name);
  }
};

const restoreData = () => {
  console.log('Restore data initiated.');
};

const downloadBackup = (fileName: string) => {
  console.log('Downloading backup:', fileName);
};

</script>

<style>
span {
  font-weight: normal;
}
</style>
