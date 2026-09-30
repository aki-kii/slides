<script setup lang="ts">
/**
 * 締めのページ。他の登壇資料 (zero-drift-cdk-ops) と同じ見た目にそろえてある。
 *
 *   ---
 *   layout: ending
 *   ---
 *
 *   # Thank You!
 *
 * 背景は青のグラデーション。右下にアイキャッチを置く前提なので、
 * 中身は左上寄せにして、右下を空けておく。
 */
</script>

<template>
  <div class="slidev-layout ending flex flex-col justify-center">
    <slot />
  </div>
</template>

<style>
.slidev-layout.ending {
  background: linear-gradient(155deg, #015d7d 0%, #0283b2 60%, #1aa9d1 100%);
  color: white;
  padding: 5rem 6rem;
  height: 100%;
  position: relative;
  align-items: flex-start;
  text-align: left;
}

.slidev-layout.ending h1 {
  color: white;
  font-size: 2.8rem;
  font-weight: 900;
  line-height: 1.25;
  letter-spacing: -0.01em;
  margin: 0 0 1rem;
}

.slidev-layout.ending p,
.slidev-layout.ending strong {
  color: rgba(255, 255, 255, 0.85);
}
</style>
