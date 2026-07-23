<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import CartLineItem from '@/components/cart/CartLineItem.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const cart = useCartStore()
const router = useRouter()
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Shopping Cart</h1>

    <EmptyState
      v-if="cart.items.length === 0"
      icon="pi-shopping-cart"
      title="Your cart is empty"
      description="Browse our products and add items to your cart."
    >
      <button
        type="button"
        class="mt-4 px-5 py-2 bg-orange-600 text-white rounded-xl text-sm font-medium hover:bg-orange-700 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-orange-400"
        @click="router.push({ name: 'product-list' })"
      >
        Browse Products
      </button>
    </EmptyState>

    <template v-else>
      <div class="bg-white border border-gray-100 rounded-xl shadow-sm px-6 mb-6">
        <CartLineItem
          v-for="item in cart.items"
          :key="item.product.id"
          :item="item"
        />
      </div>

      <div class="bg-white border border-gray-100 rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-gray-600">
            {{ cart.itemCount }} item{{ cart.itemCount !== 1 ? 's' : '' }}
          </span>
          <span class="text-2xl font-bold text-orange-600">
            ${{ cart.total.toFixed(2) }}
          </span>
        </div>

        <button
          type="button"
          class="w-full py-3 bg-orange-600 text-white rounded-xl font-semibold hover:bg-orange-700 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-orange-400 mb-3"
        >
          Proceed to Checkout
        </button>

        <button
          type="button"
          class="w-full py-2 text-sm text-gray-400 hover:text-red-500 transition-colors focus:outline-none"
          @click="cart.clearCart"
        >
          Clear cart
        </button>
      </div>
    </template>
  </div>
</template>
