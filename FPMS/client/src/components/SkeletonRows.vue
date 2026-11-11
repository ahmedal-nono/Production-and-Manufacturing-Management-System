<template>
  <tr v-for="row in rows" :key="row" class="animate-pulse" aria-hidden="true">
    <td :colspan="cols" class="px-4 py-3">
      <div
        class="h-4 rounded bg-gray-300/80"
        :style="{ width: widths[(row - 1) % widths.length] }"
      ></div>
    </td>
  </tr>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    rows?: number
    cols?: number
  }>(),
  { rows: 4, cols: 5 },
)

const widths = ['55%', '80%', '68%', '90%', '62%']
</script>
