<script setup>
import QrCode from '../components/QrCode.vue';

defineProps({
  qrUrl: {
    type: String,
    default: null,
  },
  qrLabel: {
    type: String,
    default: null,
  },
  qrSize: {
    type: Number,
    default: 120,
  },
});
</script>

<template>
  <div class="demo-layout">
    <div class="main-area">
      <div class="screen-area">
        <slot name="screen" />
      </div>
      <div class="notes-area">
        <slot name="notes" />
      </div>
    </div>
    <div class="tips-area">
      <slot name="tips" />
    </div>
    <a v-if="qrUrl" class="qr-corner" :href="qrUrl" target="_blank" rel="noopener noreferrer">
      <p v-if="qrLabel" class="qr-label">{{ qrLabel }}</p>
      <QrCode :url="qrUrl" :size="qrSize" />
    </a>
  </div>
</template>

<style scoped>
.demo-layout {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  color: #1e293b;
  overflow: hidden;
}

.main-area {
  flex: 1;
  display: flex;
  min-height: 0;
}

.screen-area {
  flex: 1;
  min-width: 0;
  padding: 10px 8px 10px 12px;
  display: flex;
  flex-direction: column;
}

.notes-area {
  width: 30%;
  flex-shrink: 0;
  padding: 12px 12px 8px 8px;
  border-left: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.tips-area {
  flex-shrink: 0;
  padding: 8px 20px;
  background: #f8fafc;
  border-top: 3px solid #3b82f6;
  font-size: 1rem;
  color: #475569;
  font-family: 'Yomogi', sans-serif;
  display: flex;
  align-items: center;
  min-height: 56px;
}

.qr-corner {
  position: absolute;
  bottom: 70px;
  right: 16px;
  cursor: pointer;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  background: rgba(248, 250, 252, 0.9);
  backdrop-filter: blur(8px);
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.qr-label {
  margin: 0;
  font-size: 0.75rem;
  color: #64748b;
  text-align: center;
  white-space: pre-line;
}
</style>
