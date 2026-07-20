import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it } from 'vitest'
import { useCartStore } from '@/stores/cart'
import type { Product } from '@/types'

const mockProduct: Product = {
  id: 'prod-001',
  name: 'Python Mastery Course',
  price: 49.99,
  shortDescription: 'Go from beginner to advanced Python developer.',
  thumbnailUrl: 'https://example.com/thumb.jpg',
  category: 'online-course',
}

const anotherProduct: Product = {
  id: 'prod-002',
  name: 'Vue 3 Complete Guide',
  price: 39.99,
  shortDescription: 'Master Vue 3.',
  thumbnailUrl: 'https://example.com/thumb2.jpg',
  category: 'online-course',
}

describe('Cart store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with empty items and zero total', () => {
    const cart = useCartStore()
    expect(cart.items).toEqual([])
    expect(cart.total).toBe(0)
    expect(cart.itemCount).toBe(0)
  })

  it('addItem adds a new product with quantity 1', () => {
    const cart = useCartStore()
    cart.addItem(mockProduct)
    expect(cart.items).toHaveLength(1)
    expect(cart.items[0].quantity).toBe(1)
    expect(cart.items[0].product.id).toBe('prod-001')
  })

  it('addItem increments quantity for an existing product', () => {
    const cart = useCartStore()
    cart.addItem(mockProduct)
    cart.addItem(mockProduct)
    expect(cart.items).toHaveLength(1)
    expect(cart.items[0].quantity).toBe(2)
  })

  it('updateQuantity changes the item quantity', () => {
    const cart = useCartStore()
    cart.addItem(mockProduct)
    cart.updateQuantity('prod-001', 5)
    expect(cart.items[0].quantity).toBe(5)
  })

  it('updateQuantity to 0 removes the item', () => {
    const cart = useCartStore()
    cart.addItem(mockProduct)
    cart.updateQuantity('prod-001', 0)
    expect(cart.items).toHaveLength(0)
  })

  it('removeItem removes the product from the cart', () => {
    const cart = useCartStore()
    cart.addItem(mockProduct)
    cart.addItem(anotherProduct)
    cart.removeItem('prod-001')
    expect(cart.items).toHaveLength(1)
    expect(cart.items[0].product.id).toBe('prod-002')
  })

  it('total computes correctly across multiple items', () => {
    const cart = useCartStore()
    cart.addItem(mockProduct)
    cart.addItem(mockProduct)
    cart.addItem(anotherProduct)
    const expected = 49.99 * 2 + 39.99 * 1
    expect(cart.total).toBeCloseTo(expected, 2)
  })

  it('clearCart empties the store', () => {
    const cart = useCartStore()
    cart.addItem(mockProduct)
    cart.addItem(anotherProduct)
    cart.clearCart()
    expect(cart.items).toHaveLength(0)
    expect(cart.total).toBe(0)
  })
})
