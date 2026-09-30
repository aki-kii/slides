<template>
  <div class="slidev-layout title">
    <!-- 上段: タイトル (右上のハッシュタグ帯を避ける) -->
    <div class="title-main">
      <slot />
    </div>

    <!-- 下段: 日付・登壇者など (JAWS SONIC ロゴの上) -->
    <div v-if="$slots.meta" class="title-meta">
      <slot name="meta" />
    </div>
  </div>
</template>

<style scoped>
.slidev-layout.title {
  position: relative;
  padding: 0;
  height: 100%;
  background-image: url('/images/theme/bg-title.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/*
 * 上のハッシュタグ帯 (〜12%) と下のロゴ帯 (76%〜) を避けて配置する。
 * 以下の rem は style.css でルートを 20px にする前 (16px) の見た目を保つため、
 * 1.25 で割った値にしてある。
 */
.title-main {
  position: absolute;
  top: 16%;
  bottom: 42%;
  left: 6%;
  right: 6%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.title-meta {
  position: absolute;
  top: 55%;
  left: 6%;
  right: 6%;
}
</style>

<style>
/*
 * 白文字は背景写真の上にそのまま置く。
 *
 * 読みやすさのために text-shadow を足さないこと。ぼかし付きの影は Chromium の
 * PDF 出力がベクタで表現できず、テキストの塊ごとにビットマップ化するため、
 * 書き出すと文字の背後に灰色の矩形が並ぶ。
 */
.slidev-layout.title :is(h1, h2, h3, p, a, div) {
  font-family: var(--font-display);
  color: #ffffff;
}

.slidev-layout.title h1 {
  font-size: 2.56rem;
  font-weight: 300;
  line-height: 1.25;
  letter-spacing: 0.02em;
  margin: 0;
}

/*
 * サブタイトルは和文が主。Neuropol は Latin しか持たないので和文は Noto Sans JP に
 * 落ちるが、読み込んでいるウェイトが 200/400/600 なので 300 を指定すると 200 が
 * 選ばれて極細になる。和文が潰れないよう 400 を指定する (Latin 側の見た目は変わらない)。
 */
.slidev-layout.title h2 {
  font-size: 1.28rem;
  font-weight: 400;
  line-height: 1.4;
  letter-spacing: 0.04em;
  margin: 1.2rem 0 0;
}

.slidev-layout.title .title-meta p {
  font-size: 0.92rem;
  font-weight: 400;
  line-height: 1.6;
  letter-spacing: 0.04em;
  margin: 0;
}

.slidev-layout.title a {
  text-decoration: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
}
</style>
