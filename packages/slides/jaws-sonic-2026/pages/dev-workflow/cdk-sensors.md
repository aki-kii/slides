---
layout: default
title: cdk-sensors
transition: slide-left
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

<PipelineChecklist
  mono
  :interactive="false"
  :show-rail="false"
  :steps="rows"
  :gap="20"
  label-width="10.5em"
/>

</div>

<div class="sensors-point">これらのタイミングで検証が走るように設定しています</div>

<style>
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
