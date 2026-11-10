<script setup>
/**
 * 前置き (小) → 言い切り (大) → 補足 (小) の 1 かたまり。StatementList の中に置く。
 *
 *   <Statement note="しかし" lead="コードの正しさを自身で判断できない" />
 *
 * 言い切りに <strong> などを入れたいときは、lead の代わりに既定スロットへ書く。
 *
 *   <Statement :notes="['走りながら音声入力で指示しています！']">
 *     <strong>走りながらコーディングエージェントを動かしている</strong>ので暇じゃなくなったから
 *   </Statement>
 *
 * v-click はそのまま付けられる (root の div に効く)。
 */
defineProps({
  /** 言い切りの前に置く前置き。1 行だけ */
  note: { type: String, default: '' },
  /** 言い切りの一行。マークアップが要るなら既定スロットを使う */
  lead: { type: String, default: '' },
  /** 言い切りの後ろに置く補足。行ごとに配列で渡す */
  notes: { type: Array, default: () => [] },
  /** 言い切りの文字サイズ。'md' は 1 行が長いページ用に一段落とす */
  leadSize: {
    type: String,
    default: 'lg',
    validator: (value) => ['lg', 'md'].includes(value),
  },
});
</script>

<template>
  <div class="intro-block">
    <div v-if="note" class="intro-note">{{ note }}</div>

    <div
      class="intro-lead"
      :class="{ 'intro-lead--md': leadSize === 'md' }"
    >
      <slot>{{ lead }}</slot>
    </div>

    <div v-for="(line, index) in notes" :key="index" class="intro-note">
      {{ line }}
    </div>
  </div>
</template>
