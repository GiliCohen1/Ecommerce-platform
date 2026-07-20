<script setup lang="ts">
defineProps<{ message: string }>()
</script>

<template>
  <div
    role="alert"
    class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 flex items-start gap-3"
  >
    <i class="pi pi-exclamation-triangle mt-0.5 flex-shrink-0" aria-hidden="true" />
    <p>{{ message }}</p>
  </div>
</template>
