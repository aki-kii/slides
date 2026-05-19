<template>
  <strong class="hl"><slot /></strong>
</template>

<style scoped>
.hl {
  background: var(--brand-tint);
  color: var(--brand-deep);
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 700;
}
</style>
