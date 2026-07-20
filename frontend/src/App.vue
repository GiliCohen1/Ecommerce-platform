<script setup lang="ts">
import NavBar from '@/components/layout/NavBar.vue'
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <NavBar />
    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>
