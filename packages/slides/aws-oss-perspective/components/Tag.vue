<template>
  <span class="tag"><slot /></span>
</template>

<style scoped>
.tag {
  border: 1.5px solid var(--line);
  border-radius: 999px;
  padding: 0.25rem 0.7rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--ink);
  white-space: nowrap;
  animation: tag-appear 0.2s ease both;
}

@keyframes tag-appear {
  from { opacity: 0; transform: scale(0.75); }
  to   { opacity: 1; transform: scale(1); }
}
</style>
