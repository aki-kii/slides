---
layout: default
title: cdk-loop
transition: fade
---

<ChapterLabel label="CDK × コーディングエージェント"/>

## CDKは検証サイクルを回しやすい

<!--
  「書く → 検証する → 結果を見る → 直す」のループを 2x2 に置いて、
  CDKが効く2つの場所 (検証する / 結果を見る) にだけ注釈をぶら下げる。
  ここは配置が意味を持つので、md 側に余白を書き足さずグリッドで決める。

  注釈はクリックで出さない。出るまで空の箱が2つ並んで見えてしまうため。
-->
<div class="loop">
  <div class="loop-node loop-node--plain">書く</div>
  <div class="loop-arrow">→</div>
  <div class="loop-node">
    <div class="loop-node-name">検証する</div>
    <div class="loop-node-note">
      <span class="loop-tag">CDK</span>
      <span>実装が正しいか検証する仕組みがたくさん備わっている</span>
    </div>
  </div>

  <div class="loop-arrow">↑</div>
  <div class="loop-gap" />
  <div class="loop-arrow">↓</div>

  <div class="loop-node loop-node--plain">直す</div>
  <div class="loop-arrow">←</div>
  <div class="loop-node">
    <div class="loop-node-name">フィードバックを得る</div>
    <div class="loop-node-note">
      <span class="loop-tag">CDK</span>
      <span>検証に失敗した箇所が理由付きでわかる</span>
    </div>
  </div>
</div>

<div class="loop-point" v-click="1">エージェントはその検証結果を利用して、<strong>正しいコードに近づけていける</strong></div>

<style>
/*
 * 2x2 のループ。左列は語だけ、右列は注釈がぶら下がるので幅が違う。
 * 列幅を固定しないと、クリックで注釈が出た瞬間に箱の位置が動く。
 */
.loop {
  margin-top: 1.5rem;
  display: grid;
  grid-template-columns: 9em 3.5em 24em;
  grid-template-rows: auto auto auto;
  justify-content: start;
  align-items: center;
  column-gap: 0.8rem;
  row-gap: 0.5rem;
}

.loop-node {
  padding: 0.7rem 1rem;
  border: 2px solid rgba(20, 36, 58, 0.25);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.6);
}

/* 左列 (書く / 直す) は語だけなので中央、右列は注釈があるので左そろえ */
.loop-node--plain {
  text-align: center;
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.35;
}

.loop-node-name {
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.35;
}

 /* タグを1列目に固定して、折り返した2行目も本文の左端にそろえる */
.loop-node-note {
  margin-top: 0.4rem;
  display: grid;
  grid-template-columns: auto 1fr;
  column-gap: 0.5em;
  align-items: baseline;
  font-size: 0.85rem;
  line-height: 1.55;
  color: #3a3941;
}

/* CDKが効く場所だけに付ける印。地の文と混ざらないよう色を持たせる */
.loop-tag {
  padding: 0.05em 0.5em;
  border-radius: 4px;
  background: rgba(255, 45, 120, 0.12);
  color: #c0392b;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.loop-arrow {
  text-align: center;
  font-size: 1.5rem;
  line-height: 1;
  opacity: 0.55;
}

.loop-gap {
  /* 中央の空きセル。矢印の縦位置をそろえるためだけに置く */
}

.loop-point {
  margin-top: 1.4rem;
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.4;
}
</style>

<!--
1. コードを書く、検証する、結果を見る、直す。このループです
2. CDKには、実際にAWSへデプロイする前に、実装が正しいのかを検証する仕組みがたくさん備わっています
3. しかも壊れているところが、自分が書いたソースコードの場所で返ってきます
4. （クリック）エージェントはその検証結果を利用して、検証サイクルを回すことで、正しいコードに近づけていけます
5. （クリック）今日一番伝えたいのはここです
6. IaC、特にCDKは、コーディングエージェントでAWSインフラを構築するための検証サイクルを回すのに向いています
7. どんな検証があるのかは3章で、実際にどう回すのかは4章で見ていきます
-->
