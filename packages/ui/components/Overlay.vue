<script setup>
import { computed } from 'vue';

const props = defineProps({
  clickStart: {
    type: Number,
  },
  clickEnd: {
    type: Number,
  },
  position: {
    type: [Object, String],
    default: 'center',
  },
  fontSize: {
    type: String,
    default: '1.25rem',
  },
  // エクスポート（PDF/PNG）でこのオーバーレイを出さない。
  // Slidev の export は media: 'screen' でレンダリングするため @media print が
  // 効かず、印刷レイアウトでは絶対配置が崩れる。崩れるページに個別で付ける。
  hideOnExport: {
    type: Boolean,
    default: false,
  },
});

const presetPositions = {
  'top-left': { left: '2rem', top: '2rem' },
  'top-right': { right: '2rem', top: '2rem' },
  'bottom-left': { left: '2rem', bottom: '2rem' },
  'bottom-right': { right: '2rem', bottom: '2rem' },
  center: { left: '50%', top: '50%', transform: 'translate(-50%, -50%)' },
  'center-left': { left: '15rem', top: '5rem' },
  'center-right': { right: '12rem', top: '5rem' },
};

const isCenter = computed(() => props.position === 'center');

const getPositionStyle = () => {
  const boxStyle = {
    // backdrop-filter は Chromium の PDF 出力でラスタライズされず、
    // 中身のテキストごと消えるため使わない。背景は 90% 不透明で十分見える。
    background: 'rgba(180, 180, 180, 0.95)',
    color: '#1a1a1a',
    padding: '1rem 2rem',
    borderRadius: '1rem',
    maxWidth: '95%',
    lineHeight: '2rem',
  };

  // 中央配置は flex に任せる。absolute + translate だと
  // 印刷レイアウト（#print-container）でスケールが変わり位置がずれるため。
  if (isCenter.value) return boxStyle;

  const basePosition =
    typeof props.position === 'string'
      ? presetPositions[props.position]
      : props.position;

  return {
    position: 'absolute',
    ...basePosition,
    ...boxStyle,
  };
};
</script>

<template>
  <template v-if="clickEnd !== undefined">
    <div
      v-click.hide="clickEnd"
      class="print-hidden"
      :class="{ 'overlay-hide-on-export': hideOnExport }"
    >
      <div v-click="clickStart">
        <div class="overlay-backdrop" />
        <div class="overlay-root" :class="{ 'overlay-center': isCenter }">
          <div :style="getPositionStyle()"><slot /></div>
        </div>
      </div>
    </div>
  </template>
  <template v-else>
    <div
      v-click="clickStart"
      class="print-hidden"
      :class="{ 'overlay-hide-on-export': hideOnExport }"
    >
      <div class="overlay-backdrop" />
      <div class="overlay-root" :class="{ 'overlay-center': isCenter }">
        <div :style="getPositionStyle()"><slot /></div>
      </div>
    </div>
  </template>
</template>

<style scoped>
.overlay-root {
  position: absolute;
  inset: 0;
  z-index: 100;
}

.overlay-center {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.overlay-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.5);
  z-index: 99;
}

@media print {
  .overlay-backdrop {
    display: none;
  }
}

.print-hidden {
  display: block;
}


@media print {
  .print-hidden {
    display: none !important;
  }
}

div :deep(*) {
  font-size: v-bind(fontSize) !important;
}
</style>
