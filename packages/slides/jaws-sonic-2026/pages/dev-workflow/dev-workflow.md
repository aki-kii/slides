---
layout: section
transition: slide-left
---

# 開発フロー × CDKの検証

---
layout: default
transition: fade
clicks: 6
---

<script setup>
import { computed } from 'vue';
import { DEV_WORKFLOW_STEPS } from '../../devWorkflow';

// $clicks は Slidev がスライドの script setup に注入するので、宣言せずそのまま使う

/**
 * 上から1行ずつ出す。
 * いま説明している行は running、説明が終わった行は done にする。
 */
const rows = computed(() =>
  DEV_WORKFLOW_STEPS.slice(0, $clicks.value + 1).map((step, index) => ({
    ...step,
    status: index < $clicks.value ? 'done' : 'running',
  })),
);
</script>

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

# CDKアプリの開発フロー

<!-- 上下の軸は全部の層を説明し終えてから、まとめとして同時に出す -->
<div class="axis axis--top" v-click="5">
  <span class="arrow">▲</span>
  <span>実行サイクルが<strong>速い</strong> ／ 変更の回数が<strong>多い</strong></span>
</div>

<div class="flow">

<PipelineChecklist
  mono
  :interactive="false"
  :steps="rows"
  :gap="22"
  label-width="8.5em"
/>

</div>

<div class="axis axis--bottom" v-click="5">
  <span class="arrow">▼</span>
  <span>実行サイクルが<strong>遅い</strong> ／ 変更の回数が<strong>少ない</strong></span>
</div>

<style>
.flow :deep(.pipeline-step) {
  font-size: 0.98rem;
}

/* 上下に置く軸のキャプション。レールの左端に頭を揃える */
.axis {
  display: flex;
  align-items: center;
  gap: 0.45em;
  font-size: 1.05rem;
  color: #55545f;
}

.axis .arrow {
  color: #000;
  line-height: 1;
}

.axis--top {
  margin: 1.6rem 0 0.9rem;
}

.axis--bottom {
  margin-top: 0.9rem;
}
</style>

<Overlay clickStart="6">早いタイミングでエラーを潰すことで、検証サイクルを早められる！</Overlay>
