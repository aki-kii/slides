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
  <div class="slidev-layout profile flex flex-col h-full pl-20 pr-12">
    <!-- 上段: 写真 + コンテンツ -->
    <div class="flex items-center justify-start flex-1 gap-12">
      <!-- 左: 写真 -->
      <div class="flex-shrink-0 flex flex-col items-center">
        <img
          :src="props.image"
          class="w-64 h-64 rounded-xl shadow-lg object-cover"
        />
      </div>

      <!-- 右: 名前 + コンテンツ -->
      <div class="flex flex-col justify-center">
        <h2 class="text-4xl font-bold mb-6">{{ props.name }}</h2>
        <slot />
      </div>
    </div>

    <!-- 下段 -->
    <div v-if="$slots.footer" class="footer-slot flex items-center gap-8 border-t border-white/20 pt-2 h-32 pb-8">
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
