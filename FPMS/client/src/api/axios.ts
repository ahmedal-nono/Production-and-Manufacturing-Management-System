import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios'
import { baseApiUrl } from '@/api'
import { useUserStore } from '@/stores/user'

const apiOrigin = baseApiUrl.replace(/\/api\/?$/, '')
const refreshUrl = `${apiOrigin}/token/refresh/`

let refreshPromise: Promise<string | null> | null = null

async function refreshAccessToken(refresh: string): Promise<string | null> {
  try {
    const { data } = await axios.post<{ access?: string; refresh?: string }>(
      refreshUrl,
      { refresh },
    )
    if (data.refresh) {
      const store = useUserStore()
      store.refresh = data.refresh
    }
    return data.access ?? null
  } catch {
    return null
  }
}

axios.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const store = useUserStore()
  if (store.access) {
    config.headers.set('Authorization', `Bearer ${store.access}`)
  }
  return config
})

axios.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const store = useUserStore()
    const original = error.config as
      | (InternalAxiosRequestConfig & { _retry?: boolean })
      | undefined
    const status = error.response?.status
    const url = original?.url ?? ''

    const isAuthEndpoint = url.includes('/login/') || url.includes('/token/refresh/')

    if (
      status === 401 &&
      original &&
      !original._retry &&
      store.refresh &&
      !isAuthEndpoint
    ) {
      original._retry = true
      if (!refreshPromise) {
        refreshPromise = refreshAccessToken(store.refresh).finally(() => {
          refreshPromise = null
        })
      }
      const newAccess = await refreshPromise
      if (newAccess) {
        store.access = newAccess
        return axios(original)
      }
      store.logout()
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  },
)

export default axios
