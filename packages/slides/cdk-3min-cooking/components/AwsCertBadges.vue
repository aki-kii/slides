<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

// public/ 配下の画像をビルド時にすべて検出し、キー(パス)だけ使う
const publicImagePaths = Object.keys(
  import.meta.glob('/public/**/*.{png,jpg,jpeg,svg,webp}'),
);

const props = defineProps({
  /** public/ 配下の画像ディレクトリ (例: "/images/certs") */
  dir: { type: String, default: null },
  /** dir の代わりに画像パスを直接指定 */
  items: { type: Array, default: null },
  /** 1段あたりの個数 */
  perRow: { type: Number, default: 8 },
  /** 六角形同士の隙間 (px) */
  gap: { type: Number, default: 2 },
});

const container = ref(null);
const containerWidth = ref(0);
const containerHeight = ref(0);

let ro = null;
onMounted(() => {
  if (!container.value) return;
  ro = new ResizeObserver(([entry]) => {
    containerWidth.value = entry.contentRect.width;
    containerHeight.value = entry.contentRect.height;
  });
  ro.observe(container.value);
});
onUnmounted(() => ro?.disconnect());

const images = computed(() => {
  if (props.items) return props.items;
  if (!props.dir) return [];
  const prefix = `/public${props.dir}/`;
  return publicImagePaths
    .filter(
      (p) => p.startsWith(prefix) && !p.slice(prefix.length).includes('/'),
    )
    .sort()
    .map((p) => p.replace(/^\/public/, ''));
});

const numRows = computed(() => Math.ceil(images.value.length / props.perRow));

const hexWidthFromWidth = computed(() => {
  if (!containerWidth.value) return Infinity;
  const offsetExtra = props.gap / 2;
  const available = containerWidth.value - offsetExtra;
  return (available - (props.perRow - 1) * props.gap) / props.perRow;
});

const hexWidthFromHeight = computed(() => {
  if (!containerHeight.value || numRows.value === 0) return Infinity;
  const hexH = containerHeight.value / (1 + 0.75 * (numRows.value - 1));
  return hexH / 1.1547;
});

const hexWidth = computed(() => Math.min(hexWidthFromWidth.value, hexWidthFromHeight.value));
const hexHeight = computed(() => hexWidth.value * 1.1547);

const rows = computed(() => {
  const result = [];
  for (let i = 0; i < images.value.length; i += props.perRow) {
    result.push({
      items: images.value.slice(i, i + props.perRow),
      offset: result.length % 2 === 1,
    });
  }
  return result;
});

const overlapPx = computed(() => -(hexHeight.value * 0.25 - props.gap) + 'px');
const offsetPx = computed(() => (hexWidth.value + props.gap) / 2 + 'px');
</script>

<template>
  <div ref="container" class="honeycomb">
    <div
      v-for="(row, ri) in rows"
      :key="ri"
      class="honeycomb-row"
      :style="{
        gap: gap + 'px',
        marginTop: ri > 0 ? overlapPx : '0',
        paddingLeft: row.offset ? offsetPx : '0',
        paddingRight: row.offset ? offsetPx : '0',
      }"
    >
      <div
        v-for="(item, ci) in row.items"
        :key="ci"
        class="hexagon"
        :style="{
          width: hexWidth + 'px',
          minWidth: hexWidth + 'px',
          height: hexHeight + 'px',
        }"
      >
        <img :src="typeof item === 'string' ? item : item.src" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.honeycomb {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  height: 100%;
}

.honeycomb-row {
  display: flex;
  justify-content: flex-start;
}

.hexagon {
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  overflow: hidden;
  flex-shrink: 0;
}

.hexagon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
