<script setup lang="ts">
// モノレポの図（diagrams/monorepo-secretary.svg）をページに直接埋め込む。
// InlineSvg は実行時に「/public/images/<名前>」の文字列で SVG を引くので、
// dist を1枚の HTML に束ね直すビューアで画像のパスが書き換えられると、図が空になる。
// ここではビルド時に ?raw で文字列として取り込み、パスに頼らずに描く。
// （ページに埋め込むので、PDF でも Noto Sans JP で描かれる点は InlineSvg と同じ）
import svg from '../diagrams/monorepo-secretary.svg?raw'

defineProps<{ label?: string }>()
</script>

<template>
  <div class="inline-svg" role="img" :aria-label="label" v-html="svg" />
</template>

<style scoped>
.inline-svg :deep(svg) {
  display: block;
  width: 100%;
  height: auto;
}
</style>
