---
layout: default
title: cdk-chapter
# 次のプロフィールページへアイコンが飛ぶので、View Transitions で繋ぐ
transition: view-transition
---

<script setup>
/**
 * 運営メンバー。ファイル名 = X のアカウント名なので、
 * 一覧はファイル名だけ持って、表示名とリンクはそこから組み立てる。
 * 並び順は支部の資料 (MC資料) と同じ 6 列 x 2 行。
 */
const FILES = [
  'tmk2154.jpg',
  'yamatatsu193.jpg',
  'HorseVictory.png',
  'tniizawa.jpg',
  'yktAWS.jpg',
  'hayatin.jpg',
  'WinterYukky.jpg',
  'rrrraaaaa6.jpg',
  'hedgehog051.jpg',
  'makies.png',
  'akikii__.jpg',
  'kawaaaas.jpg',
];

const members = FILES.map((file) => {
  const id = file.replace(/\.[^.]+$/, '');
  return { id, image: `/images/cdk-chapter/${file}`, url: `https://x.com/${id}` };
});
</script>

<div class="chapter-head">
  <img class="chapter-logo" src="/images/aboutme/jawsug-cdk-logo.png" />
  <div>

# JAWS-UG CDK支部

  <div class="chapter-lead">AWS CDKに関する知見やプラクティスを共有する専門支部</div>
  </div>
</div>

<div class="member-caption">運営メンバー</div>

<div class="member-grid">
  <a
    v-for="m in members"
    :key="m.id"
    class="member"
    :href="m.url"
    target="_blank"
    rel="noopener noreferrer"
  >
    <!-- 登壇者のアイコンだけ、次ページのプロフィール写真と同じ名前を付けて繋ぐ -->
    <img
      class="member-icon"
      :src="m.image"
      :alt="m.id"
      :style="m.id === 'akikii__' ? 'view-transition-name: akikii-icon' : undefined"
    />
    <span class="member-name">@{{ m.id }}</span>
  </a>
</div>

<BottomLink href="https://jawsug-cdk.connpass.com/" label="https://jawsug-cdk.connpass.com" />

<style>
.chapter-head {
  display: flex;
  align-items: center;
  gap: 1.4rem;
}

.chapter-logo {
  height: 3.6rem;
  width: auto;
}

/* h1 のデフォルト余白だと横並びにしたときに縦位置がずれる */
.chapter-head h1 {
  margin-bottom: 0.3rem;
}

.chapter-lead {
  font-size: 1.05rem;
  line-height: 1.5;
  color: #3a3941;
}

.member-caption {
  margin-top: 1.8rem;
  font-size: 0.95rem;
  letter-spacing: 0.08em;
  color: rgba(20, 36, 58, 0.6);
}

/*
 * 6 列 x 2 行。列幅は 1fr で等分し、アイコンの直径だけを決めているので、
 * 名前の長短 (@HorseVictory / @hayatin) で列がずれない。
 */
.member-grid {
  margin-top: 0.9rem;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  row-gap: 1.1rem;
  column-gap: 0.4rem;
}

/* テーマが a に破線の下線を引くので、カード全体のリンクでは消しておく */
.slidev-layout a.member,
.slidev-layout a.member:hover {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.45rem;
  text-decoration: none;
  border-bottom: none;
}

.member-icon {
  width: 4.4rem;
  height: 4.4rem;
  border-radius: 50%;
  object-fit: cover;
  background: #fff;
  /*
   * ぼかし付きの box-shadow は使わない。丸く抜いた画像に掛けると Chromium の
   * PDF 出力で影が角丸を無視した灰色の四角として焼き込まれる。
   */
  outline: 2px solid rgba(255, 255, 255, 0.9);
  outline-offset: -1px;
  transition: transform 0.15s ease;
}

.member:hover .member-icon {
  transform: translateY(-2px);
}

.member-name {
  font-size: 0.72rem;
  line-height: 1.2;
  color: #14243a;
  white-space: nowrap;
}

.slidev-layout a.member:hover .member-name {
  text-decoration: underline;
}
</style>

<!--
1. 今日の登壇者が所属している、JAWS-UG CDK支部の紹介です
2. AWS CDK について語り合う支部で、オンライン中心で勉強会を開催しています
3. 運営メンバーはこちらの12名です
4. connpass でイベントを告知しているので、興味があればぜひご参加ください
-->
