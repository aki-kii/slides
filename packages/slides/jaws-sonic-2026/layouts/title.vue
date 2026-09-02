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
.slidev-layout.title :is(h1, h2, h3, p, a, div) {
  font-family: var(--font-display);
  color: #ffffff;
  text-shadow: 0 2px 12px rgba(10, 20, 60, 0.55);
}

.slidev-layout.title h1 {
  font-size: 2.56rem;
  font-weight: 300;
  line-height: 1.25;
  letter-spacing: 0.02em;
  margin: 0;
}

.slidev-layout.title h2 {
  font-size: 1.28rem;
  font-weight: 300;
  line-height: 1.4;
  letter-spacing: 0.04em;
  margin: 1.2rem 0 0;
  opacity: 0.92;
}

.slidev-layout.title .title-meta p {
  font-size: 0.92rem;
  line-height: 1.6;
  letter-spacing: 0.04em;
  margin: 0;
}

.slidev-layout.title a {
  text-decoration: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
}
</style>
