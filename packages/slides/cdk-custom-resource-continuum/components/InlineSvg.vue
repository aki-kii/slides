<script lang="ts">
let count = 0
</script>

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

// 埋め込むと id がページ全体で共有される。Slidev は前後のスライドも DOM に残すので、
// 別のスライドの矢じり（marker）と id がぶつかり、そのスライドが隠れると矢じりが消える。
// 埋め込むたびに id へ接頭辞を付けて、ぶつからないようにする。
const prefix = `isvg${++count}-`

const svg = computed(() => {
  const raw = svgs[`../public/images/${props.src}`] ?? ''
  return raw
    .replace(/\bid="([^"]+)"/g, `id="${prefix}$1"`)
    .replace(/url\(#([^)]+)\)/g, `url(#${prefix}$1)`)
    .replace(/href="#([^"]+)"/g, `href="#${prefix}$1"`)
})
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
