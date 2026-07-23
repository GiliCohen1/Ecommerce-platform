<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getProductById } from '@/api/products'
import { useCartStore } from '@/stores/cart'
import type { AsyncState, Product, ProductDetail } from '@/types'
import ReviewItem from '@/components/product/ReviewItem.vue'
import ErrorBanner from '@/components/common/ErrorBanner.vue'

const route = useRoute()
const router = useRouter()
const cart = useCartStore()

// Summary data passed from the product list via router state — renders instantly.
const preview = ref<Product | null>(
  (window.history.state?.product as Product) ?? null,
)

const state = ref<AsyncState<ProductDetail>>({ status: 'loading' })
const addedToCart = ref(false)

async function fetchProduct() {
  try {
    const product = await getProductById(route.params.id as string)
    state.value = { status: 'success', data: product }
  } catch (err) {
    state.value = {
      status: 'error',
      message: err instanceof Error ? err.message : 'Product not found.',
    }
  }
}

function handleAddToCart() {
  const product = state.value.status === 'success' ? state.value.data : preview.value
  if (!product) return
  cart.addItem(product)
  addedToCart.value = true
  setTimeout(() => { addedToCart.value = false }, 2000)
}

onMounted(fetchProduct)
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <button
      type="button"
      class="flex items-center gap-2 text-sm text-orange-600 hover:text-orange-800 mb-6 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-orange-400 rounded"
      @click="router.push({ name: 'product-list' })"
    >
      <i class="pi pi-arrow-left" aria-hidden="true" />
      Back to Products
    </button>

    <ErrorBanner v-if="state.status === 'error'" :message="state.message" />

    <!-- Preview: shown immediately from router state while full data loads -->
    <template v-else-if="preview && state.status === 'loading'">
      <div class="grid md:grid-cols-2 gap-8 mb-8">
        <img
          :src="preview.thumbnailUrl"
          :alt="preview.name"
          class="w-full rounded-xl object-cover aspect-video"
        />
        <div class="flex flex-col">
          <span class="inline-block text-xs font-medium bg-orange-50 text-orange-600 rounded-full px-2 py-0.5 mb-3 capitalize w-fit">
            {{ preview.category.replace('-', ' ') }}
          </span>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ preview.name }}</h1>
          <p class="text-gray-500 text-sm mb-4">{{ preview.shortDescription }}</p>
          <p class="text-3xl font-bold text-orange-600 mb-6">${{ preview.price.toFixed(2) }}</p>
          <button
            type="button"
            class="w-full sm:w-auto px-6 py-3 bg-orange-600 text-white rounded-xl font-semibold hover:bg-orange-700 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-orange-400 flex items-center justify-center gap-2"
            @click="handleAddToCart"
          >
            <i class="pi pi-shopping-cart" aria-hidden="true" />
            Add to Cart
          </button>
        </div>
      </div>
      <!-- Skeleton placeholders for description + reviews while still loading -->
      <div class="animate-pulse space-y-4">
        <div class="bg-white border border-gray-100 rounded-xl p-6">
          <div class="h-4 bg-gray-200 rounded w-1/4 mb-4" />
          <div class="space-y-2">
            <div class="h-3 bg-gray-200 rounded w-full" />
            <div class="h-3 bg-gray-200 rounded w-5/6" />
            <div class="h-3 bg-gray-200 rounded w-4/6" />
          </div>
        </div>
        <div class="bg-white border border-gray-100 rounded-xl p-6">
          <div class="h-4 bg-gray-200 rounded w-1/4" />
        </div>
      </div>
    </template>

    <!-- Skeleton: shown only when navigating directly (no preview available) -->
    <div v-else-if="state.status === 'loading'" class="animate-pulse space-y-4">
      <div class="h-64 bg-gray-200 rounded-xl" />
      <div class="h-6 bg-gray-200 rounded w-2/3" />
      <div class="h-4 bg-gray-200 rounded w-full" />
      <div class="h-4 bg-gray-200 rounded w-5/6" />
    </div>

    <!-- Full content -->
    <template v-else-if="state.status === 'success'">
      <div class="grid md:grid-cols-2 gap-8 mb-8">
        <img
          :src="state.data.thumbnailUrl"
          :alt="state.data.name"
          class="w-full rounded-xl object-cover aspect-video"
        />
        <div class="flex flex-col">
          <span class="inline-block text-xs font-medium bg-orange-50 text-orange-600 rounded-full px-2 py-0.5 mb-3 capitalize w-fit">
            {{ state.data.category.replace('-', ' ') }}
          </span>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ state.data.name }}</h1>
          <p class="text-gray-500 text-sm mb-4">{{ state.data.shortDescription }}</p>
          <p class="text-3xl font-bold text-orange-600 mb-6">${{ state.data.price.toFixed(2) }}</p>
          <button
            type="button"
            class="w-full sm:w-auto px-6 py-3 bg-orange-600 text-white rounded-xl font-semibold hover:bg-orange-700 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-orange-400 flex items-center justify-center gap-2"
            @click="handleAddToCart"
          >
            <i :class="['pi', addedToCart ? 'pi-check' : 'pi-shopping-cart']" aria-hidden="true" />
            {{ addedToCart ? 'Added!' : 'Add to Cart' }}
          </button>
        </div>
      </div>

      <div class="bg-white border border-gray-100 rounded-xl p-6 mb-6 shadow-sm">
        <h2 class="text-lg font-semibold text-gray-900 mb-3">Description</h2>
        <p class="text-gray-600 text-sm leading-relaxed">{{ state.data.longDescription }}</p>
      </div>

      <div class="bg-white border border-gray-100 rounded-xl p-6 shadow-sm">
        <h2 class="text-lg font-semibold text-gray-900 mb-1">
          Reviews ({{ state.data.reviews.length }})
        </h2>
        <div v-if="state.data.reviews.length > 0">
          <ReviewItem v-for="review in state.data.reviews" :key="review.id" :review="review" />
        </div>
        <p v-else class="text-sm text-gray-400 mt-3">No reviews yet.</p>
      </div>
    </template>
  </div>
</template>
