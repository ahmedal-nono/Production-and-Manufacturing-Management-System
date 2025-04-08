<template>
  <div v-if="visible" class="popup-overlay" @click="handleOverlayClick">
    <div class="popup-content" @click.stop>
      <button
        @click="$emit('update:visible', false)"
        class="close-button rounded-full! bg-white! px-4! py-2! shadow!"
      >
        ✕
      </button>
      <h3 class="mb-4 flex justify-center text-xl font-bold">{{ title }}</h3>
      <div class="space-y-4">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// defineProps({
//   visible: {
//     type: Boolean,
//     required: true,
//   },
//   title: {
//     type: String,
//     default: '',
//   },
// })
const { visible, title = '' } = defineProps<{
  visible: boolean
  title: string
}>()

const emit = defineEmits()

function handleOverlayClick() {
  console.log(visible)

  emit('update:visible', false)
}
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 100%;
  max-width: 1000vh;
  max-height: 120vh;
  overflow-y: auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
  position: relative;
  scale: 70%;
}

.close-button {
  position: sticky;
  top: 10px;
  left: 100%;
  background: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #333;
}
</style>
