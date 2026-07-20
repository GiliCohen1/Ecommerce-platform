import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import type { CartItem, Product } from '@/types'

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])

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
