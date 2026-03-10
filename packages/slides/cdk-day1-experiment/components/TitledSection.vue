<template>
  <div class="flex items-baseline gap-4 mb-4">
    <h2 class="!m-0">{{ title }}</h2>
    <span>{{ description }}</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description: string
}>()
</script>
