<template>
  <section class="bg-[#F0F0F0]">
    <div class="mx-auto flex flex-col items-center justify-center px-6 py-8 md:h-screen lg:py-0">
      <a href="#" class="mb-6 flex items-center text-2xl font-semibold text-black">
        <img class="mr-2 h-8 w-8" src="../assets/FPMS.png" alt="logo" />
        FPMS
      </a>
      <div
        class="w-full rounded-xl border border-gray-700 bg-white shadow sm:max-w-md md:mt-0 xl:p-0"
      >
        <div class="space-y-4 rounded-xl bg-[#FFFFFF] p-6 sm:p-8 md:space-y-6">
          <h1 class="text-xl leading-tight font-bold tracking-tight text-black md:text-2xl">
            Sign in to your account
          </h1>
          <form class="space-y-4 md:space-y-6" @submit.prevent="handleLogin">
            <div>
              <label for="email" class="mb-2 block text-sm font-medium text-black"
                >Your Email</label
              >
              <input
                type="email"
                name="email"
                id="email"
                v-model="loginForm.email"
                class="focus:ring-primary-600 focus:border-primary-600 block w-full rounded-xl border border-gray-600 bg-[#CCCCCC] p-2.5 text-black placeholder-gray-400 focus:border-blue-500 focus:ring-blue-500"
                placeholder="Email"
                required
              />
            </div>
            <div>
              <label for="password" class="mb-2 block text-sm font-medium text-black"
                >Password</label
              >
              <input
                type="password"
                name="password"
                id="password"
                v-model="loginForm.password"
                placeholder="••••••••"
                class="focus:ring-primary-600 focus:border-primary-600 block w-full rounded-xl border border-gray-600 bg-[#CCCCCC] p-2.5 text-black placeholder-gray-400 focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>

            <button
              type="submit"
              class="focus:ring-primary-300 hover:bg-primary-700 focus:ring-primary-800 w-full cursor-pointer rounded-xl bg-[#F0F0F0] px-5 py-2.5 text-center text-sm font-medium text-black hover:bg-gray-200 focus:ring-4 focus:outline-none"
              :disabled="loading"
            >
              <span v-if="!loading">Sign in</span>
              <span v-else>Signing in...</span>
            </button>
            <!-- <div v-if="error" class="text-red-500 text-sm">
            </div> -->
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { baseApiUrl } from '@/api'
import { useUserStore, type UserType } from '@/stores/user'
import { useAxios } from '@vueuse/integrations/useAxios'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const loginForm = reactive({
  email: '',
  password: '',
})
const loading = ref(false)

const router = useRouter() // Initialize the router instance

const handleLogin = async () => {
  const { data } = await useAxios<{
    user: UserType
    access: string
    refresh: string
  }>(`${baseApiUrl}/admin/users/login/`, {
    method: 'POST',
    data: loginForm,
  })

  const userStore = useUserStore()
  if (data.value) {
    userStore.setUser(data.value.user, data.value.access, data.value.refresh)

    // Role-based route mapping
    const roleRoutes = {
      'Quality Control Manager': { name: 'quality' },
      'Quality Control Inspector': { name: 'reports' },
      Admin: { name: 'home' },
      'Production Planner': { name: 'production' },
      'Production Manager': { name: 'workcenters' },
      '404': { name: 'not-found' },
    }
    const role = (userStore?.user?.role || '404') as keyof typeof roleRoutes
    const route = roleRoutes[role]
    if (route) router.push({ name: route.name }) // Use the router instance to navigate
  }
}
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
