<script setup>
/**
 * 4章トレース用の2カラムレイアウト。
 * 左に開発フローのレール (PipelineChecklist)、右に本文を置く。
 *
 *   <PipelineStage stage="commit" status="failed">
 *
 * stage には devWorkflow.js の key ('commit') / ラベル / index (1) のどれを渡してもよい。
 * status はその層の状態で、下の層は自動で done、上の層は pending になる。
 * クリックで進めたいときは status を式にする。
 *
 *   <PipelineStage stage="commit" :status="$clicks < 1 ? 'running' : 'done'">
 *
 * 以前は書き出した PNG (public/images/dev-workflow/) を貼っていたが、
 * 層の名前を変えるたびに再書き出しが要るのでコンポーネントで描くようにした。
 */
import { computed } from 'vue';
import { DEV_WORKFLOW_STEPS } from '../devWorkflow';

const props = defineProps({
  /** いまいる層。key / ラベル / index のいずれか */
  stage: { type: [String, Number], required: true },
  /** その層の状態。'pending' | 'running' | 'done' | 'failed' */
  status: { type: String, default: 'running' },
  /** レールに並べる層。既定は devWorkflow.js の全層 */
  steps: { type: Array, default: () => DEV_WORKFLOW_STEPS },
  /**
   * レールの見た目。文字サイズと pill 幅と間隔は
   * 「開発フロー × CDKの検証」章の図に合わせてあるが、トレース章は右に本文が
   * 並ぶので pill 幅だけ狭めてある (10.5em → 9em)。
   * 本文がもっと欲しいページは railLabelWidth / railFontSize を下げる。
   */
  railFontSize: { type: String, default: '0.98rem' },
  /** pill の最小幅。全部の pill がこの幅にそろう */
  railLabelWidth: { type: String, default: '9em' },
  /** 層同士の間隔 (px) */
  railGap: { type: Number, default: 22 },
  /** running の層のアイコンを回す */
  animate: { type: Boolean, default: true },
});

const index = computed(() =>
  typeof props.stage === 'number'
    ? props.stage
    : props.steps.findIndex(
        (step) => step.key === props.stage || step.label === props.stage,
      ),
);

/** 下の層は done、上の層は pending で埋める */
const railSteps = computed(() =>
  props.steps.map((step, i) => ({
    label: step.label,
    status:
      i < index.value ? 'done' : i === index.value ? props.status : 'pending',
  })),
);
</script>

<template>
  <div class="pipeline-stage">
    <div class="rail" :style="{ '--rail-font': railFontSize }">
      <PipelineChecklist
        mono
        :interactive="false"
        :animate="animate"
        :steps="railSteps"
        :gap="railGap"
        :label-width="railLabelWidth"
      />
    </div>
    <div class="body">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.pipeline-stage {
  display: flex;
  align-items: flex-start;
  gap: 2.5rem;
  margin-top: 0.5rem;
}

.rail {
  flex: none;
}

/* テーマの `.slidev-layout ol li` に負けないよう、レール側で文字サイズを決める */
.rail :deep(.pipeline-step) {
  font-size: var(--rail-font);
}

.body {
  flex: 1;
  min-width: 0;
}

/* 右カラムのコードブロックはスライド幅に収める */
.body :deep(pre) {
  max-width: 100%;
}
</style>
