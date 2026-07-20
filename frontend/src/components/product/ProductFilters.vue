<script setup lang="ts">
import { ref, watch } from 'vue'
import type { ProductFilters } from '@/types'

const emit = defineEmits<{ 'update:filters': [filters: ProductFilters] }>()

const name = ref('')
const category = ref('')
const sortBy = ref<'name' | 'price'>('name')
const order = ref<'asc' | 'desc'>('asc')

let debounceTimer: ReturnType<typeof setTimeout>

function emitFilters() {
  emit('update:filters', {
    name: name.value || undefined,
    category: category.value || undefined,
    sort_by: sortBy.value,
    order: order.value,
  })
}

watch(name, () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(emitFilters, 300)
})

watch([category, sortBy, order], emitFilters)
</script>

<template>
  <div class="bg-white border border-gray-100 rounded-xl p-4 flex flex-wrap gap-3 items-end shadow-sm">
    <div class="flex-1 min-w-[180px]">
      <label for="filter-name" class="block text-xs font-medium text-gray-600 mb-1">Search</label>
      <input
        id="filter-name"
        v-model="name"
        type="search"
        placeholder="Search products..."
        class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
    </div>

    <div class="min-w-[160px]">
      <label for="filter-category" class="block text-xs font-medium text-gray-600 mb-1">Category</label>
      <select
        id="filter-category"
        v-model="category"
        class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      >
        <option value="">All categories</option>
        <option value="online-course">Online Course</option>
        <option value="ebook">eBook</option>
        <option value="software-license">Software License</option>
      </select>
    </div>

    <div class="min-w-[140px]">
      <label for="filter-sort" class="block text-xs font-medium text-gray-600 mb-1">Sort by</label>
      <select
        id="filter-sort"
        v-model="sortBy"
        class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      >
        <option value="name">Name</option>
        <option value="price">Price</option>
      </select>
    </div>

    <div class="min-w-[120px]">
      <label for="filter-order" class="block text-xs font-medium text-gray-600 mb-1">Order</label>
      <select
        id="filter-order"
        v-model="order"
        class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      >
        <option value="asc">Ascending</option>
        <option value="desc">Descending</option>
      </select>
    </div>
  </div>
</template>
