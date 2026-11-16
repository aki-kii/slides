<script setup>
import { useSlideContext } from '@slidev/client'

const { $frontmatter } = useSlideContext()
</script>

<template>
  <div v-if="$frontmatter.chapter" class="chapter-label">{{ $frontmatter.chapter }}</div>
</template>

<style scoped>
.chapter-label {
  position: absolute;
  top: 1.5rem;
  left: 3.5rem;
  font-size: 0.75rem;
  color: rgba(0, 0, 0, 0.25);
  font-weight: 400;
  letter-spacing: 0.05em;
  z-index: 50;
  pointer-events: none;
  user-select: none;
}
</style>
