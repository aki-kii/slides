<template>
  <div class="stopwatch">
    <span class="stopwatch-time">{{ formattedTime }}</span>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue';

const elapsed = ref(0);
const isRunning = ref(false);
let intervalId: ReturnType<typeof setInterval> | null = null;
let startTime = 0;

const formattedTime = computed(() => {
  const totalSeconds = Math.floor(elapsed.value / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
});

function stop() {
  if (intervalId) { clearInterval(intervalId); intervalId = null; }
  isRunning.value = false;
}

function reset() {
  stop();
  elapsed.value = 0;
}

function start() {
  if (isRunning.value) return;
  startTime = Date.now() - elapsed.value;
  intervalId = setInterval(() => { elapsed.value = Date.now() - startTime; }, 100);
  isRunning.value = true;
}

defineExpose({ start, stop, reset });

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId);
});
</script>

<style scoped>
.stopwatch {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stopwatch-time {
  font-size: 1.8rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: #f1f5f9;
  letter-spacing: 0.05em;
}

</style>
