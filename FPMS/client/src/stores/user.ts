import { defineStore } from 'pinia'

interface User {
  id: number
  name: string
  email: string
}

interface UserState {
  user: User | null
  token: string | null
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    token: null,
  }),
  actions: {
    setUser(user: User, token: string) {
      this.user = user
      this.token = token
    },
    logout() {
      this.user = null
      this.token = null
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.user && !!state.token,
  },
})
