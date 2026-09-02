<script setup>
import { computed } from 'vue';
import { usePipelineStatuses } from '../composables/pipelineStatus';

const props = defineProps({
  /**
   * 手順。下の段 (実行頻度が高いもの) から順に並べる。
   * 末尾の topCount 個は三角形の外 (頂点の上) に置かれる。
   */
  steps: { type: Array, required: true },
  /** steps の末尾から何個を頂点の上に出すか */
  topCount: { type: Number, default: 0 },
  /**
   * 'plain'  : 状態を持たない構造図として、全段を同じ色で描く
   * 'status' : done / running / failed / pending を段の色で表す
   */
  variant: { type: String, default: 'plain' },
  /**
   * 進行中の手順の index。これより前は done、これ自身は running、後は pending。
   * Slidev のクリックと連動させるなら :current="$clicks" を渡す (variant="status" 時)
   */
  current: { type: Number, default: null },
  /** 失敗した手順の index。current より優先される */
  failedAt: { type: Number, default: null },
  /** クリックで pending → running → done → failed → pending と状態を回す */
  interactive: { type: Boolean, default: true },
  /** running の段を明滅させる */
  animate: { type: Boolean, default: true },
  /** 左に「頻度 / サイクル」の軸を表示する */
  showAxis: { type: Boolean, default: false },
  /** 左の軸の上端・下端のラベル (1 要素 1 行) */
  axisTop: { type: Array, default: () => ['頻度: 少', '1 サイクル: 遅い'] },
  axisBottom: { type: Array, default: () => ['頻度: 多', '1 サイクル: 速い'] },
  /** 各段の高さの比率 (頂点から順)。足りない分は 1 で埋める */
  bandWeights: { type: Array, default: () => [1.6, 1, 1, 1] },
});

const { resolved, cycle } = usePipelineStatuses(props);

// --- 図形の基準値 -------------------------------------------------------
const BASE_W = 620; // 底辺の長さ
const TRI_H = 400; // 三角形の高さ
const TOP_MARGIN = 40;
const PILL_H = 52; // 頂点の上に置くステップの高さ
const TOP_GAP = 62; // 頂点 (や下のステップ) との間隔
const AXIS_X = 92;
const LABEL_POS = 0.66; // 段の中でラベルを置く位置 (下寄りだと幅に余裕が出る)
const FONT_MAX = 20;

const isPlain = computed(() => props.variant === 'plain');
const clickable = computed(() => props.interactive && !isPlain.value);

// 軸を出すときだけ左に場所を空ける
const cx = computed(() => (props.showAxis ? 440 : BASE_W / 2 + 16));
const vbW = computed(() => (props.showAxis ? 780 : BASE_W + 32));

const bandSteps = computed(() =>
  resolved.value.slice(0, Math.max(resolved.value.length - props.topCount, 0)),
);
const topSteps = computed(() =>
  resolved.value.slice(Math.max(resolved.value.length - props.topCount, 0)),
);

const apexY = computed(
  () => TOP_MARGIN + topSteps.value.length * (PILL_H + TOP_GAP),
);
const baseY = computed(() => apexY.value + TRI_H);
const viewBox = computed(
  () => `0 0 ${vbW.value} ${baseY.value + (props.showAxis ? 62 : 20)}`,
);

// 頂点から順に、各段の上端・下端の位置 (0〜1) を求める
const bandFractions = computed(() => {
  const n = bandSteps.value.length;
  const weights = Array.from({ length: n }, (_, i) => props.bandWeights[i] ?? 1);
  const total = weights.reduce((a, b) => a + b, 0);
  const fractions = [0];
  weights.forEach((w) => fractions.push(fractions.at(-1) + w / total));
  return fractions;
});

const bands = computed(() =>
  // steps は下の段から並んでいるので、描画は逆順 (頂点から) にする
  bandSteps.value
    .map((step, index) => ({ step, index }))
    .reverse()
    .map(({ step, index }, row) => {
      const fTop = bandFractions.value[row];
      const fBot = bandFractions.value[row + 1];
      const yTop = apexY.value + fTop * TRI_H;
      const yBot = apexY.value + fBot * TRI_H;
      const wTop = (BASE_W * fTop) / 2;
      const wBot = (BASE_W * fBot) / 2;
      const labelY = yTop + (yBot - yTop) * LABEL_POS;
      return {
        step,
        index,
        points: [
          `${cx.value - wTop},${yTop}`,
          `${cx.value + wTop},${yTop}`,
          `${cx.value + wBot},${yBot}`,
          `${cx.value - wBot},${yBot}`,
        ].join(' '),
        labelY,
        // 上の段ほど幅が狭いので、はみ出さないよう文字を縮める
        fontSize: Math.min(
          FONT_MAX,
          ((BASE_W * (labelY - apexY.value)) / TRI_H) * 0.78 /
            (step.label.length * 0.6),
        ),
      };
    }),
);

// 頂点の上のステップ。頂点に近いものから上へ積む
const tops = computed(() =>
  topSteps.value.map((step, k) => {
    const cy = apexY.value - TOP_GAP - PILL_H / 2 - k * (PILL_H + TOP_GAP);
    const w = Math.max(step.label.length * 12 + 44, 160);
    return {
      step,
      index: bandSteps.value.length + k,
      x: cx.value - w / 2,
      y: cy - PILL_H / 2,
      w,
      cy,
      arrowFrom: cy + PILL_H / 2 + TOP_GAP,
      arrowTo: cy + PILL_H / 2,
    };
  }),
);

const statusClass = (step) => (isPlain.value ? 'is-plain' : `is-${step.status}`);
const axisTopY = computed(() => apexY.value + 40);
</script>

<template>
  <div class="pyramid" :class="{ 'no-animate': !animate }">
    <svg :viewBox="viewBox" class="pyramid-svg">
      <!-- 左の軸: 下ほど高頻度・短サイクル -->
      <g v-if="showAxis" class="axis">
        <line :x1="AXIS_X" :y1="axisTopY" :x2="AXIS_X" :y2="baseY" />
        <polygon
          :points="`${AXIS_X},${axisTopY - 12} ${AXIS_X - 6},${axisTopY} ${AXIS_X + 6},${axisTopY}`"
        />
        <polygon
          :points="`${AXIS_X},${baseY + 12} ${AXIS_X - 6},${baseY} ${AXIS_X + 6},${baseY}`"
        />
        <text
          v-for="(line, i) in axisTop"
          :key="`t${i}`"
          class="axis-label"
          :x="AXIS_X"
          :y="axisTopY - 40 + i * 20"
        >
          {{ line }}
        </text>
        <text
          v-for="(line, i) in axisBottom"
          :key="`b${i}`"
          class="axis-label"
          :x="AXIS_X"
          :y="baseY + 34 + i * 20"
        >
          {{ line }}
        </text>
      </g>

      <!-- 三角形の各段 -->
      <g
        v-for="band in bands"
        :key="band.index"
        class="band"
        :class="[statusClass(band.step), { 'is-interactive': clickable }]"
        @click="clickable && cycle(band.index)"
      >
        <polygon :points="band.points" />
        <text
          :x="cx"
          :y="band.labelY"
          :style="{ fontSize: `${band.fontSize}px` }"
        >
          {{ band.step.label }}
        </text>
      </g>

      <!-- 頂点の上のステップ (topCount > 0 のときだけ) -->
      <g
        v-for="top in tops"
        :key="top.index"
        class="top-step"
        :class="[statusClass(top.step), { 'is-interactive': clickable }]"
        @click="clickable && cycle(top.index)"
      >
        <line
          class="arrow-line"
          :x1="cx"
          :y1="top.arrowFrom"
          :x2="cx"
          :y2="top.arrowTo + 10"
        />
        <polygon
          class="arrow-head"
          :points="`${cx},${top.arrowTo} ${cx - 7},${top.arrowTo + 12} ${cx + 7},${top.arrowTo + 12}`"
        />
        <rect
          :x="top.x"
          :y="top.y"
          :width="top.w"
          :height="PILL_H"
          :rx="PILL_H / 2"
        />
        <text :x="cx" :y="top.cy">{{ top.step.label }}</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.pyramid {
  --plain: #4a4952;
  --plain-fill: #f5f5f7;
  --done: #108548;
  --done-fill: #e9f5ee;
  --running: #1f75cb;
  --running-fill: #e7f0fb;
  --failed: #dd2b0e;
  --failed-fill: #fdeceb;
  --pending: #c9c8ce;
  --pending-fill: #f4f4f6;
  --ink: #1f1e24;

  width: 100%;
}

.pyramid-svg {
  display: block;
  width: 100%;
  height: auto;
  overflow: visible;
}

/* 段・頂点上ステップの共通の状態色 */
.band,
.top-step {
  --color: var(--pending);
  --fill: var(--pending-fill);
  --text: #8b8a92;
}

.band.is-plain,
.top-step.is-plain {
  --color: var(--plain);
  --fill: var(--plain-fill);
  --text: var(--ink);
}

.band.is-done,
.top-step.is-done {
  --color: var(--done);
  --fill: var(--done-fill);
  --text: var(--ink);
}

.band.is-running,
.top-step.is-running {
  --color: var(--running);
  --fill: var(--running-fill);
  --text: var(--ink);
}

.band.is-failed,
.top-step.is-failed {
  --color: var(--failed);
  --fill: var(--failed-fill);
  --text: var(--ink);
}

.band polygon,
.top-step rect {
  fill: var(--fill);
  stroke: var(--color);
  stroke-width: 2;
  stroke-linejoin: round;
  transition:
    fill 0.25s ease,
    stroke 0.25s ease;
}

.band text,
.top-step text {
  fill: var(--text);
  font-family: var(--slidev-code-font-family, ui-monospace, monospace);
  font-size: 20px;
  text-anchor: middle;
  dominant-baseline: central;
  transition: fill 0.25s ease;
}

.band.is-interactive,
.top-step.is-interactive {
  cursor: pointer;
  user-select: none;
}

.band.is-running polygon,
.top-step.is-running rect {
  animation: pyramid-pulse 1.6s ease-in-out infinite;
}

.pyramid.no-animate .band polygon,
.pyramid.no-animate .top-step rect {
  animation: none;
}

.arrow-line {
  stroke: var(--color);
  stroke-width: 2.5;
}

.arrow-head {
  fill: var(--color);
}

/* 左の軸 */
.axis line {
  stroke: #b6b5bd;
  stroke-width: 2;
}

.axis polygon {
  fill: #b6b5bd;
}

.axis-label {
  fill: #6b6a73;
  font-size: 15px;
  text-anchor: middle;
}

@keyframes pyramid-pulse {
  50% {
    opacity: 0.62;
  }
}
</style>
