<script setup>
/**
 * コーディングエージェントが喋っているページのタイトル。
 * 左に Claude Code のアイコン (カニ)、右に吹き出しを置いて、
 * 誰が主体で動いているのかを一目で分かるようにする。
 *
 *   <AgentChat>実装するよー</AgentChat>
 *
 * クリックでセリフを切り替えたいときは texts に並べる。
 * texts[n] が n クリック目のセリフになり、最後の要素はそれ以降ずっと出たままになる。
 *
 *   <AgentChat :texts="['修正したよ！', 'Lintエラー消えた！']" />
 *
 * 切り替えにはクリックが必要なので、同じページに v-click を置くか、
 * frontmatter に clicks: <セリフ数 - 1> を書いておくこと。
 *
 * 中身は ChatMessage を h2 サイズで包んだだけ。吹き出しの見た目 (地・しっぽ・
 * インラインコードの詰め) はそちらに集約してある。
 * やり取りを縦に並べたいときは ChatLog / ChatMessage を直接使う。
 *
 * 行頭のコンポーネントタグは markdown が HTML ブロックとして素通しするため、
 * スロットに書いたバックティックはインラインコードにならない。
 * `cdk diff` のようなコマンド名を混ぜたいときは texts を使うこと。
 */
defineProps({
  /** クリックごとに切り替えるセリフ。省略時はスロットの中身をそのまま出す */
  texts: { type: Array, default: null },
});
</script>

<template>
  <ChatMessage class="agent-chat" tag="h2" from="agent" :texts="texts">
    <slot />
  </ChatMessage>
</template>

<style scoped>
.agent-chat {
  /* 見出しなので h2 のサイズ (style.css) に合わせる。アイコンも余白もこれに追従する */
  --chat-font-size: 1.7rem;
  /* 前後の要素と詰まって見えないように上下を空ける (h2 の margin は 0 になっている) */
  margin-block: 0.35em;
}
</style>
