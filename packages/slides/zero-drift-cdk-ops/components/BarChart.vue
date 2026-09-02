<script setup lang="ts">
import { computed } from 'vue'

interface Bar {
  label: string
  value: number
  color?: string
  valueLabel?: string
  icon?: string
}

const props = withDefaults(
  defineProps<{
    bars: Bar[]
    max?: number
    unit?: string
    height?: number
    barWidth?: number
    decimals?: number
  }>(),
  {
    unit: '',
    height: 280,
    barWidth: 96,
    decimals: 0,
  },
)

const maxValue = computed(
  () => props.max ?? Math.max(...props.bars.map((b) => b.value)),
)

function barHeight(v: number): number {
  const ratio = maxValue.value > 0 ? v / maxValue.value : 0
  return Math.round(ratio * props.height)
}

function format(v: number): string {
  return v.toLocaleString(undefined, {
    minimumFractionDigits: props.decimals,
    maximumFractionDigits: props.decimals,
  })
}
</script>

<template>
  <div
    class="flex items-end justify-center gap-12"
    :style="{ height: `${height + 48}px` }"
  >
    <div
      v-for="(bar, i) in bars"
      :key="i"
      class="flex flex-col items-center justify-end h-full"
    >
      <div class="mb-2 text-xl font-bold">
        {{ bar.valueLabel ?? unit + format(bar.value) }}
      </div>
      <div
        class="rounded-t transition-all duration-700 ease-out"
        :style="{
          width: `${barWidth}px`,
          height: `${barHeight(bar.value)}px`,
          backgroundColor: bar.color || '#64748b',
        }"
      />
      <img v-if="bar.icon" :src="bar.icon" class="mt-3 h-10" />
      <div class="mt-2 text-center text-base">{{ bar.label }}</div>
    </div>
  </div>
</template>
