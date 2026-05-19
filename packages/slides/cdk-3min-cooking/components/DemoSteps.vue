<template>
  <div class="steps-panel">
    <ul :class="['list', clicks > 0 ? 'has-active' : '']">
      <li
        v-for="(step, i) in steps"
        v-show="i >= clicks - 1"
        :key="i"
        :class="[
          'step',
          i < clicks - 1 ? 'done' : i === clicks - 1 ? 'current' : 'upcoming',
        ]"
      >
        <div class="step-row">
          <span class="icon">
            <span v-if="i < clicks - 1">✓</span>
            <span v-else-if="i === clicks - 1">▶</span>
            <span v-else>{{ i + 1 }}</span>
          </span>
          <span>{{ step.label }}</span>
        </div>
        <p v-if="i === clicks - 1 && step.desc" class="step-desc">{{ step.desc }}</p>
        <div v-if="i === clicks - 1 && step.code" class="code-block">
          <button class="copy-btn" @click="copy(toText(step.code))">
            {{ copied ? '✓ Copied' : 'Copy' }}
          </button>
          <pre><code>{{ toText(step.code) }}</code></pre>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useNav } from '@slidev/client';

const { clicks } = useNav();

const props = defineProps<{
  steps: { label: string; tips: string; desc?: string; code?: string | string[] }[];
}>();

const currentStep = computed(
  () => props.steps[Math.min(clicks.value, props.steps.length - 1)],
);

function toText(code: string | string[] | undefined): string {
  if (!code) return '';
  return Array.isArray(code) ? code.join('\n') : code;
}

const copied = ref(false);
async function copy(code: string) {
  if (!code) return;
  await navigator.clipboard.writeText(code);
  copied.value = true;
  setTimeout(() => {
    copied.value = false;
  }, 2000);
}
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
  color: #f1f5f9;
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
  flex-direction: column;
  gap: 6px;
  padding: 6px 8px;
  border-radius: 6px;
  font-size: 0.8rem;
  transition: all 0.25s;
}

.step-row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.step.done {
  color: #cbd5e1;
}
.step.current {
  background: #dbeafe;
  color: #1d4ed8;
  font-weight: 600;
}
.step.upcoming {
  color: #1e293b;
}

.has-active .step.upcoming {
  color: #94a3b8;
}

.icon {
  flex-shrink: 0;
  width: 1.2em;
  text-align: center;
}

.step.done .icon {
  color: #16a34a;
}
.step.current .icon {
  color: #2563eb;
}

.step-desc {
  margin: 0;
  font-size: 0.75rem;
  color: #64748b;
  line-height: 1.5;
  font-weight: 400;
}

.code-block {
  position: relative;
  margin-top: 8px;
  background: #0d1117;
  border: 1px solid #1e293b;
  border-radius: 6px;
  overflow: hidden;
}

.code-block pre {
  margin: 0;
  padding: 10px 12px;
  font-size: 0.72rem;
  line-height: 1.5;
  overflow-x: auto;
  color: #e2e8f0;
}

.code-block code {
  font-family: 'Fira Code', 'Cascadia Code', monospace;
}

.copy-btn {
  position: absolute;
  top: 6px;
  right: 6px;
  background: #3b82f6;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 0.68rem;
  cursor: pointer;
  transition: all 0.2s;
}

.copy-btn:hover {
  background: #2563eb;
  color: #ffffff;
}
</style>
