<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useNav } from '@slidev/client'

const props = defineProps<{
  tag: string
  title: string
  featured?: boolean
  clickAt?: number
}>()

const { clicks } = useNav()
const activated = ref(false)

watch(() => clicks.value, (val) => {
  if (props.clickAt === undefined) return
  if (val >= props.clickAt) {
    activated.value = true
  } else if (activated.value && val > 0) {
    // スライド内で戻った場合（clicks が段階的に減少）のみリセット
    // val === 0 はスライド遷移時の一括リセットなので無視
    activated.value = false
  }
}, { immediate: true })

const isFeatured = computed(() => props.featured || activated.value)
</script>

<template>
  <div class="pillar" :class="{ featured: isFeatured }">
    <span class="tag">{{ tag }}</span>
    <h3 v-html="title" />
    <div class="body"><slot /></div>
  </div>
</template>

<style scoped>
.pillar {
  background: white;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 1.3rem 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  height: 100%;
  box-sizing: border-box;
}

.pillar.featured {
  background: var(--brand);
  border-color: var(--brand);
}

.tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: var(--brand);
  font-weight: 600;
  letter-spacing: 0.14em;
}

.pillar.featured .tag {
  color: rgba(255, 255, 255, 0.8);
}

h3 {
  font-size: 1.3rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.25;
  color: var(--ink);
}

.pillar.featured h3 {
  color: white;
}

.body {
  font-size: 0.9rem;
  color: var(--ink-soft);
  line-height: 1.6;
  margin: 0;
}

.pillar.featured .body {
  color: rgba(255, 255, 255, 0.92);
}

.pillar :deep(li) {
  color: var(--ink-soft);
}

.pillar :deep(li::marker) {
  color: var(--ink-soft);
}

.pillar.featured :deep(li) {
  color: rgba(255, 255, 255, 0.92);
}

.pillar.featured :deep(li::marker) {
  color: rgba(255, 255, 255, 0.92);
}
</style>
