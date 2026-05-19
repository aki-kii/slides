<script setup>
import { provide } from 'vue'

defineProps({
  bottom: { type: String, default: '1.2rem' },
})

provide('insideBottomLinks', true)
</script>

<template>
  <div class="bottom-links-wrapper" :style="{ bottom }">
    <slot />
  </div>
</template>

<style scoped>
.bottom-links-wrapper {
  position: absolute;
  left: 3.5rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
  z-index: 100;
}
</style>
