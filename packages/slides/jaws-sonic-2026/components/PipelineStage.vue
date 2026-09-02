<script setup>
/**
 * 4章トレース用の2カラムレイアウト。
 * 左に開発フローのレール画像 (public/images/dev-workflow/) を、右に本文を置く。
 * レール画像は .pipeline-export.cjs で PipelineChecklist から書き出したもの。
 */
defineProps({
  /** レール画像のファイル名 (拡張子なし)。例: '2-git-commit-failed' */
  rail: { type: String, required: true },
  /** レール画像の幅 */
  railWidth: { type: String, default: '250px' },
});
</script>

<template>
  <div class="pipeline-stage">
    <img
      class="rail"
      :src="`/images/dev-workflow/${rail}.png`"
      :style="{ width: railWidth }"
      alt=""
    />
    <div class="body">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.pipeline-stage {
  display: flex;
  align-items: flex-start;
  gap: 2.5rem;
  margin-top: 0.5rem;
}

.rail {
  flex: none;
  object-fit: contain;
}

.body {
  flex: 1;
  min-width: 0;
}

/* 右カラムのコードブロックはスライド幅に収める */
.body :deep(pre) {
  max-width: 100%;
}
</style>
