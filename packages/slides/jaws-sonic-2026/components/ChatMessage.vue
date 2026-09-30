<script setup>
/**
 * 吹き出し1つ。会話を並べるときは <ChatLog> の中に入れて使う。
 *
 *   <ChatMessage from="agent">わかった！実装していくよー</ChatMessage>
 *   <ChatMessage from="user">会話ログをS3に保存するようにして</ChatMessage>
 *
 * from で話者を切り替える。agent は左、user は右に寄って向かい合う。
 * 同じ話者が続くときは2件目以降のアイコンを伏せるので、連続した発言でも
 * アイコンが並ばない (場所は空けたままなので吹き出しの端は揃う)。
 *
 * 大きさは --chat-font-size ひとつで決まる。アイコン・余白・しっぽは
 * すべて em なので、文字サイズを変えれば吹き出しごと拡大縮小する。既定は 1.6rem。
 * 詰めたいページは <ChatLog font-size="1.25rem"> のように囲んで落とす。
 * ページ冒頭の見出しに使うときは heading を付ける (h2 + 見出しサイズ)。
 *
 * 箇条書きなど markdown を入れたいときは、前後に空行を空けて書く。
 *
 *   <ChatMessage from="agent">
 *
 *   - 会話ログ用のS3バケットを追加
 *
 *   </ChatMessage>
 *
 * クリックでセリフを切り替えたいときは texts に並べる。
 * texts[n] が n クリック目のセリフになり、最後の要素はそれ以降ずっと出たままになる。
 *
 *   <ChatMessage from="user" :texts="['どう？', 'おk、マージしといて']" />
 *
 * 行頭のコンポーネントタグは markdown が HTML ブロックとして素通しするため、
 * スロットに書いたバックティックはインラインコードにならない。
 * `cdk deploy` のようなコマンド名を混ぜたいときは texts を使うこと。
 */
import { computed } from 'vue';
import { useChatParts } from '../chatText';

const props = defineProps({
  /** 話者。'agent' | 'user' */
  from: { type: String, default: 'agent' },
  /** クリックごとに切り替えるセリフ。省略時はスロットの中身をそのまま出す */
  texts: { type: Array, default: null },
  /**
   * ページ冒頭の見出しとして使う。h2 で描いて、文字を見出しサイズに上げる。
   *
   *   <ChatMessage from="agent" heading>Lintエラーが出ちゃった</ChatMessage>
   */
  heading: { type: Boolean, default: false },
  /**
   * アイコンを出さない。
   * ページ見出し (heading) と同じ話者が続くときに、カニが2つ並ぶのを避ける用。
   *
   *   <ChatMessage from="agent" no-icon>
   */
  noIcon: { type: Boolean, default: false },
});

const parts = useChatParts(props);

const isUser = computed(() => props.from === 'user');
const icon = computed(() =>
  isUser.value ? '/images/aboutme/me-icon.png' : '/images/claude-code-icon.svg',
);
</script>

<template>
  <component
    :is="heading ? 'h2' : 'div'"
    class="chat-message"
    :class="[isUser ? 'from-user' : 'from-agent', { heading }]"
  >
    <img v-if="!noIcon" class="icon" :src="icon" alt="" />
    <span class="bubble"><template v-if="parts"><template
        v-for="(part, i) in parts"
        :key="i"
      ><code v-if="part.code">{{ part.value }}</code><template v-else>{{ part.value }}</template></template></template><slot v-else /></span>
  </component>
</template>

<style scoped>
.chat-message {
  display: flex;
  align-items: center;
  /*
   * 大きさの基準。既定は会話が主役のページでちょうどよい 1.6rem で、
   * 下の em はすべてこれに乗る。呼び出し側は --chat-font-size だけ変えればよい。
   */
  font-size: var(--chat-font-size, 1.6rem);
  /* しっぽ (0.3em) がアイコンに刺さらないだけの間隔をとる */
  gap: 0.62em;
  width: 100%;
  /* ChatLog なしで並べても詰まって見えないように上下を空ける */
  margin-block: 0.35em;
}

/* 見出しは h2 のサイズ (style.css) に合わせる。アイコンも余白もこれに追従する */
.heading {
  --chat-font-size: 1.7rem;
}

/* ニンゲンは右に寄せて、アイコンを吹き出しの右に置く (row-reverse なので flex-start が右端) */
.from-user {
  flex-direction: row-reverse;
  justify-content: flex-start;
}

/*
 * 同じ話者が続くときはアイコンを繰り返さない。
 * visibility なので場所は残り、吹き出しの端は上下で揃ったままになる。
 */
.from-agent + .from-agent .icon,
.from-user + .from-user .icon {
  visibility: hidden;
}

.bubble {
  position: relative;
  max-width: 92%;
  padding: 0.3em 0.7em 0.36em;
  border-radius: 0.42em;
}

.from-agent .bubble {
  background: rgba(217, 119, 87, 0.14);
}

.from-user .bubble {
  background: rgba(31, 117, 203, 0.12);
}

/* 吹き出しのしっぽ。どちらもアイコンの方を向かせる */
.bubble::after {
  content: '';
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  border: 0.3em solid transparent;
}

.from-agent .bubble::after {
  right: 100%;
  border-right-color: rgba(217, 119, 87, 0.14);
}

.from-user .bubble::after {
  left: 100%;
  border-left-color: rgba(31, 117, 203, 0.12);
}

/* スロットの中身が段落に包まれても1行に収まるようにする */
.bubble :deep(p) {
  display: inline;
  margin: 0;
}

/* 箇条書きを入れたときに吹き出しから飛び出さないよう、リストの余白を落とす */
.bubble :deep(ul) {
  margin: 0;
}

/*
 * 段落もリストも style.css が要素セレクタで独自のサイズを持っているので、
 * 吹き出しの中では打ち消して .chat-message のサイズに揃える。
 */
.bubble :deep(p),
.bubble :deep(li) {
  font-size: inherit;
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
  width: 1.45em;
  height: 1.45em;
}

/* ニンゲンのアイコンは写真なので丸く抜く */
.from-user .icon {
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
