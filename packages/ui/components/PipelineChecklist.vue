<script setup>
import { usePipelineStatuses } from '../composables/pipelineStatus';

const props = defineProps({
  /** 手順の配列。文字列 or { label, status } を並べる */
  steps: { type: Array, required: true },
  /**
   * 進行中の手順の index。
   * これより前は done、これ自身は running、これより後は pending になる。
   * Slidev のクリックと連動させるなら :current="$clicks" を渡す
   * (frontmatter の clicks に手順数を書いておく)。
   * 未指定なら steps 側の status をそのまま使う。
   */
  current: { type: Number, default: null },
  /**
   * 失敗した手順の index。
   * これより前は done、これ自身は failed、これより後は pending になる。
   * current より優先される。
   */
  failedAt: { type: Number, default: null },
  /** クリックで pending → running → done → failed → pending と状態を回す */
  interactive: { type: Boolean, default: true },
  /** running アイコンを回転させる */
  animate: { type: Boolean, default: true },
  /** ラベルを等幅フォントにする (コマンド名向け) */
  mono: { type: Boolean, default: false },
  /** アイコンの直径 (px) */
  iconSize: { type: Number, default: 34 },
  /** 手順同士の間隔 (px) */
  gap: { type: Number, default: 16 },
  /**
   * ラベルの最小幅 (CSS の長さ)。
   * 指定すると全部の pill が同じ幅になり、右に置いた説明文が縦に揃う。
   */
  labelWidth: { type: String, default: null },
  /**
   * 左のレール (状態アイコンと接続線) を出すか。
   * false にすると pill だけが縦に並ぶので、順序ではなく対応関係を見せたいときに使う。
   */
  showRail: { type: Boolean, default: true },
});

const { resolved, cycle } = usePipelineStatuses(props);
</script>

<template>
  <ol
    class="pipeline"
    :class="{ 'is-mono': mono, 'no-animate': !animate }"
    :style="{
      '--icon-size': `${iconSize}px`,
      '--gap': `${gap}px`,
      '--label-width': labelWidth ?? '0',
    }"
  >
    <li
      v-for="(step, index) in resolved"
      :key="index"
      class="pipeline-step"
      :class="[`is-${step.status}`, { 'is-interactive': interactive }]"
      @click="cycle(index)"
    >
      <div v-if="showRail" class="rail">
        <!-- 前後の手順とをつなぐ線。完了済みの手順から伸びる線だけ色を付ける -->
        <span
          v-if="index > 0"
          class="line line--up"
          :class="{ 'is-done': resolved[index - 1].status === 'done' }"
        />
        <span
          v-if="index < resolved.length - 1"
          class="line line--down"
          :class="{ 'is-done': step.status === 'done' }"
        />

        <svg class="icon" viewBox="0 0 16 16" aria-hidden="true">
          <circle class="ring" cx="8" cy="8" r="7" />
          <!-- done: チェック -->
          <path
            v-if="step.status === 'done'"
            class="check"
            d="M4.6 8.3 L7 10.6 L11.5 5.7"
          />
          <!-- running: 時計まわりに欠けた円 (GitLab の running アイコン風) -->
          <path
            v-else-if="step.status === 'running'"
            class="wedge"
            d="M8 8 L8 2.6 A5.4 5.4 0 1 0 13.4 8 Z"
          />
          <!-- failed: ✕ -->
          <path
            v-else-if="step.status === 'failed'"
            class="cross"
            d="M5.7 5.7 L10.3 10.3 M10.3 5.7 L5.7 10.3"
          />
          <!-- pending: 中央のドット -->
          <circle v-else class="dot" cx="8" cy="8" r="2.7" />
        </svg>
      </div>

      <div class="label">
        <slot :name="`step-${index}`" :step="step" :index="index">
          {{ step.label }}
        </slot>
      </div>

      <!-- pill の右に置く説明文。steps に desc を持たせるか、スロットで差し込む -->
      <div v-if="step.desc || $slots[`desc-${index}`]" class="desc">
        <slot :name="`desc-${index}`" :step="step" :index="index">
          {{ step.desc }}
        </slot>
      </div>
    </li>
  </ol>
</template>

<style scoped>
.pipeline {
  --done: #108548;
  --running: #1f75cb;
  --failed: #dd2b0e;
  --pending: #9b9aa3;
  --line: #d3d2d7;

  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--gap);
  width: fit-content;
}

.pipeline-step {
  display: flex;
  align-items: center;
  gap: 0.8em;
  margin: 0;
  padding: 0;
  --color: var(--pending);
}

.pipeline-step.is-done {
  --color: var(--done);
}

.pipeline-step.is-running {
  --color: var(--running);
}

.pipeline-step.is-failed {
  --color: var(--failed);
}

.pipeline-step.is-interactive {
  cursor: pointer;
  user-select: none;
}

/* アイコンと、上下に伸びる接続線 */
.rail {
  position: relative;
  flex: none;
  width: var(--icon-size);
  height: var(--icon-size);
}

.icon {
  position: relative;
  width: 100%;
  height: 100%;
  color: var(--color);
  transition: color 0.25s ease;
}

.ring {
  fill: #ffffff;
  stroke: currentColor;
  stroke-width: 1.6;
}

.check,
.cross {
  fill: none;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.wedge {
  fill: currentColor;
  transform-origin: 8px 8px;
  animation: pipeline-spin 1.6s linear infinite;
}

.pipeline.no-animate .wedge {
  animation: none;
}

.dot {
  fill: currentColor;
}

.line {
  position: absolute;
  left: 50%;
  width: 2px;
  transform: translateX(-50%);
  background: var(--line);
  transition: background 0.25s ease;
}

.line.is-done {
  background: var(--done);
}

.line--up {
  bottom: 50%;
  height: calc(50% + var(--gap));
}

.line--down {
  top: 50%;
  height: calc(50% + var(--gap));
}

/* ラベル (GitLab のジョブ pill 風) */
.label {
  padding: 0.3em 1em;
  border: 1.5px solid var(--color);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.92);
  /*
   * ぼかし付きの box-shadow は使わない。Chromium の PDF 出力が影を角丸を無視した
   * 灰色の矩形として焼き込むため、書き出すと pill の背後に四角が並ぶ。
   * (opacity が掛かる is-pending だけは正常に出るので画面では気付きにくい)
   * 枠線と不透明に近い地があるので、影が無くても pill として読める。
   */
  color: #1f1e24;
  line-height: 1.5;
  white-space: nowrap;
  transition:
    border-color 0.25s ease,
    opacity 0.25s ease;
}

.label {
  min-width: var(--label-width);
  text-align: center;
}

/* pill の右の説明文。pill と違って本文のフォントで読ませる */
.desc {
  color: #3a3941;
  line-height: 1.5;
}

.pipeline-step.is-pending .desc {
  opacity: 0.85;
}

.pipeline.is-mono .label {
  font-family: var(--slidev-code-font-family, ui-monospace, monospace);
  font-size: 0.92em;
}

.pipeline-step.is-pending .label {
  border-color: var(--line);
  opacity: 0.7;
}

@keyframes pipeline-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
