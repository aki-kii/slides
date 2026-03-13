<template>
  <div class="steps-panel">
    <div class="title">手順</div>
    <ul class="list">
      <li
        v-for="(step, i) in steps"
        :key="i"
        :class="['step', i < clicks ? 'done' : i === clicks ? 'current' : 'upcoming']"
      >
        <span class="icon">
          <span v-if="i < clicks">✓</span>
          <span v-else-if="i === clicks">▶</span>
          <span v-else>{{ i + 1 }}</span>
        </span>
        <span>{{ step.label }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useNav } from '@slidev/client';

const { clicks } = useNav();

defineProps<{
  steps: { label: string; tips: string }[]
}>();
</script>

<style scoped>
.steps-panel {
  display: flex;
  flex-direction: column;
  gap: 8px;
  height: 100%;
}

.title {
  font-size: 0.85rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding-bottom: 6px;
  border-bottom: 1px solid #1e293b;
}

.list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 6px 8px;
  border-radius: 6px;
  font-size: 0.8rem;
  transition: all 0.25s;
}

.step.done    { color: #475569; }
.step.current { background: #1e3a5f; color: #93c5fd; font-weight: 600; }
.step.upcoming { color: #64748b; }

.icon {
  flex-shrink: 0;
  width: 1.2em;
  text-align: center;
}

.step.done .icon    { color: #22c55e; }
.step.current .icon { color: #60a5fa; }
</style>
