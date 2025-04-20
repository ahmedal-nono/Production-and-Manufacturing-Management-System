import { defineStore } from 'pinia'


export interface UserType {
  id: string
  full_name: string
  email: string
  contact_number: string
  account_status: boolean
  department: string
  role: string
}

interface UserState {
  user: UserType | null
  access: string | null
  refresh: string | null
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    access: null,
    refresh: null,
  }),
  actions: {
    setUser(user: UserType, access: string, refresh: string) {
      this.user = user;
      this.access = access;
      this.refresh = refresh;
      localStorage.setItem('user', JSON.stringify(user))
    },
    logout() {
      this.user = null;
      this.access = null;
      this.refresh = null;
    },
  },
  getters: {
    isAuthenticated: (state) => {
      return !!state.user && !!state.access;
    },
  },
  persist: true,
})
