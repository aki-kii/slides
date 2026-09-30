<script setup>
/**
 * 吹き出しを縦に並べる会話ログ。中に <ChatMessage> を並べて使う。
 *
 *   <ChatLog>
 *
 *   <ChatMessage from="agent">実装したよ</ChatMessage>
 *
 *   <ChatMessage from="user">おk、マージしといて</ChatMessage>
 *
 *   </ChatLog>
 *
 * 吹き出しの間隔はここの gap で決めるので、ChatMessage 側は余白を持たない。
 * ページ冒頭の「誰が喋っているか」を出す見出しは ChatMessage の heading。
 *
 * 吹き出しの大きさは ChatMessage の既定 (1.6rem) のまま。
 * 中身が詰まるページだけ fontSize で落とす。
 *
 *   <ChatLog font-size="1.25rem">
 */
defineProps({
  /** 吹き出しの文字サイズ。省略時は ChatMessage の既定 (1.6rem) のまま */
  fontSize: { type: String, default: null },
});
</script>

<template>
  <div class="chat-log" :style="fontSize ? { '--chat-font-size': fontSize } : null">
    <slot />
  </div>
</template>

<style scoped>
.chat-log {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* 間隔はこちらの gap で決めるので、ChatMessage が単体用に持っている余白は消す */
.chat-log > :deep(.chat-message) {
  margin-block: 0;
}
</style>
