<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

// label を渡さなければ、ページの frontmatter の chapter を表示する
const props = defineProps<{ label?: string }>()
const { $frontmatter } = useSlideContext()
const text = computed(() => props.label ?? $frontmatter.chapter)
</script>

<template>
  <div v-if="text" class="chapter-label">{{ text }}</div>
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
