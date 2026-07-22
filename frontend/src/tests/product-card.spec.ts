import { mount, flushPromises } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import { describe, expect, it } from 'vitest'
import ProductCard from '@/components/product/ProductCard.vue'
import type { Product } from '@/types'

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', component: { template: '<div />' } },
    { path: '/products/:id', name: 'product-detail', component: { template: '<div />' } },
  ],
})

const product: Product = {
  id: 'prod-007',
  name: 'TypeScript Deep Dive',
  price: 34.99,
  shortDescription: 'Advanced TypeScript patterns.',
  thumbnailUrl: 'https://example.com/ts.jpg',
  category: 'online-course',
}

function mountCard() {
  return mount(ProductCard, {
    props: { product },
    global: { plugins: [router] },
  })
}

describe('ProductCard', () => {
  it('renders the product name', () => {
    const wrapper = mountCard()
    expect(wrapper.text()).toContain('TypeScript Deep Dive')
  })

  it('renders the price formatted to 2 decimal places', () => {
    const wrapper = mountCard()
    expect(wrapper.text()).toContain('$34.99')
  })

  it('renders the short description', () => {
    const wrapper = mountCard()
    expect(wrapper.text()).toContain('Advanced TypeScript patterns.')
  })

  it('renders the thumbnail with the correct src and alt', () => {
    const wrapper = mountCard()
    const img = wrapper.find('img')
    expect(img.attributes('src')).toBe('https://example.com/ts.jpg')
    expect(img.attributes('alt')).toBe('TypeScript Deep Dive')
  })

  it('renders the category badge with human-readable text', () => {
    const wrapper = mountCard()
    expect(wrapper.text()).toContain('online course')
  })

  it('has an accessible aria-label describing the product', () => {
    const wrapper = mountCard()
    expect(wrapper.attributes('aria-label')).toContain('TypeScript Deep Dive')
  })

  it('navigates to product-detail route on click', async () => {
    await router.push('/')
    const wrapper = mountCard()
    await wrapper.trigger('click')
    await flushPromises()
    expect(router.currentRoute.value.name).toBe('product-detail')
    expect(router.currentRoute.value.params.id).toBe('prod-007')
  })
})
