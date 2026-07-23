<script setup lang="ts">
import { computed } from 'vue'
import { useCartStore } from '@/stores/cart'

const cart = useCartStore()

const itemCount = computed(() => cart.itemCount)
</script>

<template>
  <nav class="bg-white border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
      <router-link
        to="/"
        class="text-lg font-bold text-orange-600 hover:text-orange-800 transition-colors"
      >
        DigitalShop
      </router-link>

      <div class="flex items-center gap-4">
        <router-link
          to="/"
          class="text-sm text-gray-600 hover:text-orange-600 transition-colors"
        >
          Products
        </router-link>

        <router-link
          to="/cart"
          class="relative flex items-center gap-1 text-sm text-gray-600 hover:text-orange-600 transition-colors"
          aria-label="`Shopping cart, ${itemCount} items`"
        >
          <i class="pi pi-shopping-cart text-lg" aria-hidden="true" />
          <span
            v-if="itemCount > 0"
            class="absolute -top-2 -right-2 bg-orange-600 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center"
            aria-live="polite"
          >
            {{ itemCount }}
          </span>
          <span class="hidden sm:inline">Cart</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>
