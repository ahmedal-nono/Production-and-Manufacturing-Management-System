import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

type Notification = {
  id: string // Unique identifier for each notification
  title: string // Title of the notification
  body: string // Body of the notification
  type: 'success' | 'error' | 'info'
  role: string // Role of the user
  isRead: boolean // Track read status
}

export function useNotificationStore() {
  const notifications = ref<Notification[]>([]) // Reactive array to store notifications

  // Add a notification
  const addNotification = (
    id: string,
    title: string,
    body: string,
    type: 'success' | 'error' | 'info',
  ) => {
    const userRole = useUserStore().role // Fetch the role from user store
    notifications.value.push({ id, title, body, type, role: userRole, isRead: false })
  }

  // Get notifications for a specific role
  const getNotificationsForRole = (role: string): Notification[] => {
    return notifications.value.filter((notification) => notification.role === role)
  }

  // Mark a notification as read
  const markNotificationAsRead = (id: string): void => {
    const notification = notifications.value.find((notification) => notification.id === id)
    if (notification) {
      notification.isRead = true
    }
  }

  // Clear notifications (optional)
  const clearNotifications = (): void => {
    notifications.value = []
  }

  return {
    notifications,
    addNotification,
    getNotificationsForRole,
    markNotificationAsRead,
    clearNotifications,
  }
}
