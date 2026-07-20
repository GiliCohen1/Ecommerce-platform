<script setup lang="ts">
defineProps<{
  icon?: string
  title: string
  description?: string
}>()
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 text-center text-gray-500">
    <i :class="['pi', icon ?? 'pi-inbox', 'text-5xl mb-4 text-gray-300']" aria-hidden="true" />
    <h3 class="text-lg font-semibold text-gray-600 mb-1">{{ title }}</h3>
    <p v-if="description" class="text-sm">{{ description }}</p>
    <slot />
  </div>
</template>
