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
          <form class="space-y-4 md:space-y-6" action="#">
            <div>
              <label for="username" class="mb-2 block text-sm font-medium text-black"
                >Your Username</label
              >
              <input
                type="username"
                name="username"
                id="username"
                class="focus:ring-primary-600 focus:border-primary-600 block w-full rounded-xl border border-gray-600 bg-[#CCCCCC] p-2.5 text-black placeholder-gray-400 focus:border-blue-500 focus:ring-blue-500"
                placeholder="Username"
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
                placeholder="••••••••"
                class="focus:ring-primary-600 focus:border-primary-600 block w-full rounded-xl border border-gray-600 bg-[#CCCCCC] p-2.5 text-black placeholder-gray-400 focus:border-blue-500 focus:ring-blue-500"
              />
            </div>

            <button
              type="submit"
              class="focus:ring-primary-300 hover:bg-primary-700 focus:ring-primary-800 w-full cursor-pointer rounded-xl bg-[#F0F0F0] px-5 py-2.5 text-center text-sm font-medium text-black hover:bg-gray-200 focus:ring-4 focus:outline-none"
            >
              Sign in
            </button>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<style>
button {
  cursor: pointer;
}
</style>
