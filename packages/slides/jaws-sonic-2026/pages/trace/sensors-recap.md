---
layout: default
title: sensors-recap
transition: slide-left
clicks: 2
---

<script setup>
import { DEV_WORKFLOW_STEPS } from '../../devWorkflow';

/**
 * 層と検証の対応表なので、順序ではなく対応関係が読めればよい。
 * レール (アイコンと接続線) は出さず、pill だけを並べる。
 */
const rows = DEV_WORKFLOW_STEPS.map((step) => ({
  label: step.label,
  desc: step.sensor,
  status: 'done',
}));
</script>

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

# CDKで検証する仕組み

<div class="sensors">

<!--
  1クリック目で、今回のトレースで実際に効いた3つ (Linter / cdk validate / cdk diagnose) を赤くする。
  desc はプレーンな文字列なので、色を付けたい行だけスロットで差し替えている。
-->
<PipelineChecklist
  mono
  :interactive="false"
  :show-rail="false"
  :steps="rows"
  :gap="20"
  label-width="10.5em"
>
  <template #desc-0>
    <span :class="{ 'is-hit': $clicks >= 1 }">Linter</span> / 型チェッカー
  </template>
  <template #desc-3>
    CI (<span :class="{ 'is-hit': $clicks >= 1 }">cdk validate</span> / cdk drift / Linter / 単体テスト / 型チェッカー)
  </template>
  <template #desc-4>
    CD (cdk deploy) / <span :class="{ 'is-hit': $clicks >= 1 }">cdk diagnose</span>
  </template>
</PipelineChecklist>

</div>

<div class="sensors-point" v-click="2">検証サイクルを回すことでエージェントが<strong>自律的に修正</strong>できた！</div>

<style>
/* 今回のトレースで実際に効いた検証。1クリック目で赤くする */
.sensors :deep(.is-hit) {
  color: #c0392b;
  font-weight: 700;
  transition: color 0.25s ease;
}

.sensors-point {
  margin-top: 1.6rem;
  font-size: 1.35rem;
}

.sensors {
  margin-top: 2.2rem;
}

.sensors :deep(.pipeline-step) {
  font-size: 0.98rem;
  gap: 1.6em;
}

/* 検証名は等幅にすると PR 行が折り返すので、本文と同じサンセリフで置く */
.sensors :deep(.desc) {
  color: #3a3941;
}
</style>
