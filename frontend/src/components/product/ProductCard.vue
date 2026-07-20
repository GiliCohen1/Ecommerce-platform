<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Product } from '@/types'

const props = defineProps<{ product: Product }>()
const router = useRouter()

function navigate() {
  router.push({ name: 'product-detail', params: { id: props.product.id } })
}
</script>

<template>
  <button
    type="button"
    class="bg-white rounded-xl border border-gray-100 overflow-hidden shadow-sm hover:shadow-md transition-shadow text-left w-full focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500"
    @click="navigate"
    :aria-label="`View details for ${product.name}`"
  >
    <img
      :src="product.thumbnailUrl"
      :alt="product.name"
      class="w-full h-48 object-cover"
      loading="lazy"
    />
    <div class="p-4">
      <span
        class="inline-block text-xs font-medium bg-indigo-50 text-indigo-600 rounded-full px-2 py-0.5 mb-2 capitalize"
      >
        {{ product.category.replace('-', ' ') }}
      </span>
      <h2 class="font-semibold text-gray-900 text-sm mb-1 line-clamp-2">{{ product.name }}</h2>
      <p class="text-xs text-gray-500 line-clamp-2 mb-3">{{ product.shortDescription }}</p>
      <p class="font-bold text-indigo-600">${{ product.price.toFixed(2) }}</p>
    </div>
  </button>
</template>
