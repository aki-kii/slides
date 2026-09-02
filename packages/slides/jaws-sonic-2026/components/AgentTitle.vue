<script setup>
/**
 * コーディングエージェントが喋っているページのタイトル。
 * 左に Claude Code のアイコン (カニ)、右に吹き出しを置いて、
 * 誰が主体で動いているのかを一目で分かるようにする。
 *
 *   <AgentTitle>実装するよー</AgentTitle>
 *
 * クリックでセリフを切り替えたいときは texts に並べる。
 * texts[n] が n クリック目のセリフになり、最後の要素はそれ以降ずっと出たままになる。
 *
 *   <AgentTitle :texts="['修正したよ！', 'Lintエラー消えた！']" />
 *
 * 切り替えにはクリックが必要なので、同じページに v-click を置くか、
 * frontmatter に clicks: <セリフ数 - 1> を書いておくこと。
 *
 * 行頭のコンポーネントタグは markdown が HTML ブロックとして素通しするため、
 * スロットに書いたバックティックはインラインコードにならない。
 * `cdk diff` のようなコマンド名を混ぜたいときは texts を使うこと (下で <code> に変換している)。
 */
import { computed } from 'vue';
import { useSlideContext } from '@slidev/client';

const props = defineProps({
  /** クリックごとに切り替えるセリフ。省略時はスロットの中身をそのまま出す */
  texts: { type: Array, default: null },
});

const { $clicks } = useSlideContext();

const text = computed(() => {
  const { texts } = props;
  if (!texts?.length) return null;
  // クリックが進みすぎても最後のセリフで止める
  return texts[Math.min(Math.max($clicks.value, 0), texts.length - 1)];
});

/** `...` で囲んだところをインラインコードとして描き分けるために分割する */
const parts = computed(() =>
  text.value == null
    ? null
    : text.value
        .split(/(`[^`]+`)/)
        .filter(Boolean)
        .map((part) =>
          part.startsWith('`') && part.endsWith('`')
            ? { code: true, value: part.slice(1, -1) }
            : { code: false, value: part },
        ),
);
</script>

<template>
  <h2 class="agent-title">
    <img class="icon" src="/images/claude-code-icon.svg" alt="" />
    <span class="bubble"><template v-if="parts"><template
        v-for="(part, i) in parts"
        :key="i"
      ><code v-if="part.code">{{ part.value }}</code><template v-else>{{ part.value }}</template></template></template><slot v-else /></span>
  </h2>
</template>

<style scoped>
.agent-title {
  display: flex;
  align-items: center;
  gap: 0.62em;
  width: fit-content;
  max-width: 100%;
}

.icon {
  flex: none;
  width: 1.45em;
  height: 1.45em;
}

.bubble {
  position: relative;
  padding: 0.14em 0.62em 0.2em;
  border-radius: 0.42em;
  background: rgba(217, 119, 87, 0.14);
}

/* 吹き出しのしっぽ。カニの方を向かせる */
.bubble::before {
  content: '';
  position: absolute;
  top: 50%;
  right: 100%;
  transform: translateY(-50%);
  border: 0.3em solid transparent;
  border-right-color: rgba(217, 119, 87, 0.14);
}

/* スロットの中身が段落に包まれても1行に収まるようにする */
.bubble :deep(p) {
  display: inline;
  margin: 0;
}

/* テーマのインラインコードは吹き出しから縦にはみ出すので、中に収まるまで詰める */
.bubble code,
.bubble :deep(code) {
  padding: 0.02em 0.22em;
  border-radius: 0.2em;
  background: rgba(255, 255, 255, 0.55);
}
</style>
