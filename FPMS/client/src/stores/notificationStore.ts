type Notification = {
  id: string // Unique identifier for each notification
  message: string
  type: 'success' | 'error' | 'info'
  role: string
  isRead: boolean // Track read status
}

class NotificationStore {
  public notifications: Notification[] = [] // Array to store notifications

  // Add a notification
  addNotification(
    id: string,
    message: string,
    type: 'success' | 'error' | 'info',
    role: string,
  ): void {
    this.notifications.push({ id, message, type, role, isRead: false })
  }

  // Get notifications for a specific role
  getNotificationsForRole(role: string): Notification[] {
    return this.notifications.filter((notification) => notification.role === role)
  }

  // Mark a notification as read
  markNotificationAsRead(id: string): void {
    const notification = this.notifications.find((notification) => notification.id === id)
    if (notification) {
      notification.isRead = true
    }
  }

  // Clear notifications (optional)
  clearNotifications(): void {
    this.notifications = []
  }
}

// Export a singleton instance of the store
const notificationStore = new NotificationStore()
export default notificationStore
