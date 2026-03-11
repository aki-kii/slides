<script setup>
import { provide } from 'vue'

provide('insideBottomLinks', true)
</script>

<template>
  <div class="bottom-links-wrapper">
    <slot />
  </div>
</template>

<style scoped>
.bottom-links-wrapper {
  position: absolute;
  bottom: 0.85rem;
  left: 3.5rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
  z-index: 100;
}
</style>
