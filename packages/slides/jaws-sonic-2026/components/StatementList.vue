<script setup>
/**
 * 「小さい前置き → 大きい言い切り」のかたまりを縦に並べる枠。
 *
 *   <StatementList>
 *     <Statement note="CDKはプログラミング言語で書けるので" lead="コーディングエージェントの得意分野！" />
 *     <Statement v-click="1" note="しかし" lead="コードの正しさを自身で判断できない" />
 *   </StatementList>
 *
 * 文字組みは style.css の .intro-* に置いたまま (Q&A や数字の並びなど、
 * 素の HTML で書いている変則ページと同じトークンを共有するため)。
 * ここはそのクラスを貼るだけの薄い入れ物にしている。
 */
defineProps({
  /** かたまり同士の間隔。'wide' は話を切り離したいページ用に一段あける */
  gap: {
    type: String,
    default: 'normal',
    validator: (value) => ['normal', 'wide'].includes(value),
  },
});
</script>

<template>
  <div class="intro-body" :class="{ 'intro-body--wide': gap === 'wide' }">
    <slot />
  </div>
</template>
