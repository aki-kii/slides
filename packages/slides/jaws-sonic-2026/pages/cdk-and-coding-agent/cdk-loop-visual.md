---
layout: default
title: cdk-loop-visual
transition: fade
clicks: 1
---

<ChapterLabel label="CDK × コーディングエージェント"/>

## CDKの検証サイクル

<!--
  前ページの 2x2 の図を、エージェントと CDK の 2 者が回すループとして描き直したもの。
  外部 SVG ファイルにすると <img> の中からアイコンを参照できないので、
  ここではインライン SVG にしてアイコンを href で読んでいる。

  ループは半径 150 の正円。中心 (350,230) の円周上に 2 つのノードを置き、
  上下の弧をその円から切り出しているので、往路と復路が同じ丸みになる。
  流れは stroke-dashoffset のアニメーションで出す。
  往路 = 青 (エージェント → CDK)、復路 = 紫 (CDK → エージェント) で、
  voiceio の構成図と同じ色の使い方に揃えてある。

  テーマの CSS が SVG の <text> にも効いてしまい font-size 属性が負けるので、
  文字サイズは style 属性で指定している。
-->
<div class="cycle">
<svg viewBox="127 36 751 384" width="100%" role="img" aria-label="コーディングエージェントが実装し、CDKが検証して結果を返すループ。右にCDKが用意している検証の一覧">
  <defs>
    <marker id="cy-fwd" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#2b6cb0"/>
    </marker>
    <marker id="cy-back" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#8b5cf6"/>
    </marker>
  </defs>

  <!-- 往路: エージェントが実装する (正円の上半分) -->
  <path d="M252,152 A110,110 0 0 1 408,152" fill="none" stroke="#2b6cb0" stroke-width="4"
        stroke-dasharray="14 10" marker-end="url(#cy-fwd)">
    <animate attributeName="stroke-dashoffset" from="0" to="-24" dur="0.9s" repeatCount="indefinite"/>
  </path>
  <text x="330" y="100" style="font-size:21px" text-anchor="middle" font-weight="700" fill="#2b6cb0">実装・修正する</text>

  <!-- 復路: CDKが検証して結果を返す (正円の下半分) -->
  <path d="M408,308 A110,110 0 0 1 252,308" fill="none" stroke="#8b5cf6" stroke-width="4"
        stroke-dasharray="14 10" marker-end="url(#cy-back)">
    <animate attributeName="stroke-dashoffset" from="0" to="-24" dur="0.9s" repeatCount="indefinite"/>
  </path>
  <text x="330" y="372" style="font-size:21px" text-anchor="middle" font-weight="700" fill="#7c4fe0">検証してフィードバックを返す</text>

  <!-- 左: コーディングエージェント / 右: AWS CDK。キャプションは小さく添えるだけ -->
  <image href="/images/claude-code-icon.svg" x="186" y="196" width="68" height="68"/>
  <text x="220" y="286" style="font-size:14px" text-anchor="middle" font-weight="700" fill="#5a6b7a">コーディングエージェント</text>
  <image href="/images/cdk/awscdk.dio.png" x="410" y="200" width="60" height="60"/>
  <text x="440" y="286" style="font-size:14px" text-anchor="middle" font-weight="700" fill="#5a6b7a">AWS CDK</text>

  <!-- CDK 側にぶら下がる、検証するためのツール一覧 -->
  <line x1="546" y1="52" x2="546" y2="404" stroke="#d3d2d7" stroke-width="2"/>
  <text x="572" y="66" style="font-size:17px" font-weight="700" fill="#5a6b7a">CDKで利用できる検証ツール/コマンド</text>
  <g style="font-size:19px" font-weight="700" fill="#1f1e24" font-family="var(--slidev-code-font-family, ui-monospace, monospace)">
    <text x="572" y="110">Linter</text>
    <text x="572" y="152">型チェッカー</text>
    <text x="572" y="194">単体テスト</text>
    <text x="572" y="236">cdk synth</text>
    <text x="572" y="278">cdk diff</text>
    <text x="572" y="320">cdk validate</text>
    <text x="572" y="362">cdk drift</text>
    <text x="572" y="404">cdk diagnose</text>
  </g>
</svg>
</div>

<Overlay hide-on-export>検証サイクルを繰り返して正しい実装に近づけている</Overlay>

<style>
.cycle {
  margin-top: 0.9rem;
  /* 図が高いと下の一行がスライドからはみ出すので、幅で高さを抑える */
  max-width: 32rem;
  margin-left: auto;
  margin-right: auto;
}

.cycle-point {
  margin-top: 0.8rem;
  text-align: center;
  font-size: 1.15rem;
}
</style>
