<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <div class="max-w-lg mx-auto px-4 py-24 text-center">
    <p class="text-8xl font-bold text-indigo-100 mb-4">404</p>
    <h1 class="text-2xl font-bold text-gray-800 mb-2">Page Not Found</h1>
    <p class="text-gray-500 mb-8">The page you are looking for does not exist.</p>
    <button
      type="button"
      class="px-6 py-3 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400"
      @click="router.push({ name: 'product-list' })"
    >
      Go to Products
    </button>
  </div>
</template>
