<template>
  <div :style="containerStyle">
    <template v-for="item in visibleItems" :key="String(item)">
      <slot name="item" :item="item" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import { useNav } from '@slidev/client'
import { useSequentialReveal } from '../composables/useSequentialReveal'

const props = withDefaults(defineProps<{
  items: unknown[]
  duration?: number
  direction?: 'wrap' | 'row' | 'column'
  at?: number
  step?: boolean
}>(), { duration: 5, direction: 'wrap', at: 1, step: false })

const { clicks } = useNav()

// timed mode
const { visible: timedVisible, start, reset } = useSequentialReveal(props.items as string[], props.duration)

watch(clicks, (val) => {
  if (props.step) return
  if (val >= props.at) start()
  else reset()
}, { immediate: true })

const visibleItems = computed(() => {
  if (props.step) {
    const count = Math.max(0, clicks.value - props.at + 1)
    return props.items.slice(0, count)
  }
  return timedVisible.value
})

const containerStyle = computed(() => {
  const base = 'display:flex; gap:0.35rem; align-content:flex-start;'
  if (props.direction === 'column') return base + ' flex-direction:column;'
  if (props.direction === 'row')    return base + ' flex-direction:row;'
  return base + ' flex-wrap:wrap;'
})
</script>
