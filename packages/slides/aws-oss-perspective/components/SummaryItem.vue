<script setup lang="ts">
defineProps<{
  num: string
  sub?: string
}>()
</script>

<template>
  <li class="summary-item">
    <span class="num">{{ num }}</span>
    <span class="body">
      <span class="content"><slot /></span>
      <span v-if="sub" class="sub">{{ sub }}</span>
    </span>
  </li>
</template>

<style scoped>
.summary-item {
  display: grid;
  grid-template-columns: 52px 1fr;
  column-gap: 1rem;
  padding: 0.65rem 0;
  border-top: 1px solid var(--line);
  font-size: 1.1rem;
  line-height: 1.4;
  list-style: none;
}

.summary-item:last-child {
  border-bottom: 1px solid var(--line);
}

.num {
  font-family: 'Inter', sans-serif;
  font-weight: 200;
  font-size: 1.5rem;
  color: var(--brand);
  line-height: 1;
  align-self: baseline;
}

.body {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  color: var(--ink);
}

.sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  color: var(--ink-mute);
  letter-spacing: 0.04em;
}
</style>
