<script setup lang="ts">
import type { ProductReview } from '@/types'

defineProps<{ review: ProductReview }>()
</script>

<template>
  <div class="border-t border-gray-100 py-4">
    <div class="flex items-center justify-between mb-1">
      <span class="font-medium text-gray-800 text-sm">{{ review.author }}</span>
      <span class="text-xs text-gray-400">{{ review.date }}</span>
    </div>
    <div class="flex gap-0.5 mb-2" :aria-label="`Rating: ${review.rating} out of 5`">
      <i
        v-for="star in 5"
        :key="star"
        :class="['pi', star <= review.rating ? 'pi-star-fill text-yellow-400' : 'pi-star text-gray-300', 'text-xs']"
        aria-hidden="true"
      />
    </div>
    <p class="text-sm text-gray-600">{{ review.comment }}</p>
  </div>
</template>
