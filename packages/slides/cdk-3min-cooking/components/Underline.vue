<script setup>
import { computed } from 'vue';

const props = defineProps({
  // 絶対位置 (例: '120px', '10%')
  x: {
    type: String,
    required: true,
  },
  y: {
    type: String,
    required: true,
  },
  // 線の幅
  width: {
    type: String,
    default: '200px',
  },
  // 線の色
  color: {
    type: String,
    default: '#ef4444',
  },
  // 線の太さ (px)
  strokeWidth: {
    type: Number,
    default: 4,
  },
  // v-click の表示開始クリック番号
  clickStart: {
    type: Number,
  },
  // v-click の非表示開始クリック番号
  clickEnd: {
    type: Number,
  },
  // アニメーション時間
  duration: {
    type: String,
    default: '0.6s',
  },
  // イージング
  easing: {
    type: String,
    default: 'ease-out',
  },
});

const svgHeight = computed(() => props.strokeWidth + 6);
const lineY = computed(() => (props.strokeWidth + 6) / 2);
</script>

<template>
  <template v-if="clickEnd !== undefined">
    <div v-click.hide="clickEnd" class="underline-wrapper" :style="{
      position: 'absolute',
      left: x,
      top: y,
      width: width,
      height: `${svgHeight}px`,
      pointerEvents: 'none',
      overflow: 'visible',
      zIndex: 10,
    }">
      <div v-click="clickStart" class="underline-wrapper" :style="{
        position: 'absolute',
        left: 0,
        top: 0,
        width: '100%',
        height: `${svgHeight}px`,
        overflow: 'visible',
      }">
        <svg width="100%" :height="svgHeight" overflow="visible">
          <line
            pathLength="1"
            x1="0" :y1="lineY"
            x2="100%" :y2="lineY"
            :stroke="color"
            :stroke-width="strokeWidth"
            stroke-linecap="round"
            class="underline-line"
          />
        </svg>
      </div>
    </div>
  </template>
  <template v-else>
    <div v-click="clickStart" class="underline-wrapper" :style="{
      position: 'absolute',
      left: x,
      top: y,
      width: width,
      height: `${svgHeight}px`,
      pointerEvents: 'none',
      overflow: 'visible',
      zIndex: 10,
    }">
      <svg width="100%" :height="svgHeight" overflow="visible">
        <line
          pathLength="1"
          x1="0" :y1="lineY"
          x2="100%" :y2="lineY"
          :stroke="color"
          :stroke-width="strokeWidth"
          stroke-linecap="round"
          class="underline-line"
        />
      </svg>
    </div>
  </template>
</template>

<style scoped>
.underline-line {
  stroke-dasharray: 1;
  stroke-dashoffset: 0;
  animation: draw v-bind(duration) v-bind(easing) forwards;
}

/* v-click で非表示の間はアニメーションをリセット */
.slidev-vclick-hidden .underline-line {
  animation: none;
  stroke-dashoffset: 1;
}

@keyframes draw {
  from {
    stroke-dashoffset: 1;
  }
  to {
    stroke-dashoffset: 0;
  }
}
</style>
