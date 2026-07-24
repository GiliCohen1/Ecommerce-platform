import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'
import type { CartItem, Product } from '@/types'

const STORAGE_KEY = 'ecom:cart'

export const useCartStore = defineStore('cart', () => {
  const stored = localStorage.getItem(STORAGE_KEY)
  const items = ref<CartItem[]>(stored ? JSON.parse(stored) : [])

  watch(items, (val) => localStorage.setItem(STORAGE_KEY, JSON.stringify(val)), { deep: true })

  const itemCount = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0),
  )

  const total = computed(() =>
    items.value.reduce((sum, item) => sum + item.product.price * item.quantity, 0),
  )

  function addItem(product: Product): void {
    const existing = items.value.find((i) => i.product.id === product.id)
    if (existing) {
      existing.quantity++
    } else {
      items.value.push({ product, quantity: 1 })
    }
  }

  function updateQuantity(productId: string, quantity: number): void {
    if (quantity <= 0) {
      removeItem(productId)
      return
    }
    const item = items.value.find((i) => i.product.id === productId)
    if (item) item.quantity = quantity
  }

  function removeItem(productId: string): void {
    items.value = items.value.filter((i) => i.product.id !== productId)
  }

  function clearCart(): void {
    items.value = []
  }

  return { items, itemCount, total, addItem, updateQuantity, removeItem, clearCart }
})
