<script setup>
import { computed } from 'vue';

const props = defineProps({
  text: {
    type: String,
    required: true,
  },
  // 白背景でも読めるよう、明度の高い純色は避けた7色
  colors: {
    type: Array,
    default: () => [
      '#e74c3c',
      '#e67e22',
      '#d4a017',
      '#27ae60',
      '#2980b9',
      '#6c5ce7',
      '#8e44ad',
    ],
  },
});

const chars = computed(() => [...props.text]);

const hexToRgb = (hex) => [
  Number.parseInt(hex.slice(1, 3), 16),
  Number.parseInt(hex.slice(3, 5), 16),
  Number.parseInt(hex.slice(5, 7), 16),
];

const lerp = (a, b, t) => Math.round(a + (b - a) * t);

// 文字位置に応じて色を線形補間する。
// CSS の background-clip: text は PDF エクスポートでグラデーションの座標が
// ずれて一部の色域しか乗らないため、1文字ずつ color を指定している。
const colorAt = (index) => {
  const total = chars.value.length;
  const stops = props.colors;
  if (total <= 1 || stops.length === 1) return stops[0];

  const pos = (index / (total - 1)) * (stops.length - 1);
  const i = Math.min(Math.floor(pos), stops.length - 2);
  const t = pos - i;
  const [r1, g1, b1] = hexToRgb(stops[i]);
  const [r2, g2, b2] = hexToRgb(stops[i + 1]);

  return `rgb(${lerp(r1, r2, t)}, ${lerp(g1, g2, t)}, ${lerp(b1, b2, t)})`;
};
</script>

<template>
  <span class="rainbow-text">
    <span
      v-for="(char, index) in chars"
      :key="index"
      :style="{ color: colorAt(index) }"
      >{{ char }}</span
    >
  </span>
</template>

<style scoped>
.rainbow-text {
  font-weight: 900;
}
</style>
