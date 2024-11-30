<template>
    <div class="w-full">
     <div class="pl-3 pb-2 h-fit">
      <div class="flex w-full flex-col">
        <div class="flex w-full justify-between px-2 pt-4">
          <img src="../assets/noti.png" class="size-11 cursor-pointer"alt="">
          
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
          focusable="false"
        >
          <path d="M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0"></path>
          <path d="M21 21l-6 -6"></path>
        </svg>
            <p>Search</p>
          </div>
          <img src="../assets/avatar.png" alt="" class="size-12 cursor-pointer">
        </div>
  
        
      </div>
    </div>
    <div class="flex flex-col m-2 p-4 justify-center rounded-2xl bg-gray-200 ">
        <p class="text-xl font-bold flex justify-center">System Administraion</p>
        
        <div class="flex flex-row py-4 gap-20">
            <div class="flex flex-col bg-gray-100 rounded-lg p-2  w-3/6">
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
                <div class="flex flex-col font-bold  pt-2 space-y-1">
                    <p>Activity Log</p>
                    <button class="bg-green-600 h-fit w-fit p-2 rounded-md font-normal text-white">View Full Activity Log</button>
                    <p>Last Login Information</p>
                    <span>Last Login: 11/24/2024, 10:30 AM</span>
                    <p>Your Last Login</p>
                    <span>Last Login: 11/24/2024, 09:45 AM</span>
                </div>
            </div>  
        </div>

        <div class="flex flex-col items-center bg-[#bee8ea] border rounded-xl w-fit p-6 cursor-pointer shadow-md sh shadow-gray-500">
            
            <img src="../assets/user_manage.png" class=" size-20"alt="">
            <p class="font-bold text-[13px] pt-2 ">User Management</p>
            
        </div>

        <div class="flex justify-end gap-10 py-2">
            <div class="flex flex-col items-center justify-evenly bg-[#bee8ea] border rounded-xl w-fit p-2 cursor-pointer shadow-md shadow-gray-500">
                <img src="../assets/settings.png" class="size-10" alt="">
                <p class="font-bold text-[10px] pt-2">Language & Time</p>

            </div>
            <div class="flex flex-col items-center bg-[#bee8ea] border rounded-xl w-fit p-2 cursor-pointer shadow-md shadow-gray-500">
                <img src="../assets/backup.png" class="size-10"alt="">
                <p class="font-bold text-[10px] pt-2">Backup & Restore</p>
            </div>
        </div>
    </div>
    </div>
    
  </template>
  
  <script setup lang="ts">
  
  </script>

  <style>
    span{
        font-weight: normal;
    }
  </style>