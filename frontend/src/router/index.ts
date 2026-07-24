import { createRouter, createWebHistory } from 'vue-router'
import ProductDetailView from '@/views/ProductDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'product-list',
      component: () => import('@/views/ProductListView.vue'),
    },
    {
      path: '/products/:id',
      name: 'product-detail',
      component: ProductDetailView,
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('@/views/CartView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
    },
  ],
})

export default router
