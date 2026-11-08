<template>
  <div>
    <!-- Main Reported Issues Popup -->
    <Popup
      :visible="showReportedIssuesPopup"
      @update:visible="(value: boolean) => emitEvent('update:showReportedIssuesPopup', value)"
    >
      <div class="p-4">
        <!-- Header -->
        <h2 class="mb-4 text-2xl font-bold">Reports Dashboard</h2>
        <div class="mb-4 flex items-center justify-between">
          <div class="flex w-full justify-evenly gap-2 rounded-lg bg-black/20 px-3 py-1.5">
            <button
              class="w-full rounded-md px-3 py-1.5 text-lg transition-all duration-300 ease-in-out"
              @click="activeTab = 'issues'"
              :class="['tab-btn', { 'bg-black text-white': activeTab === 'issues' }]"
            >
              Issues
            </button>
            <button
              class="w-full rounded-md px-3 py-1.5 text-lg transition-all duration-300 ease-in-out"
              @click="
                () => {
                  activeTab = 'production'
                  fetchProductionPerformance()
                }
              "
              :class="['tab-btn', { 'bg-black text-white': activeTab === 'production' }]"
            >
              Production
            </button>
            <button
              class="w-full rounded-md px-3 py-1.5 text-lg transition-all duration-300 ease-in-out"
              @click="
                () => {
                  activeTab = 'workflow'
                  fetchWorkflowAnalysis()
                }
              "
              :class="['tab-btn', { 'bg-black text-white': activeTab === 'workflow' }]"
            >
              Workflow
            </button>
            <button
              class="w-full rounded-md px-3 py-1.5 text-lg transition-all duration-300 ease-in-out"
              @click="
                () => {
                  activeTab = 'orders'
                  fetchOrderStatus()
                }
              "
              :class="['tab-btn', { 'bg-black text-white': activeTab === 'orders' }]"
            >
              Orders
            </button>
            <button
              class="w-full rounded-md px-3 py-1.5 text-lg transition-all duration-300 ease-in-out"
              @click="
                () => {
                  activeTab = 'stages'
                  fetchStageDurations()
                }
              "
              :class="['tab-btn', { 'bg-black text-white': activeTab === 'stages' }]"
            >
              Stages
            </button>
            <button
              class="w-full rounded-md px-3 py-1.5 text-lg transition-all duration-300 ease-in-out"
              @click="
                () => {
                  activeTab = 'scheduled'
                  fetchScheduledReports()
                }
              "
              :class="['tab-btn', { 'bg-black text-white': activeTab === 'scheduled' }]"
            >
              Scheduled
            </button>
          </div>
        </div>

        <!-- Issues Tab -->
        <div v-if="activeTab === 'issues'">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="text-xl font-semibold">Reported Issues</h3>
            <button
              @click="openNewIssuePopup"
              class="rounded bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700"
            >
              New Issue
            </button>
          </div>

          <!-- Filters -->
          <div class="mb-4 flex flex-wrap items-center gap-4">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by title, product, or keyword"
              class="w-full flex-1 rounded border px-4 py-2 sm:w-auto"
            />
            <select v-model="statusFilter" class="rounded border px-4 py-2">
              <option value="all">All Statuses</option>
              <option value="Active">Active</option>
              <option value="Resolved">Resolved</option>
            </select>
          </div>

          <!-- Issues Table -->
          <div class="overflow-x-auto">
            <table class="w-full text-center">
              <thead class="bg-blue-500 text-white">
                <tr>
                  <th class="border border-gray-700 px-4 py-2">Issue ID</th>
                  <th class="border border-gray-700 px-4 py-2">Category</th>
                  <th class="border border-gray-700 px-4 py-2">Priority</th>
                  <th class="border border-gray-700 px-4 py-2">Affected Item</th>
                  <th class="border border-gray-700 px-4 py-2">Time Stamp</th>
                  <th class="border border-gray-700 px-4 py-2">Status</th>
                  <th class="border border-gray-700 px-4 py-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in filteredIssues"
                  :key="item.id"
                  class="border bg-white hover:bg-gray-50"
                >
                  <td class="border border-gray-700 px-4 py-2">{{ item.id }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.category }}</td>
                  <td class="border border-gray-700 px-4 py-2">
                    <span
                      :class="[
                        'rounded-full px-2 py-1 text-xs font-semibold',
                        item.priority === 'high' || item.priority === 'critical'
                          ? 'bg-red-100 text-red-800'
                          : item.priority === 'medium'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-green-100 text-green-800',
                      ]"
                    >
                      {{ item.priority }}
                    </span>
                  </td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.affected_item }}</td>
                  <td class="border border-gray-700 px-4 py-2">
                    {{ formatDate(item.created_at) }}
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    <span
                      :class="[
                        'rounded-full px-2 py-1 text-xs font-semibold',
                        item.status === 'Active'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800',
                      ]"
                    >
                      {{ item.status || 'Active' }}
                    </span>
                  </td>
                  <td class="space-x-2 border border-gray-700 px-4 py-2">
                    <button
                      @click="openEditIssuePopup(item)"
                      class="rounded bg-yellow-500 px-2 py-1 text-white hover:bg-yellow-600"
                    >
                      Edit
                    </button>
                    <button
                      @click="confirmDeleteIssue(item.id)"
                      class="rounded bg-red-600 px-2 py-1 text-white hover:bg-red-700"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Production Performance Tab -->
        <div v-if="activeTab === 'production'" class="mt-4">
          <h3 class="mb-4 text-xl font-semibold">Production Performance</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-center">
              <thead class="bg-blue-500 text-white">
                <tr>
                  <th class="border border-gray-700 px-4 py-2">Production Line</th>
                  <th class="border border-gray-700 px-4 py-2">Total Orders</th>
                  <th class="border border-gray-700 px-4 py-2">Completed Orders</th>
                  <th class="border border-gray-700 px-4 py-2">Completion Rate</th>
                  <th class="border border-gray-700 px-4 py-2">Average Duration</th>
                  <th class="border border-gray-700 px-4 py-2">Delayed Orders</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in productionData"
                  :key="item.production_line"
                  class="border bg-white hover:bg-gray-50"
                >
                  <td class="border border-gray-700 px-4 py-2">{{ item.production_line }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.total_orders }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.completed_orders }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.completion_rate }}%</td>
                  <td class="border border-gray-700 px-4 py-2">
                    {{
                      item.average_duration
                        ? item.average_duration?.split(' ')?.[0] +
                          'days ,' +
                          item.average_duration?.split(' ')?.[1] +
                          'hours'
                        : '-'
                    }}
                  </td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.delayed_orders }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Workflow Analysis Tab -->
        <div v-if="activeTab === 'workflow'" class="mt-4">
          <h3 class="mb-4 text-xl font-semibold">Workflow Analysis</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-center">
              <thead class="bg-blue-500 text-white">
                <tr>
                  <th class="border border-gray-700 px-4 py-2">Workflow</th>
                  <th class="border border-gray-700 px-4 py-2">Total Stages</th>
                  <th class="border border-gray-700 px-4 py-2">Avg Duration</th>
                  <th class="border border-gray-700 px-4 py-2">Inspections</th>
                  <th class="border border-gray-700 px-4 py-2">Longest Stage</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in workflowData"
                  :key="item.workflow.id"
                  class="border bg-white hover:bg-gray-50"
                >
                  <td class="border border-gray-700 px-4 py-2">{{ item.workflow.name }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.total_stages }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.avg_stage_duration }}m</td>
                  <td class="border border-gray-700 px-4 py-2">
                    {{ item.total_inspection_points }}
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    <template v-if="item.longest_stage">
                      {{ item.longest_stage.name }} ({{ item.longest_stage.duration }}m)
                    </template>
                    <template v-else> - </template>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Order Status Tab -->
        <div v-if="activeTab === 'orders'" class="mt-4">
          <h3 class="mb-4 text-xl font-semibold">Order Status</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-center">
              <thead class="bg-blue-500 text-white">
                <tr>
                  <th class="border border-gray-700 px-4 py-2">Status</th>
                  <th class="border border-gray-700 px-4 py-2">Count</th>
                  <th class="border border-gray-700 px-4 py-2">Total Quantity</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in orderData"
                  :key="item.status"
                  class="border bg-white hover:bg-gray-50"
                >
                  <td class="border border-gray-700 px-4 py-2">{{ item.status }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.count }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.total_quantity }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Stage Durations Tab -->
        <div v-if="activeTab === 'stages'" class="mt-4">
          <h3 class="mb-4 text-xl font-semibold">Stage Durations</h3>
          <div class="mb-4">
            <input
              v-model="workflowFilter"
              type="text"
              placeholder="Filter by workflow..."
              class="rounded border px-4 py-2"
            />
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-center">
              <thead class="bg-blue-500 text-white">
                <tr>
                  <th class="border border-gray-700 px-4 py-2">Workflow</th>
                  <th class="border border-gray-700 px-4 py-2">Stage</th>
                  <th class="border border-gray-700 px-4 py-2">Avg</th>
                  <th class="border border-gray-700 px-4 py-2">Min</th>
                  <th class="border border-gray-700 px-4 py-2">Max</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in filteredStageData"
                  :key="item.workflow_name + item.stage_name"
                  class="border bg-white hover:bg-gray-50"
                >
                  <td class="border border-gray-700 px-4 py-2">{{ item.workflow_name }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.stage_name }}</td>
                  <td class="border border-gray-700 px-4 py-2">
                    <span class="font-medium">{{ item.avg_duration_minutes }}m</span>
                    <span class="block text-xs text-gray-500"
                      >{{ item.avg_duration_seconds }}s</span
                    >
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    <span class="font-medium">{{ item.min_duration_minutes }}m</span>
                    <span class="block text-xs text-gray-500"
                      >{{ item.min_duration_seconds }}s</span
                    >
                  </td>
                  <td class="border border-gray-700 px-4 py-2">
                    <span class="font-medium">{{ item.max_duration_minutes }}m</span>
                    <span class="block text-xs text-gray-500"
                      >{{ item.max_duration_seconds }}s</span
                    >
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Scheduled Reports Tab -->
        <div v-if="activeTab === 'scheduled'" class="mt-4">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="text-xl font-semibold">Scheduled Reports</h3>
            <button
              @click="openNewScheduledReportPopup"
              class="rounded bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700"
            >
              New Schedule
            </button>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-center">
              <thead class="bg-blue-500 text-white">
                <tr>
                  <th class="border border-gray-700 px-4 py-2">Report Type</th>
                  <th class="border border-gray-700 px-4 py-2">Frequency</th>
                  <th class="border border-gray-700 px-4 py-2">Recipients</th>
                  <th class="border border-gray-700 px-4 py-2">Next Run</th>
                  <th class="border border-gray-700 px-4 py-2">Status</th>
                  <th class="border border-gray-700 px-4 py-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in scheduledData"
                  :key="item.id"
                  class="border bg-white hover:bg-gray-50"
                >
                  <td class="border border-gray-700 px-4 py-2">
                    {{ reportTypes[item.report_type] || item.report_type }}
                  </td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.frequency }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ item.recipients }}</td>
                  <td class="border border-gray-700 px-4 py-2">{{ formatDate(item.next_run) }}</td>
                  <td class="border border-gray-700 px-4 py-2">
                    <span
                      :class="[
                        'rounded-full px-2 py-1 text-xs font-semibold',
                        item.is_active
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800',
                      ]"
                    >
                      {{ item.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td class="space-x-2 border border-gray-700 px-4 py-2">
                    <button
                      @click="openEditScheduledReportPopup(item)"
                      class="rounded bg-yellow-500 px-2 py-1 text-white hover:bg-yellow-600"
                    >
                      Edit
                    </button>
                    <button
                      @click="confirmDeleteScheduledReport(item.id)"
                      class="rounded bg-red-600 px-2 py-1 text-white hover:bg-red-700"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Popup>

    <!-- Issue Form Popup -->
    <Popup :visible="showIssueFormPopup" @update:visible="showIssueFormPopup = $event">
      <div class="p-4">
        <h2 class="mb-4 text-xl font-semibold">
          {{ currentIssueId ? 'Edit Issue' : 'Submit an Issue' }}
        </h2>

        <form @submit.prevent="submitIssue" class="space-y-4">
          <!-- Issue Category -->
          <div>
            <label class="mb-1 block font-medium">Issue Category</label>
            <select
              v-model="issueForm.category"
              class="w-full rounded border px-3 py-2 focus:outline-none"
              required
            >
              <option value="">Select Category</option>
              <option value="Equipment">Equipment</option>
              <option value="Production">Production</option>
              <option value="Quality">Quality</option>
              <option value="Maintenance">Maintenance</option>
            </select>
          </div>

          <!-- Affected Workflow -->
          <div>
            <label class="mb-1 block font-medium">Affected Item</label>
            <input
              type="text"
              v-model="issueForm.affected_item"
              placeholder="Assembly Line 1"
              class="w-full rounded border px-3 py-2 focus:outline-none"
              required
            />
          </div>

          <!-- Urgency -->
          <div>
            <label class="mb-1 block font-medium">Priority</label>
            <div class="flex flex-wrap gap-4">
              <label
                v-for="priority in ['low', 'medium', 'high', 'critical']"
                :key="priority"
                class="flex items-center gap-1"
              >
                <input
                  type="radio"
                  v-model="issueForm.priority"
                  :value="priority"
                  class="h-4 w-4"
                  required
                />
                <span class="capitalize">{{ priority }}</span>
              </label>
            </div>
          </div>

          <!-- Description -->
          <div>
            <label class="mb-1 block font-medium">Description</label>
            <textarea
              v-model="issueForm.description"
              rows="5"
              class="w-full rounded border px-3 py-2 focus:outline-none"
              placeholder="Enter issue description..."
              required
            ></textarea>
          </div>

          <!-- Actions -->
          <div class="mt-4 flex justify-end gap-2">
            <button
              type="button"
              @click="showIssueFormPopup = false"
              class="rounded bg-gray-500 px-4 py-2 text-white hover:bg-gray-600"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
              :disabled="submitting"
            >
              {{ submitting ? 'Saving...' : currentIssueId ? 'Update Issue' : 'Submit Issue' }}
            </button>
          </div>
        </form>
      </div>
    </Popup>

    <!-- Scheduled Report Form Popup -->
    <Popup
      :visible="showScheduledReportFormPopup"
      @update:visible="showScheduledReportFormPopup = $event"
    >
      <div class="p-4">
        <h2 class="mb-4 text-xl font-semibold">
          {{ currentScheduledReportId ? 'Edit Scheduled Report' : 'New Scheduled Report' }}
        </h2>

        <form @submit.prevent="submitScheduledReport" class="space-y-4">
          <!-- Report Type -->
          <div>
            <label class="mb-1 block font-medium">Report Type</label>
            <select
              v-model="scheduledReportForm.report_type"
              class="w-full rounded border px-3 py-2 focus:outline-none"
              required
            >
              <option value="production_performance">Production Performance</option>
              <option value="workflow_analysis">Workflow Analysis</option>
              <option value="order_status">Order Status</option>
              <option value="stage_durations">Stage Durations</option>
            </select>
          </div>

          <!-- Frequency -->
          <div>
            <label class="mb-1 block font-medium">Frequency</label>
            <select
              v-model="scheduledReportForm.frequency"
              class="w-full rounded border px-3 py-2 focus:outline-none"
              required
            >
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>

          <!-- Recipients -->
          <div>
            <label class="mb-1 block font-medium">Recipients (comma separated)</label>
            <input
              type="text"
              v-model="scheduledReportForm.recipients"
              placeholder="email1@example.com, email2@example.com"
              class="w-full rounded border px-3 py-2 focus:outline-none"
              required
            />
          </div>

          <!-- Next Run -->
          <div>
            <label class="mb-1 block font-medium">Next Run</label>
            <input
              type="datetime-local"
              v-model="scheduledReportForm.next_run"
              class="w-full rounded border px-3 py-2 focus:outline-none"
              required
            />
          </div>

          <!-- Status -->
          <div>
            <label class="mb-1 block font-medium">Status</label>
            <div class="flex items-center gap-2">
              <input
                type="checkbox"
                v-model="scheduledReportForm.is_active"
                id="is_active"
                class="h-4 w-4"
              />
              <label for="is_active">Active</label>
            </div>
          </div>

          <!-- Actions -->
          <div class="mt-4 flex justify-end gap-2">
            <button
              type="button"
              @click="showScheduledReportFormPopup = false"
              class="rounded bg-gray-500 px-4 py-2 text-white hover:bg-gray-600"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
              :disabled="submitting"
            >
              {{ submitting ? 'Saving...' : currentScheduledReportId ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </Popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Popup from '@/components/popup.vue'
import { useTimeAgo } from '@vueuse/core'
import { baseApiUrl } from '@/api'
// Convert Django duration string to seconds
const API_BASE_URL = `${baseApiUrl}/reports/`

// Props and emits
const props = defineProps<{
  showReportedIssuesPopup: boolean
}>()

const emitEvent = defineEmits(['update:showReportedIssuesPopup'])

// Tab management
const activeTab = ref('issues')

// Common state
const submitting = ref(false)

// ==================== Reported Issues ====================
const issues = ref<any[]>([])
const issuesLoading = ref(false)
const issuesError = ref<string | null>(null)
const searchQuery = ref('')
const statusFilter = ref('all')
const showIssueFormPopup = ref(false)
const currentIssueId = ref<number | null>(null)
const issueForm = ref({
  category: '',
  affected_item: '',
  priority: '',
  description: '',
})

const filteredIssues = computed(() => {
  return issues.value.filter((issue) => {
    const matchesSearch =
      issue.category.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      issue.affected_item.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      issue.description.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesStatus =
      statusFilter.value === 'all' ||
      (issue.status || 'Active').toLowerCase() === statusFilter.value.toLowerCase()

    return matchesSearch && matchesStatus
  })
})

interface Issue {
  id: number
  category: string
  affected_item: string
  priority: string
  description: string
  created_at: string
  status?: string
}

interface StageData {
  workflow_name: string
  stage_name: string
  avg_duration_minutes: number
  avg_duration_seconds: number
  min_duration_minutes: number
  min_duration_seconds: number
  max_duration_minutes: number
  max_duration_seconds: number
}

interface ScheduledReport {
  id: number
  report_type: string
  frequency: string
  recipients: string
  next_run: string
  is_active: boolean
}

interface ProductionData {
  production_line: string
  total_orders: number
  completed_orders: number
  completion_rate: number
  average_duration?: string
  delayed_orders: number
}

interface WorkflowData {
  workflow: {
    id: number
    name: string
  }
  total_stages: number
  avg_stage_duration: number
  total_inspection_points: number
  longest_stage?: {
    name: string
    duration: number
  }
}

interface OrderData {
  status: string
  count: number
  total_quantity: number
}

const formatMinutes = (minutes: number): string => {
  return `${Math.round(minutes)}m`
}
const formatSeconds = (seconds: number): string => {
  if (seconds < 60) return `${seconds}s`

  const hours: number = Math.floor(seconds / 3600)
  const remainingMinutes: number = Math.floor((seconds % 3600) / 60)

  return hours > 0 ? `${hours}h ${remainingMinutes}m` : `${remainingMinutes}m`
}

const fetchIssues = async () => {
  try {
    issuesLoading.value = true
    issuesError.value = null
    const response = await axios.get(`${API_BASE_URL}issues/`)
    issues.value = response.data
  } catch (err) {
    issuesError.value = 'Failed to fetch issues'
    console.error('Error fetching issues:', err)
  } finally {
    issuesLoading.value = false
  }
}

const openNewIssuePopup = () => {
  issueForm.value = {
    category: '',
    affected_item: '',
    priority: '',
    description: '',
  }
  currentIssueId.value = null
  showIssueFormPopup.value = true
}

const openEditIssuePopup = (issue: any) => {
  currentIssueId.value = issue.id
  issueForm.value = {
    category: issue.category,
    affected_item: issue.affected_item,
    priority: issue.priority,
    description: issue.description,
  }
  showIssueFormPopup.value = true
}

const confirmDeleteIssue = (id: number) => {
  if (confirm('Are you sure you want to delete this issue?')) {
    deleteIssue(id)
  }
}

const deleteIssue = async (id: number) => {
  try {
    await axios.delete(`${API_BASE_URL}issues/${id}/`)
    issues.value = issues.value.filter((issue) => issue.id !== id)
  } catch (err) {
    issuesError.value = 'Failed to delete issue'
    console.error('Error deleting issue:', err)
  }
}

const submitIssue = async () => {
  try {
    submitting.value = true
    const payload = {
      category: issueForm.value.category,
      affected_item: issueForm.value.affected_item,
      priority: issueForm.value.priority,
      description: issueForm.value.description,
    }

    if (currentIssueId.value) {
      const response = await axios.put(`${API_BASE_URL}issues/${currentIssueId.value}/`, payload)
      const index = issues.value.findIndex((i) => i.id === currentIssueId.value)
      if (index !== -1) {
        issues.value[index] = response.data
      }
    } else {
      const response = await axios.post(`${API_BASE_URL}issues/`, payload)
      issues.value.unshift(response.data)
    }
    showIssueFormPopup.value = false
  } catch (err) {
    issuesError.value = currentIssueId.value ? 'Failed to update issue' : 'Failed to create issue'
    console.error('Error submitting issue:', err)
  } finally {
    submitting.value = false
  }
}

// ==================== Production Performance ====================
const productionData = ref<any[]>([])
const productionLoading = ref(false)
const productionError = ref<string | null>(null)

const fetchProductionPerformance = async () => {
  try {
    productionLoading.value = true
    productionError.value = null
    const response = await axios.get(`${API_BASE_URL}production/performance/`)
    productionData.value = response.data
  } catch (err) {
    productionError.value = 'Failed to fetch production performance data'
    console.error('Error fetching production performance:', err)
  } finally {
    productionLoading.value = false
  }
}

// ==================== Workflow Analysis ====================
const workflowData = ref<any[]>([])
const workflowLoading = ref(false)
const workflowError = ref<string | null>(null)

const fetchWorkflowAnalysis = async () => {
  try {
    workflowLoading.value = true
    workflowError.value = null
    const response = await axios.get(`${API_BASE_URL}workflow/analysis/`)
    workflowData.value = response.data
  } catch (err) {
    workflowError.value = 'Failed to fetch workflow analysis data'
    console.error('Error fetching workflow analysis:', err)
  } finally {
    workflowLoading.value = false
  }
}

// ==================== Order Status ====================
const orderData = ref<any[]>([])
const orderLoading = ref(false)
const orderError = ref<string | null>(null)

const fetchOrderStatus = async () => {
  try {
    orderLoading.value = true
    orderError.value = null
    const response = await axios.get(`${API_BASE_URL}orders/status/`)
    orderData.value = response.data
  } catch (err) {
    orderError.value = 'Failed to fetch order status data'
    console.error('Error fetching order status:', err)
  } finally {
    orderLoading.value = false
  }
}

// ==================== Stage Durations ====================
const stageData = ref<any[]>([])
const stageLoading = ref(false)
const stageError = ref<string | null>(null)
const workflowFilter = ref('')

const fetchStageDurations = async () => {
  try {
    stageLoading.value = true
    stageError.value = null
    const response = await axios.get(`${API_BASE_URL}stages/durations/`)
    stageData.value = response.data
  } catch (err) {
    stageError.value = 'Failed to fetch stage durations data'
    console.error('Error fetching stage durations:', err)
  } finally {
    stageLoading.value = false
  }
}

const filteredStageData = computed(() => {
  const filter = workflowFilter.value.toLowerCase()
  return stageData.value.filter(
    (item) =>
      !filter ||
      item.workflow_name.toLowerCase().includes(filter) ||
      item.stage_name.toLowerCase().includes(filter),
  )
})
// ==================== Scheduled Reports ====================
const scheduledData = ref<any[]>([])
const scheduledLoading = ref(false)
const scheduledError = ref<string | null>(null)
const showScheduledReportFormPopup = ref(false)
const currentScheduledReportId = ref<number | null>(null)
const scheduledReportForm = ref({
  report_type: 'production_performance',
  frequency: 'weekly',
  recipients: '',
  next_run: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().slice(0, 16),
  is_active: true,
})

const reportTypes: Record<string, string> = {
  production_performance: 'Production Performance',
  workflow_analysis: 'Workflow Analysis',
  order_status: 'Order Status',
  stage_durations: 'Stage Durations',
}

const fetchScheduledReports = async () => {
  try {
    scheduledLoading.value = true
    scheduledError.value = null
    const response = await axios.get(`${API_BASE_URL}scheduled/`)
    scheduledData.value = response.data
  } catch (err) {
    scheduledError.value = 'Failed to fetch scheduled reports'
    console.error('Error fetching scheduled reports:', err)
  } finally {
    scheduledLoading.value = false
  }
}

const openNewScheduledReportPopup = () => {
  scheduledReportForm.value = {
    report_type: 'production_performance',
    frequency: 'weekly',
    recipients: '',
    next_run: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().slice(0, 16),
    is_active: true,
  }
  currentScheduledReportId.value = null
  showScheduledReportFormPopup.value = true
}

const openEditScheduledReportPopup = (report: any) => {
  currentScheduledReportId.value = report.id
  scheduledReportForm.value = {
    report_type: report.report_type,
    frequency: report.frequency,
    recipients: report.recipients,
    next_run: report.next_run.slice(0, 16),
    is_active: report.is_active,
  }
  showScheduledReportFormPopup.value = true
}

const confirmDeleteScheduledReport = (id: number) => {
  if (confirm('Are you sure you want to delete this scheduled report?')) {
    deleteScheduledReport(id)
  }
}

const deleteScheduledReport = async (id: number) => {
  try {
    await axios.delete(`${API_BASE_URL}scheduled/${id}/`)
    scheduledData.value = scheduledData.value.filter((r) => r.id !== id)
  } catch (err) {
    scheduledError.value = 'Failed to delete scheduled report'
    console.error('Error deleting scheduled report:', err)
  }
}

const submitScheduledReport = async () => {
  try {
    submitting.value = true
    const payload = {
      report_type: scheduledReportForm.value.report_type,
      frequency: scheduledReportForm.value.frequency,
      recipients: scheduledReportForm.value.recipients,
      next_run: scheduledReportForm.value.next_run,
      is_active: scheduledReportForm.value.is_active,
    }

    if (currentScheduledReportId.value) {
      const response = await axios.put(
        `${API_BASE_URL}scheduled/${currentScheduledReportId.value}/`,
        payload,
      )
      const index = scheduledData.value.findIndex((r) => r.id === currentScheduledReportId.value)
      if (index !== -1) {
        scheduledData.value[index] = response.data
      }
    } else {
      const response = await axios.post(`${API_BASE_URL}scheduled/`, payload)
      scheduledData.value.unshift(response.data)
    }
    showScheduledReportFormPopup.value = false
  } catch (err) {
    scheduledError.value = currentScheduledReportId.value
      ? 'Failed to update scheduled report'
      : 'Failed to create scheduled report'
    console.error('Error submitting scheduled report:', err)
  } finally {
    submitting.value = false
  }
}

// Helper functions
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

// Initialize data
onMounted(() => {
  fetchIssues()
})
</script>

<style scoped></style>
