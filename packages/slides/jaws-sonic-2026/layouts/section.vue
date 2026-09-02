<script setup lang="ts">
/**
 * 章の扉ページ。bg-section-header.png を背景に敷いて、章タイトルだけを大きく置く。
 *
 *   ---
 *   layout: section
 *   label: 4章 トレース
 *   ---
 *
 *   ## エージェントの動きをトレースしてみよう
 *
 * label は見出しの上に出る小見出し (省略可)。本文ページの ChapterLabel と
 * 同じ文言を渡しておくと、扉と中身がつながって見える。
 */
defineProps({
  /** 見出しの上に置く章ラベル。空なら描画しない */
  label: {
    type: String,
    default: '',
  },
});
</script>

<template>
  <div class="slidev-layout section">
    <!-- 右上のロゴ帯 (〜14%) を避けたいので、中身は上下中央に置く -->
    <div class="section-body">
      <!-- アクセントはラベルの下線なので、ラベルが無ければ一緒に消す -->
      <template v-if="label">
        <div class="section-label">{{ label }}</div>
        <div class="section-accent" />
      </template>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.slidev-layout.section {
  position: relative;
  padding: 0;
  height: 100%;
  background-image: url('/images/theme/bg-section-header.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.section-body {
  position: absolute;
  top: 16%;
  bottom: 10%;
  left: 8%;
  right: 8%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* 「4章」の数字が Neuropol だと読みにくいので、ここは本文フォントのまま */
.section-label {
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: 0.18em;
  color: rgba(20, 36, 58, 0.6);
  margin-bottom: 0.9rem;
}

/* ラベルの下に引くアクセント。JAWS SONIC のロゴのピンク */
.section-accent {
  width: 4.2rem;
  height: 4px;
  border-radius: 2px;
  background: linear-gradient(90deg, #ff2d78 0%, #6c5ce7 100%);
  margin-bottom: 1.4rem;
}
</style>

<style>
/*
 * 背景がうっすら明るいグラデーションなので、濃紺の文字に白い滲みを添えて
 * 光の筋の上でも読めるようにする。
 */
.slidev-layout.section :is(h1, h2, h3, p) {
  color: #14243a;
  text-shadow: 0 1px 10px rgba(255, 255, 255, 0.7);
  margin: 0;
}

.slidev-layout.section :is(h1, h2) {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1.4;
  letter-spacing: 0.01em;
  /*
   * 和文は文字単位でどこでも折り返るので、長いタイトルで
   * 「〜してみ / よう」のような切れ方をしないよう balance で行長を揃える。
   * auto-phrase が効く環境ならそちらが文節で切ってくれる。
   */
  max-width: 24em;
  word-break: auto-phrase;
  text-wrap: balance;
}

/* 見出しに続く補足文があれば、一段落として下に置く */
.slidev-layout.section p {
  font-size: 1.25rem;
  line-height: 1.7;
  color: rgba(20, 36, 58, 0.75);
  margin-top: 1.2rem;
}
</style>
