<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>

<template>
  <span class="eyebrow">{{ text }}</span>
</template>
