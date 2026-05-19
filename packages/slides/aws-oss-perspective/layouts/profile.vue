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
    <!-- 上段: 写真 + コンテンツ -->
    <div class="flex items-start" style="padding:30px 40px 0 80px; gap:64px;">
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
      style="height:162px; padding:32px 40px 20px 80px; gap:16px;"
    >
      <slot name="footer" />
    </div>
  </div>
</template>

<style scoped>
.footer-slot :deep(img) {
  height: 100%;
  width: auto;
  object-fit: contain;
  flex-shrink: 0;
}
</style>
