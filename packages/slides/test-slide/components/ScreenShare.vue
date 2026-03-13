<template>
  <div class="screen-share-wrapper">
    <div class="screen-share-frame">
      <video v-show="isSharing" ref="videoEl" autoplay playsinline class="screen-share-video" />
      <div v-if="!isSharing" class="placeholder">
        <button class="start-button" @click="startShare">デモを開始</button>
      </div>
      <button v-if="isSharing" class="stop-button" @click="stopShare">✕ 停止</button>
      <div class="stopwatch-overlay">
        <Stopwatch ref="stopwatchRef" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue';

const videoEl = ref<HTMLVideoElement | null>(null);
const stopwatchRef = ref<InstanceType<typeof import('./Stopwatch.vue').default> | null>(null);
const isSharing = ref(false);
let stream: MediaStream | null = null;

async function startShare() {
  try {
    stream = await navigator.mediaDevices.getDisplayMedia({
      video: true,
      audio: false,
    });
    isSharing.value = true;

    await new Promise<void>((resolve) => {
      const check = setInterval(() => {
        if (videoEl.value) {
          clearInterval(check);
          resolve();
        }
      }, 50);
    });

    if (videoEl.value) {
      videoEl.value.srcObject = stream;
    }

    stopwatchRef.value?.start();

    stream.getVideoTracks()[0].addEventListener('ended', () => {
      stopShare();
    });
  } catch (e) {
    console.error('画面共有の開始に失敗しました:', e);
  }
}

function stopShare() {
  stream?.getTracks().forEach((t) => t.stop());
  stream = null;
  isSharing.value = false;
  stopwatchRef.value?.stop();
}

onUnmounted(() => {
  stopShare();
});
</script>

<style scoped>
.screen-share-wrapper {
  display: flex;
  align-items: stretch;
  justify-content: stretch;
  width: 100%;
  height: 100%;
}

.screen-share-frame {
  position: relative;
  width: 100%;
  height: 100%;
  border: 3px solid #22c55e;
  border-radius: 12px;
  overflow: hidden;
  background: #0f172a;
  box-shadow:
    0 0 0 1px #16a34a,
    0 8px 32px rgba(34, 197, 94, 0.2);
}

.placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.screen-share-video {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.start-button {
  padding: 14px 36px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background 0.2s;
}

.start-button:hover {
  background: #2563eb;
}

.stop-button {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 12px;
  background: rgba(239, 68, 68, 0.85);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background 0.2s;
}

.stop-button:hover {
  background: rgba(220, 38, 38, 0.95);
}

.stopwatch-overlay {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(4px);
  border-radius: 8px;
  padding: 4px 10px;
}
</style>
