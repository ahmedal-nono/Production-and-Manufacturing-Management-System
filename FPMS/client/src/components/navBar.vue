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
          <div class="flex cursor-pointer space-x-2 border-black bg-white rounded-xl w-4/12 p-4">
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
              class="chakra-icon css-ugv5hc"
            >
              <path d="M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0"></path>
              <path d="M21 21l-6 -6"></path>
            </svg>
            <p>Search</p>
          </div>
          <img src="../assets/avatar.png" alt="" class="size-12 cursor-pointer" />
        </div>
      </div>
    </div>
    <!-- for modules later-->
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
            <button class="bg-green-600 h-fit w-fit p-2 rounded-md font-normal text-white">View Full Activity Log</button>
            <p>Last Login Information</p>
            <span>Last Login: 11/24/2024, 10:30 AM</span>
            <p>Your Last Login</p>
            <span>Last Login: 11/24/2024, 09:45 AM</span>
          </div>
        </div>
      </div>
      <div class="flex flex-col items-center bg-[#bee8ea] border rounded-xl w-fit p-6 cursor-pointer shadow-md shadow-gray-500">
        <img src="../assets/user_manage.png" class="size-20" alt="" />
        <p class="font-bold text-[13px] pt-2">User Management</p>
      </div>
      <div class="flex justify-end gap-10 py-2">
        <div class="flex flex-col items-center justify-evenly bg-[#bee8ea] border rounded-xl w-fit p-2 cursor-pointer shadow-md shadow-gray-500">
          <img src="../assets/settings.png" class="size-10" alt="" />
          <p class="font-bold text-[10px] pt-2">Language & Time</p>
        </div>
        <div class="flex flex-col items-center bg-[#bee8ea] border rounded-xl w-fit p-2 cursor-pointer shadow-md shadow-gray-500">
          <img src="../assets/backup.png" class="size-10" alt="" />
          <p class="font-bold text-[10px] pt-2">Backup & Restore</p>
        </div>
      </div>
    </div>
    <!-- for modules later-->
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Popup from '../components/popup.vue';

const showPopup = ref(false);
const isRead = ref(false);
const isReadSecond = ref(false);

function markAsRead() {
  isRead.value = true;
}

function markAsReadSecond() {
  isReadSecond.value = true;
}
</script>

<style>
span {
  font-weight: normal;
}
</style>
