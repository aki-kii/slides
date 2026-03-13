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
  </div>
</template>

<style scoped>
.demo-layout {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  background: #0f172a;
  color: #f1f5f9;
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
  border-left: 1px solid #1e293b;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.tips-area {
  flex-shrink: 0;
  padding: 12px 20px;
  background: #1e293b;
  border-top: 3px solid #3b82f6;
  font-size: 1rem;
  color: #cbd5e1;
}
</style>
