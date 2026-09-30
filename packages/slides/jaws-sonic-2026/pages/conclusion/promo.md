---
layout: section
transition: slide-left
---

# 宣伝

---
layout: default
title: promo
transition: slide-left
---

<ChapterLabel label="宣伝"/>

<div class="promo-catch">
  <div>久しぶりのテーマフリーLT会やります！</div>
</div>

<div class="promo-body">
  <img class="promo-thumb" src="/images/promo/jawsug-cdk-26.png" alt="JAWS-UG CDK支部 #26 CDKに関することならテーマフリー！真夏のLT大会" />
  <div class="promo-qr">
    <QrCode url="https://jawsug-cdk.connpass.com/event/402841/" :size="160" />
    <a class="promo-url" href="https://jawsug-cdk.connpass.com/event/402841/" target="_blank" rel="noopener noreferrer">jawsug-cdk.connpass.com/event/402841</a>
  </div>
</div>

<div class="promo-when">2026/9/8 (火) 19:30 〜 21:00 オンライン</div>

<style>
/* 大きく言い切る2行。ここが宣伝の主役 */
.promo-catch {
  margin-top: 2.4rem;
  text-align: center;
  font-size: 1.9rem;
  font-weight: 700;
  line-height: 1.35;
}

/* 左にイベントのサムネイル、右にQRコード */
.promo-body {
  margin-top: 1.4rem;
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  justify-items: center;
  gap: 2rem;
}

.promo-thumb {
  width: 100%;
  max-width: 28rem;
  border-radius: 10px;
}

.promo-qr {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
}

/* テーマが a に破線の下線を引くので、ここでは消して等幅で見せる */
.slidev-layout a.promo-url,
.slidev-layout a.promo-url:hover {
  font-family: var(--slidev-code-font-family, ui-monospace, monospace);
  font-size: 0.72rem;
  color: #3a3941;
  border-bottom: none;
  text-decoration: none;
}

.promo-when {
  margin-top: 1rem;
  text-align: center;
  font-size: 1.15rem;
  font-weight: 700;
  color: #3a3941;
}
</style>
