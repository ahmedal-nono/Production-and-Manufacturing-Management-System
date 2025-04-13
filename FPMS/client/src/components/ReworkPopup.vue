<template>
  <Popup
    :visible="showReworkPopup"
    @update:visible="(value: boolean) => emitEvent('update:showReworkPopup', value)"
  >
  </Popup>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Popup from '@/components/popup.vue'

defineProps<{
  showReworkPopup: boolean
}>()

const emitEvent = defineEmits(['close', 'submit', 'update:showReworkPopup'])
</script>
