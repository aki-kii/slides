<template>
  <span class="kogoe"><slot /></span>
</template>

<style scoped>
/* デザインシステムの小声: 補足の下限 18px、コントラスト 4.5:1 以上（#6b7684 で 4.6:1） */
.kogoe {
  font-size: max(0.75em, 0.9rem);
  color: var(--ink-note, #6b7684);
}
</style>
