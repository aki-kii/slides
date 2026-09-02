<script setup lang="ts">
const props = defineProps({
  image: {
    type: String,
    default: '',
  },
  name: {
    type: String,
    default: '',
  },
});
</script>

<template>
  <!-- padding:0 でテーマのデフォルトpadding を無効化し、自前で制御する -->
  <div class="slidev-layout profile flex flex-col h-full justify-center" style="padding:0;">
    <!-- 上段: 写真 + コンテンツ (ロゴ帯を避けるため上部を空ける) -->
    <div class="flex items-start" style="padding:70px 40px 0 80px; gap:64px;">
      <img
        :src="props.image"
        class="rounded-xl shadow-lg object-cover flex-shrink-0"
        style="width:300px; height:300px;"
      />
      <div class="flex flex-col justify-center" style="flex:1; height:300px;">
        <h2 class="font-bold" style="font-size:40px; margin-bottom:24px; color:#1a2a3a; line-height:1.15; white-space:nowrap;">{{ props.name }}</h2>
        <slot />
      </div>
    </div>

    <!-- 下段フッター -->
    <div
      v-if="$slots.footer"
      class="footer-slot flex items-center"
      style="height:150px; padding:24px 40px 20px 80px; gap:16px;"
    >
      <slot name="footer" />
    </div>
  </div>
</template>

<style>
/* JAWS SONIC 2026 テーマ背景 */
.slidev-layout.profile {
  background-image: url('/images/theme/bg-content.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* 明るい背景に合わせてコントラストを確保 */
.slidev-layout.profile .text-gray-300 { color: #34495e; }
.slidev-layout.profile .text-gray-400 { color: #5a6b7a; }

/* rem クラスをピクセル値で上書き (root font-size 変更の影響を受けないよう固定) */
.slidev-layout.profile .text-sm  { font-size: 15px; }
.slidev-layout.profile .text-xl  { font-size: 22px; }
.slidev-layout.profile .text-base { font-size: 19px; }
.slidev-layout.profile .h-6      { height: 28px; }
</style>

<style scoped>
.footer-slot :deep(img) {
  height: 100%;
  width: auto;
  object-fit: contain;
  flex-shrink: 0;
}
</style>
