<template>
  <Popup
    :visible="showWorkinstructionPopup"
    @update:visible="(value: boolean) => emitEvent('update:showWorkinstructionPopup', value)"
  >
    <div class="">
      <!-- Header -->
      <div class="mb-4 flex items-center justify-between">
        <h2 class="text-2xl font-bold">Work Instructions Library</h2>
        <button
          @click="showCreateWorkinstructionPopup = true"
          class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          + Create New Work Instruction
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
          <option>All Products</option>
        </select>
        <select class="rounded border px-4 py-2">
          <option>All Workstations</option>
        </select>
        <select class="rounded border px-4 py-2">
          <option>All Statuses</option>
        </select>
        <input type="date" class="rounded border px-4 py-2" />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-center">
          <thead class="bg-blue-500 text-white">
            <tr>
              <th class="border border-gray-700 px-4 py-2">Title</th>
              <th class="border border-gray-700 px-4 py-2">Product</th>
              <th class="border border-gray-700 px-4 py-2">Last Updated</th>
              <th class="border border-gray-700 px-4 py-2">Status</th>
              <th class="border border-gray-700 px-4 py-2">Attachments</th>
              <th class="border border-gray-700 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, index) in instructions"
              :key="index"
              class="border bg-white hover:bg-gray-50"
            >
              <td class="border border-gray-700 px-4 py-2">{{ item.title }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ item.product }}</td>
              <td class="border border-gray-700 px-4 py-2">{{ item.updated }}</td>
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
              <td class="space-x-2 border border-gray-700 px-4 py-2">
                <button class="text-gray-700 hover:text-black">📄</button>
                <button class="text-gray-700 hover:text-black">🖼️</button>
              </td>
              <td class="space-x-2 border border-gray-700 px-4 py-2">
                <button
                  @click="showViewWorkinstructionPopup = true"
                  class="m-1 rounded bg-gray-200 px-2 py-1 text-sm hover:bg-gray-300"
                >
                  View
                </button>
                <button class="m-1 rounded bg-gray-200 px-2 py-1 text-sm hover:bg-gray-300">
                  Link
                </button>
                <button class="m-1 rounded bg-gray-200 px-2 py-1 text-sm hover:bg-gray-300">
                  Download
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Popup>

  <Popup
    :visible="showCreateWorkinstructionPopup"
    @update:visible="showCreateWorkinstructionPopup = $event"
  >
    <div class="">
      <h1 class="mb-6 text-2xl font-bold">Create New Work Instruction</h1>

      <!-- Basic Information -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Work instruction Information</h2>
        <div class="mb-4">
          <label class="mb-1 block font-medium">Task Name</label>
          <input
            v-model="form.taskName"
            type="text"
            placeholder="E.g., Brake System Assembly"
            class="w-full rounded border px-3 py-2"
          />
        </div>
        <div>
          <label class="mb-1 block font-medium">Status</label>
          <select v-model="form.status" class="w-full rounded border px-3 py-2">
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
        </div>
      </section>

      <!-- Step-by-Step Instructions -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Step-by-Step Instructions</h2>
        <div
          v-for="(step, index) in form.steps"
          :key="index"
          class="relative mb-6 rounded border p-3"
        >
          <label class="mb-1 block font-medium">Step Description</label>
          <textarea
            v-model="step.description"
            rows="3"
            class="w-full rounded border px-3 py-2"
          ></textarea>
          <div class="mt-2 flex items-center gap-2">
            <label class="inline-block text-sm">
              <input type="file" class="hidden" @change="attachMedia($event, index)" />
              <button class="rounded border bg-gray-100 px-3 py-1 text-sm hover:bg-gray-200">
                📎 Attach Media
              </button>
            </label>
            <span v-if="step.media" class="text-sm text-green-600"
              >Attached: {{ step.media.name }}</span
            >
          </div>
          <button
            @click="removeStep(index)"
            class="absolute top-2 right-4 text-lg text-red-500 hover:text-red-700"
          >
            Delete
          </button>
        </div>
        <button
          @click="addStep"
          class="rounded border bg-gray-100 px-4 py-2 text-sm hover:bg-gray-200"
        >
          + Add Step
        </button>
      </section>

      <!-- Tools & Materials -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Tools & Materials</h2>
        <div class="mb-4">
          <label class="mb-1 block font-medium">Tools Required</label>
          <textarea
            v-model="form.tools"
            rows="3"
            class="w-full rounded border px-3 py-2"
          ></textarea>
        </div>
        <div>
          <label class="mb-1 block font-medium">Materials</label>
          <input v-model="form.materials" type="text" class="w-full rounded border px-3 py-2" />
        </div>
      </section>

      <!-- Buttons -->
      <div class="flex justify-end gap-4">
        <button class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
          Save & Publish
        </button>
      </div>
    </div>
  </Popup>

  <Popup
    :visible="showViewWorkinstructionPopup"
    @update:visible="showViewWorkinstructionPopup = $event"
  >
    <div class="">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <h1 class="text-2xl font-bold">Car Door Welding Process</h1>
        <div class="space-x-2">
          <button class="rounded bg-blue-500 px-3 py-1 text-white hover:bg-blue-600">PDF</button>
          <button
            @click="showEditWorkinstructionPopup = true"
            class="rounded bg-blue-100 px-3 py-1 text-blue-700 hover:bg-blue-200"
          >
            Edit
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <!-- Left: Instructions -->
        <div class="space-y-6 lg:col-span-2">
          <!-- Steps -->
          <div v-for="(step, index) in steps" :key="index" class="rounded bg-white p-4 shadow">
            <div class="flex items-start gap-4">
              <div class="text-xl font-bold text-gray-600">{{ index + 1 }}</div>
              <div>
                <h3 class="mb-1 text-lg font-semibold">{{ step.title }}</h3>
                <p class="mb-2 text-gray-700">{{ step.description }}</p>
                <div v-if="step.media" class="overflow-hidden rounded border">
                  <img :src="step.media" alt="Step media" class="w-full object-cover" />
                </div>
              </div>
            </div>
          </div>

          <!-- Safety Precautions -->
          <div class="rounded bg-white p-4 shadow">
            <h2 class="mb-2 text-lg font-semibold">Safety Precautions</h2>
            <ul class="list-disc space-y-1 pl-6 text-gray-700">
              <li>Wear proper PPE (helmet, gloves, apron)</li>
              <li>Verify machine grounding before operation</li>
              <li>Keep work area ventilated</li>
            </ul>
          </div>
        </div>

        <!-- Right: Details -->
        <div class="space-y-4 rounded bg-white p-4 shadow">
          <div>
            <h2 class="text-md font-semibold text-gray-800">Details</h2>
            <p><strong>Product:</strong> SUV Model X</p>
            <p><strong>Last Updated:</strong> 2023-08-15 14:30</p>
            <p><strong>Status:</strong> Active</p>
          </div>

          <div>
            <h2 class="text-md font-semibold text-gray-800">Attachments</h2>
            <ul class="space-y-2">
              <li
                v-for="file in attachments"
                :key="file.name"
                class="flex items-center justify-between rounded bg-gray-100 px-3 py-2"
              >
                <span>{{ file.name }}</span>
                <button class="text-blue-600 hover:underline">⬇</button>
              </li>
            </ul>
          </div>

          <div>
            <h2 class="text-md font-semibold text-gray-800">Revision History</h2>
            <ul class="list-disc space-y-1 pl-6 text-sm text-gray-700">
              <li>2023-08-15: Updated safety guidelines</li>
              <li>2023-07-01: Initial version approved</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </Popup>

  <Popup
    :visible="showEditWorkinstructionPopup"
    @update:visible="showEditWorkinstructionPopup = $event"
  >
    <div class="">
      <h1 class="mb-6 text-2xl font-bold">Edit Work Instruction</h1>

      <!-- Basic Information -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Work instruction Information</h2>
        <div class="mb-4">
          <label class="mb-1 block font-medium">Task Name</label>
          <input
            v-model="form.taskName"
            type="text"
            placeholder="E.g., Brake System Assembly"
            class="w-full rounded border px-3 py-2"
          />
        </div>
        <div>
          <label class="mb-1 block font-medium">Status</label>
          <select v-model="form.status" class="w-full rounded border px-3 py-2">
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
        </div>
      </section>

      <!-- Step-by-Step Instructions -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Step-by-Step Instructions</h2>
        <div
          v-for="(step, index) in form.steps"
          :key="index"
          class="relative mb-6 rounded border p-3"
        >
          <label class="mb-1 block font-medium">Step Description</label>
          <textarea
            v-model="step.description"
            rows="3"
            class="w-full rounded border px-3 py-2"
          ></textarea>
          <div class="mt-2 flex items-center gap-2">
            <label class="inline-block text-sm">
              <input type="file" class="hidden" @change="attachMedia($event, index)" />
              <button class="rounded border bg-gray-100 px-3 py-1 text-sm hover:bg-gray-200">
                📎 Attach Media
              </button>
            </label>
            <span v-if="step.media" class="text-sm text-green-600"
              >Attached: {{ step.media.name }}</span
            >
          </div>
          <button
            @click="removeStep(index)"
            class="absolute top-2 right-4 text-lg text-red-500 hover:text-red-700"
          >
            Delete
          </button>
        </div>
        <button
          @click="addStep"
          class="rounded border bg-gray-100 px-4 py-2 text-sm hover:bg-gray-200"
        >
          + Add Step
        </button>
      </section>

      <!-- Tools & Materials -->
      <section class="mb-6 rounded border p-4">
        <h2 class="mb-4 font-semibold">Tools & Materials</h2>
        <div class="mb-4">
          <label class="mb-1 block font-medium">Tools Required</label>
          <textarea
            v-model="form.tools"
            rows="3"
            class="w-full rounded border px-3 py-2"
          ></textarea>
        </div>
        <div>
          <label class="mb-1 block font-medium">Materials</label>
          <input v-model="form.materials" type="text" class="w-full rounded border px-3 py-2" />
        </div>
      </section>

      <!-- Buttons -->
      <div class="flex justify-end gap-4">
        <button class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
          Save & Publish
        </button>
      </div>
    </div>
  </Popup>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import Popup from '@/components/popup.vue'

interface Instruction {
  title: string
  product: string
  updated: string
  status: string
  attachments: string[]
}

interface Step {
  description: string
  media: File | null
}

interface Form {
  taskName: string
  status: string
  steps: Step[]
  tools: string
  materials: string
}

const showCreateWorkinstructionPopup = ref<boolean>(false)
const showViewWorkinstructionPopup = ref<boolean>(false)
const showEditWorkinstructionPopup = ref<boolean>(false)

defineProps<{
  showWorkinstructionPopup: boolean
}>()

const emitEvent = defineEmits<{
  (e: 'close'): void
  (e: 'submit'): void
  (e: 'update:showWorkinstructionPopup', value: boolean): void
}>()

const instructions = ref<Instruction[]>([
  {
    title: 'Car Door Welding Process',
    product: 'SUV Model X',
    updated: '2023-08-15 14:30',
    status: 'Active',
    attachments: ['pdf', 'image'],
  },
  {
    title: 'Battery Installation',
    product: 'SUV Model X',
    updated: '2023-07-12 10:00',
    status: 'Inactive',
    attachments: ['pdf'],
  },
  {
    title: 'Quality Final Check',
    product: 'SUV Model Y',
    updated: '2023-09-01 08:45',
    status: 'Active',
    attachments: ['pdf', 'image'],
  },
])

const form = reactive<Form>({
  taskName: '',
  status: 'Active',
  steps: [
    {
      description: '',
      media: null,
    },
  ],
  tools: '',
  materials: '',
})

const addStep = (): void => {
  form.steps.push({ description: '', media: null })
}

const removeStep = (index: number): void => {
  form.steps.splice(index, 1)
}

const attachMedia = (event: Event, index: number): void => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    form.steps[index].media = file
  }
}

const steps = [
  {
    title: 'Prepare Welding Equipment',
    description: 'Check and calibrate welding machine according to specifications',
    media: 'https://via.placeholder.com/400x150?text=Welding+machine+setup',
  },
  {
    title: 'Component Alignment',
    description: 'Position door components using alignment jig Model X-123',
    media: 'https://via.placeholder.com/400x150?text=Component+alignment+jig',
  },
  {
    title: 'Spot Welding Process',
    description: 'Perform 12 spot welds at marked locations',
    media: 'https://via.placeholder.com/400x150?text=Welding+points+diagram',
  },
]

const attachments = [{ name: 'Welding_Specs.pdf' }, { name: 'Welding_Demo.mp4' }]
</script>

<style>
button {
  cursor: pointer;
}
</style>
