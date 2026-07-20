<script setup lang="ts">
import type { CartItem } from '@/types'
import { useCartStore } from '@/stores/cart'

const props = defineProps<{ item: CartItem }>()
const cart = useCartStore()

function changeQty(delta: number) {
  cart.updateQuantity(props.item.product.id, props.item.quantity + delta)
}

function remove() {
  cart.removeItem(props.item.product.id)
}
</script>

<template>
  <div class="flex items-center gap-4 py-4 border-b border-gray-100">
    <img
      :src="item.product.thumbnailUrl"
      :alt="item.product.name"
      class="w-16 h-16 rounded-lg object-cover flex-shrink-0"
    />

    <div class="flex-1 min-w-0">
      <h3 class="font-medium text-gray-900 text-sm truncate">{{ item.product.name }}</h3>
      <p class="text-xs text-gray-400 capitalize">{{ item.product.category.replace('-', ' ') }}</p>
      <p class="text-indigo-600 font-semibold text-sm mt-1">${{ item.product.price.toFixed(2) }}</p>
    </div>

    <div class="flex items-center gap-2">
      <button
        type="button"
        class="w-7 h-7 rounded-full border border-gray-200 flex items-center justify-center hover:bg-gray-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400 disabled:opacity-40"
        :disabled="item.quantity <= 1"
        @click="changeQty(-1)"
        :aria-label="`Decrease quantity of ${item.product.name}`"
      >
        <i class="pi pi-minus text-xs" aria-hidden="true" />
      </button>

      <span class="w-6 text-center text-sm font-medium" aria-live="polite">{{ item.quantity }}</span>

      <button
        type="button"
        class="w-7 h-7 rounded-full border border-gray-200 flex items-center justify-center hover:bg-gray-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400"
        @click="changeQty(1)"
        :aria-label="`Increase quantity of ${item.product.name}`"
      >
        <i class="pi pi-plus text-xs" aria-hidden="true" />
      </button>
    </div>

    <p class="text-sm font-semibold text-gray-800 w-16 text-right">
      ${{ (item.product.price * item.quantity).toFixed(2) }}
    </p>

    <button
      type="button"
      class="text-gray-300 hover:text-red-500 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-red-400 rounded"
      @click="remove"
      :aria-label="`Remove ${item.product.name} from cart`"
    >
      <i class="pi pi-trash" aria-hidden="true" />
    </button>
  </div>
</template>
