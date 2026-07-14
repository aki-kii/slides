<script setup lang="ts">
import { computed } from 'vue'

interface Segment {
  label: string
  value: number
  color?: string
  valueLabel?: string
  dashed?: boolean // 「空き」など枠線だけで表現したいとき
}

const props = withDefaults(
  defineProps<{
    segments: Segment[]
    max?: number // 全体の基準値（未指定なら合計値）
    unit?: string
    height?: number // バーの高さ(px)
    barWidth?: number
  }>(),
  {
    unit: '',
    height: 320,
    barWidth: 110,
  },
)

const total = computed(() =>
  props.segments.reduce((sum, s) => sum + s.value, 0),
)
const maxValue = computed(() => props.max ?? total.value)

function pct(v: number): number {
  return maxValue.value > 0 ? (v / maxValue.value) * 100 : 0
}
function valueText(s: Segment): string {
  return s.valueLabel ?? `${s.value}${props.unit}`
}
</script>

<template>
  <div class="flex gap-3" :style="{ height: `${height}px` }">
    <!-- 積み上げバー（下から積む） -->
    <div
      class="flex flex-col-reverse overflow-hidden rounded"
      :style="{ width: `${barWidth}px` }"
    >
      <div
        v-for="(seg, i) in segments"
        :key="i"
        class="w-full transition-all duration-500"
        :style="{
          height: `${pct(seg.value)}%`,
          backgroundColor: seg.dashed ? 'transparent' : seg.color || '#64748b',
          border: seg.dashed
            ? `2px dashed ${seg.color || '#cbd5e1'}`
            : 'none',
        }"
      />
    </div>

    <!-- 各セグメントに揃えたラベル -->
    <div class="flex flex-col-reverse">
      <div
        v-for="(seg, i) in segments"
        :key="i"
        class="flex items-center"
        :style="{ height: `${pct(seg.value)}%` }"
      >
        <span class="leading-tight whitespace-nowrap">
          <span class="font-bold">{{ valueText(seg) }}</span>
          <span class="opacity-70 ml-2">{{ seg.label }}</span>
        </span>
      </div>
    </div>
  </div>
</template>
