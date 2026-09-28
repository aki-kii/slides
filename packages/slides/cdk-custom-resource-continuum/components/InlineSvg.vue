<script setup lang="ts">
import { computed } from 'vue'

// SVG を <img> で読み込むと Web フォントが効かず、OS のフォント（ヒラギノ）で描かれる。
// そのとき PDF の文字情報が康熙部首（⾏ ⼊ ⽤ など）になるので、ページに直接埋め込んで
// Noto Sans JP で描かせる。
const props = defineProps<{ src: string; label?: string }>()

const svgs = import.meta.glob('../public/images/*.svg', {
  query: '?raw',
  import: 'default',
  eager: true,
}) as Record<string, string>

const svg = computed(() => svgs[`../public/images/${props.src}`] ?? '')
</script>

<template>
  <div class="inline-svg" role="img" :aria-label="props.label" v-html="svg" />
</template>

<style scoped>
.inline-svg :deep(svg) {
  display: block;
  width: 100%;
  height: auto;
}
</style>
