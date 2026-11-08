import { reactive, computed } from 'vue'
import axios from 'axios'
import { notificationsUrl } from '@/api'

type LocalNotification = {
  id: string
  title: string
  body: string
  type: 'success' | 'error' | 'info'
  role: string
  isRead: boolean
  time: string
}

type ServerNotification = {
  id: number
  message: string
  is_read: boolean
  created_at: string
  url: string | null
}

const API_BASE = `${notificationsUrl}/`

const state = reactive({
  local: [] as LocalNotification[],
  server: [] as ServerNotification[],
  loading: false,
  error: '',
})

// Call signature used across the stores:
// notificationStore.addNotification(message, type, role)
const addNotification = (
  message: string,
  type: 'success' | 'error' | 'info' = 'info',
  role = '',
): void => {
  state.local.unshift({
    id: `local-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
    title: message,
    body: '',
    type,
    role,
    isRead: false,
    time: new Date().toLocaleTimeString(),
  })
}

const fetchServerNotifications = async (userId: number | string): Promise<void> => {
  state.loading = true
  state.error = ''
  try {
    const { data } = await axios.get(`${API_BASE}?user=${userId}`)
    state.server = Array.isArray(data) ? data : []
  } catch {
    state.error = 'Failed to load notifications'
  } finally {
    state.loading = false
  }
}

const markAsRead = async (id: string | number): Promise<void> => {
  const serverItem = state.server.find((n) => String(n.id) === String(id))
  if (serverItem) {
    serverItem.is_read = true
    try {
      await axios.patch(`${API_BASE}${serverItem.id}/`, { is_read: true })
    } catch {
      // keep the local read state even if the request fails
    }
    return
  }
  const localItem = state.local.find((n) => n.id === id)
  if (localItem) {
    localItem.isRead = true
  }
}

const notifications = computed(() => [
  ...state.server.map((n) => ({
    id: String(n.id),
    title: n.message,
    body: n.url ?? '',
    type: 'info' as const,
    isRead: n.is_read,
    time: new Date(n.created_at).toLocaleString(),
  })),
  ...state.local,
])

const unreadCount = computed(
  () => notifications.value.filter((n) => !n.isRead).length,
)

const clearLocal = (): void => {
  state.local = []
}

const notificationStore = {
  state,
  addNotification,
  fetchServerNotifications,
  markAsRead,
  get notifications() {
    return notifications.value
  },
  get unreadCount() {
    return unreadCount.value
  },
  clearLocal,
}

export default notificationStore
