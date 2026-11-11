<template>
  <div class="animate-pulse space-y-2" aria-hidden="true">
    <div
      v-for="row in rows"
      :key="row"
      class="rounded-lg bg-gray-300/70"
      :class="compact ? 'h-8' : 'h-16'"
    ></div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    rows?: number
    compact?: boolean
  }>(),
  { rows: 4, compact: false },
)
</script>
