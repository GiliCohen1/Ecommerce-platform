<script setup lang="ts">
import { onMounted, ref } from "vue";
import { getProducts } from "@/api/products";
import type { AsyncState, Product, ProductFilters } from "@/types";
import ProductCard from "@/components/product/ProductCard.vue";
import ProductCardSkeleton from "@/components/product/ProductCardSkeleton.vue";
import ProductFiltersBar from "@/components/product/ProductFilters.vue";
import ErrorBanner from "@/components/common/ErrorBanner.vue";
import EmptyState from "@/components/common/EmptyState.vue";

const state = ref<AsyncState<Product[]>>({ status: "idle" });
const filters = ref<ProductFilters>({ sort_by: "name", order: "asc" });
const isRefetching = ref(false);

async function fetchProducts(f: ProductFilters = {}, isInitial = false) {
  if (isInitial) {
    state.value = { status: "loading" };
  } else {
    isRefetching.value = true;
  }
  try {
    const result = await getProducts(f);
    state.value = { status: "success", data: result.data };
  } catch (err) {
    state.value = {
      status: "error",
      message: err instanceof Error ? err.message : "Failed to load products.",
    };
  } finally {
    isRefetching.value = false;
  }
}

function onFiltersUpdate(newFilters: ProductFilters) {
  filters.value = newFilters;
  fetchProducts(newFilters);
}

onMounted(() => fetchProducts(filters.value, true));
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Our Products</h1>

    <div class="mb-6">
      <ProductFiltersBar @update:filters="onFiltersUpdate" />
    </div>

    <ErrorBanner
      v-if="state.status === 'error'"
      :message="state.message"
      class="mb-6"
    />

    <!-- Initial skeleton (first load only) -->
    <div
      v-if="state.status === 'loading'"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <ProductCardSkeleton v-for="n in 6" :key="n" />
    </div>

    <template v-else-if="state.status === 'success'">
      <div class="flex items-center gap-3 mb-4">
        <p class="text-sm text-gray-400">
          {{ state.data.length }} product{{
            state.data.length !== 1 ? "s" : ""
          }}
          found
        </p>
        <!-- Subtle spinner on filter re-fetches -->
        <i
          v-if="isRefetching"
          class="pi pi-spin pi-spinner text-indigo-400 text-sm"
          aria-label="Updating results"
        />
      </div>

      <div
        v-if="state.data.length > 0"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 transition-opacity duration-150"
        :class="{ 'opacity-50': isRefetching }"
      >
        <ProductCard
          v-for="product in state.data"
          :key="product.id"
          :product="product"
        />
      </div>

      <EmptyState
        v-else
        icon="pi-search"
        title="No products found"
        description="Try adjusting your filters or search term."
      />
    </template>
  </div>
</template>
