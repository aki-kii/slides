<template>
  <p class="slide-desc"><slot /></p>
</template>

<style scoped>
.slide-desc {
  font-size: 1.1rem;
  color: var(--ink-soft);
  line-height: 1.8;
  margin: -0.5rem 0 1rem;
}

.slide-desc :deep(ul) {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin: 0;
  padding-left: 1.5rem;
}
</style>
