<script setup lang="ts">
defineProps<{
  num: string
  title: string
  sub?: string
}>()
</script>

<template>
  <div class="agenda-item">
    <span class="num">{{ num }}</span>
    <div>
      <div class="title">{{ title }}</div>
      <div v-if="sub" class="sub">{{ sub }}</div>
    </div>
  </div>
</template>

<style scoped>
.agenda-item {
  display: grid;
  grid-template-columns: 70px 1fr;
  column-gap: 1.5rem;
  padding: 0.9rem 0;
  border-top: 1px solid var(--line);
  align-items: baseline;
}

.agenda-item:last-child {
  border-bottom: 1px solid var(--line);
}

.num {
  font-family: 'Inter', sans-serif;
  font-weight: 200;
  font-size: 2.5rem;
  color: var(--brand);
  line-height: 1;
}

.title {
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--ink);
  line-height: 1.3;
}

.sub {
  font-size: 0.9rem;
  color: var(--ink-mute);
  margin-top: 0.3rem;
}
</style>
