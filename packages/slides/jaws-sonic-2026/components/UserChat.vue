<script setup>
/**
 * ニンゲンが喋っているところ。
 * 右に自分のアイコン、左に吹き出しを置いて、エージェント側 (AgentChat) と
 * 左右で向かい合うようにする。
 *
 *   <UserChat>おk、マージしといて</UserChat>
 *
 * クリックでセリフを切り替えたいときは texts に並べる。
 * texts[n] が n クリック目のセリフになり、最後の要素はそれ以降ずっと出たままになる。
 *
 *   <UserChat :texts="['どう？', 'おk、マージしといて']" />
 *
 * 切り替えにはクリックが必要なので、同じページに v-click を置くか、
 * frontmatter に clicks: <セリフ数 - 1> を書いておくこと。
 *
 * 行頭のコンポーネントタグは markdown が HTML ブロックとして素通しするため、
 * スロットに書いたバックティックはインラインコードにならない。
 * `cdk deploy` のようなコマンド名を混ぜたいときは texts を使うこと (下で <code> に変換している)。
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
  <div class="user-chat">
    <span class="bubble"><template v-if="parts"><template
        v-for="(part, i) in parts"
        :key="i"
      ><code v-if="part.code">{{ part.value }}</code><template v-else>{{ part.value }}</template></template></template><slot v-else /></span>
    <img class="icon" src="/images/aboutme/me-icon.png" alt="" />
  </div>
</template>

<style scoped>
.user-chat {
  display: flex;
  align-items: center;
  /* しっぽ (0.5rem) がアイコンに刺さらないだけの間隔をとる */
  gap: 1.1rem;
  width: fit-content;
  max-width: 100%;
  /* flex でも通常のブロックでも右に寄せる */
  align-self: flex-end;
  margin-left: auto;
  /* 前後の吹き出しと詰まって見えないように上下を空ける */
  margin-block: 0.6rem;
}

.bubble {
  position: relative;
  padding: 0.6rem 1.5rem;
  border-radius: 0.6rem;
  background: rgba(31, 117, 203, 0.12);
  font-size: 1.6rem;
  font-weight: 600;
}

/* 吹き出しのしっぽ。アイコンの方 (右) を向かせる */
.bubble::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 100%;
  transform: translateY(-50%);
  border: 0.5rem solid transparent;
  border-left-color: rgba(31, 117, 203, 0.12);
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

.icon {
  flex: none;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  object-fit: cover;
  /*
   * ぼかし付きの box-shadow は使わない。border-radius で丸く抜いた画像に掛けると
   * Chromium の PDF 出力で影が角丸を無視した灰色の四角として焼き込まれる。
   * 浮かせたい分は白いリングで代用する。
   */
  outline: 2px solid rgba(255, 255, 255, 0.9);
  outline-offset: -1px;
}
</style>
