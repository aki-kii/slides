---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<br>

<ChatMessage from="user">コード見なくても全然うまくいくもんだな〜</ChatMessage>

<v-clicks>

<ChatMessage from="agent">...</ChatMessage>

</v-clicks>

---
layout: default
title: caught
transition: slide-left
clicks: 1
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<script setup>
/**
 * 直前の「コード見なくても全然うまくいくもんだな〜」への答え合わせ。
 * 実際は5回転んでいて、そのすべてをエージェントが自分で直している。
 *
 * desc は「何を直したか」ではなく「どんな事象を検出したか」で書く。
 * 個別のエラー内容はトレースで見せ終わっているので、ここでは
 * 5つが別々の種類の問題であることが伝わればよい。
 *
 * 層の並びは devWorkflow.js と同じ (下の層から) なので、
 * 3章で配った地図をそのまま埋め戻したものとして読める。
 * 下に行くほど「本来なら気付くのが遅い問題」になる。
 */
const CAUGHT = [
  { label: 'Linter', desc: '型検査は通ってしまう、CDK特有の書き方', status: 'done' },
  { label: 'cdk synth', desc: '組み合わせが成立していないプロパティ', status: 'done' },
  { label: 'cdk diff', desc: '意図しないリソースの作り直し', status: 'done' },
  { label: 'cdk validate', desc: 'AWSアカウントの状態との衝突', status: 'done' },
  { label: 'cdk diagnose', desc: 'デプロイして初めて分かる権限不足', status: 'done' },
];
</script>

## エージェントが自分で潰したもの

<div class="recap">

<PipelineChecklist
  mono
  :interactive="false"
  :steps="CAUGHT"
  :gap="18"
  label-width="9.5em"
/>

</div>

<div class="recap-point" v-click="1">壊れているところは、どれも<strong>機械がコードの場所まで</strong>教えてくれた</div>

<style>
.recap {
  margin-top: 1.4rem;
}

.recap :deep(.pipeline-step) {
  font-size: 0.98rem;
}

/* 説明は等幅にすると行が長くなるので、本文と同じサンセリフで置く */
.recap :deep(.desc) {
  color: #3a3941;
}

.recap-point {
  margin-top: 1.6rem;
  font-size: 1.35rem;
  font-weight: 700;
  line-height: 1.4;
}
</style>

<!--
1. 「うまくいく」と言いましたが、実際は5回転んでいます
2. エージェントの開発フローを下から登りながら、5つの層で検証が鳴りました
3. しかも下に行くほど、本来なら気付くのが遅い問題です
4. （クリック）どれも自分ではコードを読まずに、機械がコードの場所まで教えてくれました
-->
