<script setup lang="ts">
/**
 * Q. と A. の1行。言い切りを既定スロットに、補足を notes に渡す。
 *
 *   <QaItem mark="Q">1つにまとめたらbotの起動が遅くなるのでは？</QaItem>
 *   <QaItem mark="A" :notes="['スナップショットは起動した状態を保持している']">
 *     <strong>スナップショットから起動する</strong>ので素早い
 *   </QaItem>
 *
 * notes は HTML として描くので、<strong> などで強調できる。
 */
defineProps<{
  /** 'Q' か 'A'。A はデッキの strong の色で強調する */
  mark: 'Q' | 'A'
  /** 言い切りの下に置く補足。行ごとに配列で渡す */
  notes?: string[]
}>()
</script>

<template>
  <div class="qa-item">
    <span class="qa-mark"><strong v-if="mark === 'A'">A.</strong><template v-else>Q.</template></span>
    <div>
      <div class="qa-lead"><slot /></div>
      <div v-for="(line, i) in notes ?? []" :key="i" class="qa-note" v-html="line" />
    </div>
  </div>
</template>

<style scoped>
.qa-item {
  display: flex;
  gap: 0.8rem;
  align-items: flex-start;
  margin-top: 0.9rem;
}
.qa-mark {
  font-size: 1.6rem;
  font-weight: bold;
  width: 2.4rem;
  flex: none;
}
.qa-lead {
  font-size: 1.3rem;
  line-height: 1.5;
}
.qa-note {
  font-size: 1.05rem;
  opacity: 0.85;
  line-height: 1.5;
  margin-top: 0.2rem;
}
</style>
