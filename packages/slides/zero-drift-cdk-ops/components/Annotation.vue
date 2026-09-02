<script setup lang="ts">
withDefaults(
  defineProps<{
    x: string // 横位置 (left): '40%' や '200px'
    y: string // 縦位置 (top)
    width?: string // 赤線の長さ
    color?: string
    label?: string // コメント（slotでも可）
    fontSize?: string
    align?: 'left' | 'center' | 'right' // コメント文字の揃え
  }>(),
  {
    width: '120px',
    color: '#e11d48',
    fontSize: '0.9rem',
    align: 'center',
  },
)
</script>

<template>
  <div class="annotation" :style="{ left: x, top: y, width }">
    <div class="annotation-line" :style="{ backgroundColor: color }" />
    <div
      class="annotation-label"
      :style="{ color, fontSize, textAlign: align }"
    >
      <slot>{{ label }}</slot>
    </div>
  </div>
</template>

<style scoped>
.annotation {
  position: absolute;
  z-index: 50;
  pointer-events: none;
}
.annotation-line {
  width: 100%;
  height: 3px;
  border-radius: 2px;
}
.annotation-label {
  /* 線の中心にコメントを揃える（線より長くても両側に均等にはみ出す） */
  width: max-content;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  margin-top: 0.25rem;
  font-weight: 700;
  white-space: nowrap;
  line-height: 1.3;
}
</style>
