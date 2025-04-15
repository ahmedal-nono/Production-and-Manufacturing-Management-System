<template>
  <Popup
    :visible="showReportedIssuesPopup"
    @update:visible="(value: boolean) => emitEvent('update:showReportedIssuesPopup', value)"
  >
    <div class="">
      <!-- Header -->
      <div class="mb-4 flex items-center justify-between">
        <h2 class="text-2xl font-bold">Reports</h2>
        <button
          @click="showNewIssuePopup = true"
          class="m-2 mt-4 cursor-pointer rounded-lg bg-blue-600 p-1.5 text-white"
        >
          New Issue
        </button>
      </div>

      <!-- Filters -->
      <div class="mb-4 flex flex-wrap items-center gap-4">
        <input
          type="text"
          placeholder="Search by title, product, or keyword"
          class="w-full flex-1 rounded border px-4 py-2 sm:w-auto"
        />
        <select class="rounded border px-4 py-2">
          <option>All Statuses</option>
        </select>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr class="">
              <th class="border border-gray-700 px-4 py-2">Issue ID</th>
              <th class="border border-gray-700 px-4 py-2">Category</th>
              <th class="border border-gray-700 px-4 py-2">Priority</th>
              <th class="border border-gray-700 px-4 py-2">Affected Workflow/Job card</th>
              <th class="border border-gray-700 px-4 py-2">Time Stamp</th>
              <th class="border border-gray-700 px-4 py-2">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, index) in instructions"
              :key="index"
              class="border bg-white hover:bg-gray-50"
            >
              <td class="border border-gray-700 px-4 py-2">{{ item.id }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ item.product }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ item.quantity }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ item.dueDate }}</td>
              <td class="border border-gray-700 px-4 py-2">
                <input readonly disabled type="date" name="" id="" value="22/03/2025" />
              </td>
              <td class="border border-gray-700 px-4 py-2">
                <span
                  :class="
                    item.status === 'Active'
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-200 text-gray-600'
                  "
                  class="rounded-full px-2 py-1 text-xs"
                >
                  {{ item.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Popup>

  <Popup :visible="showNewIssuePopup" @update:visible="showNewIssuePopup = $event">
    <div class="">
      <h2 class="mb-4 text-xl font-semibold">Submit an Issue</h2>

      <form @submit.prevent="submitIssue" class="space-y-4">
        <!-- Issue Category -->
        <div>
          <label class="mb-1 block font-medium">Issue Category</label>
          <select
            v-model="form.category"
            class="w-full rounded border px-3 py-2 focus:outline-none"
          >
            <option value="">Select Category</option>
            <option value="Production">Production</option>
            <option value="Quality">Quality</option>
            <option value="Maintenance">Maintenance</option>
          </select>
        </div>

        <!-- Affected Workflow -->
        <div>
          <label class="mb-1 block font-medium">Affected Workflow/Workorder/JobCard</label>
          <input
            type="text"
            v-model="form.workflow"
            placeholder="Search workflows/job cards..."
            class="w-full rounded border px-3 py-2 focus:outline-none"
          />
        </div>

        <!-- Urgency -->
        <div>
          <label class="mb-1 block font-medium">Urgency/Priority</label>
          <div class="flex gap-6">
            <label
              v-for="priority in ['Low', 'Medium', 'High', 'Critical']"
              :key="priority"
              class="flex items-center gap-1"
            >
              <input type="radio" v-model="form.priority" :value="priority" />
              {{ priority }}
            </label>
          </div>
        </div>

        <!-- Description -->
        <div>
          <label class="mb-1 block font-medium">Description</label>
          <div class="rounded border">
            <textarea
              v-model="form.description"
              rows="5"
              class="w-full resize-none px-3 py-2 focus:outline-none"
              placeholder="Enter issue description..."
            ></textarea>
          </div>
        </div>

        <!-- Attachments -->
        <div>
          <label class="mb-1 block font-medium">Attachments</label>
          <div class="rounded border border-dashed p-4 text-center">
            <input type="file" @change="handleFileUpload" class="hidden" ref="fileInput" />
            <button
              type="button"
              @click="fileInput?.click()"
              class="rounded bg-gray-100 px-4 py-2 hover:bg-gray-200"
            >
              Attach Files
            </button>
            <div v-if="form.attachment" class="mt-2 text-sm text-gray-600">
              {{ form.attachment.name }}
            </div>
          </div>
          <button
            class="mt-4 rounded bg-red-600 px-4 py-2 text-white hover:bg-red-700"
            @click="removeAttachment()"
          >
            Remove Attachment
          </button>
        </div>

        <!-- Actions -->
        <div class="mt-4 flex justify-end gap-2">
          <button type="submit" class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
            Submit Issue
          </button>
        </div>
      </form>
    </div>
  </Popup>
</template>

<script setup lang="ts">
import { ref, useTemplateRef } from 'vue'
import Popup from '@/components/popup.vue'

const showNewIssuePopup = ref(false)

const instructions = ref([
  {
    id: 'WO-1234',
    product: 'Product A',
    quantity: 100,
    dueDate: '2023-10-01',
    status: 'Active',
  },
  {
    id: 'WO-1235',
    product: 'Product B',
    quantity: 200,
    dueDate: '2023-10-02',
    status: 'Inactive',
  },
])

defineProps<{
  showReportedIssuesPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showReportedIssuesPopup'])

const form = ref<{
  category: string
  workflow: string
  priority: string
  description: string
  attachment: File | null
}>({
  category: '',
  workflow: '',
  priority: '',
  description: '',
  attachment: null,
})

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement | null
  if (target && target.files) {
    form.value.attachment = target.files[0]
  }
}
const submitIssue = () => {
  console.log('Issue submitted:', form.value)
  close()
}

const fileInput = useTemplateRef('fileInput')

const removeAttachment = () => {
  if (fileInput?.value) {
    fileInput.value.value = ''
    form.value.attachment = null
  }
}
</script>

<style>
button {
  cursor: pointer;
}
</style>