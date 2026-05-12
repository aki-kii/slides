<script setup lang="ts">
defineProps<{
  tag: string
  title: string
  featured?: boolean
}>()
</script>

<template>
  <div class="pillar" :class="{ featured }">
    <span class="tag">{{ tag }}</span>
    <h3 v-html="title" />
    <p><slot /></p>
  </div>
</template>

<style scoped>
.pillar {
  background: white;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 1.3rem 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  height: 100%;
  box-sizing: border-box;
}

.pillar.featured {
  background: var(--brand);
  border-color: var(--brand);
}

.tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: var(--brand);
  font-weight: 600;
  letter-spacing: 0.14em;
}

.pillar.featured .tag {
  color: rgba(255, 255, 255, 0.8);
}

h3 {
  font-size: 1.3rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.25;
  color: var(--ink);
}

.pillar.featured h3 {
  color: white;
}

p {
  font-size: 0.9rem;
  color: var(--ink-soft);
  line-height: 1.6;
  margin: 0;
}

.pillar.featured p {
  color: rgba(255, 255, 255, 0.92);
}
</style>
