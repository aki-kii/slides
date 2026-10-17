<template>
  <span class="tag" :style="tagStyle">{{ name }}</span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  name: string
  color?: string
}>()

function resolveColorToRgb(color: string): [number, number, number] {
  if (typeof document === 'undefined') return [107, 114, 128]
  const canvas = document.createElement('canvas')
  canvas.width = canvas.height = 1
  const ctx = canvas.getContext('2d')!
  ctx.fillStyle = color
  ctx.fillRect(0, 0, 1, 1)
  const [r, g, b] = ctx.getImageData(0, 0, 1, 1).data
  return [r, g, b]
}

function rgbToHsl(r: number, g: number, b: number): [number, number, number] {
  r /= 255; g /= 255; b /= 255
  const max = Math.max(r, g, b), min = Math.min(r, g, b)
  let h = 0, s = 0
  const l = (max + min) / 2

  if (max !== min) {
    const d = max - min
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min)
    switch (max) {
      case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break
      case g: h = ((b - r) / d + 2) / 6; break
      case b: h = ((r - g) / d + 4) / 6; break
    }
  }

  return [Math.round(h * 360), Math.round(s * 100), Math.round(l * 100)]
}

const tagStyle = computed(() => {
  const color = props.color ?? '#6b7280'
  const [r, g, b] = resolveColorToRgb(color)
  const [h, s] = rgbToHsl(r, g, b)

  return {
    backgroundColor: `hsl(${h}, ${s}%, 93%)`,
    color: `hsl(${h}, ${Math.min(s + 10, 100)}%, 28%)`,
    borderColor: `hsl(${h}, ${s}%, 75%)`,
  }
})
</script>

<style scoped>
.tag {
  display: inline-block;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.85em;
  padding: 0.1em 0.5em;
  border-radius: 0.3em;
  border: 1px solid;
  line-height: 1.5;
  white-space: nowrap;
}
</style>
