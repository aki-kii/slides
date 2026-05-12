<script setup lang="ts">
defineProps<{
  color: string
  icon: string
  isAws?: boolean
  name: string
  desc: string
  dense?: boolean
}>()
</script>

<template>
  <div class="oss-card" :class="{ dense }">
    <div class="card-head">
      <div class="svc-icon" :class="{ dense }" :style="{ background: color }">{{ icon }}</div>
      <span class="badge" :class="{ aws: isAws }">{{ isAws ? 'AWS OSS' : 'OSS' }}</span>
    </div>
    <h4>{{ name }}</h4>
    <p class="desc">{{ desc }}</p>
    <div v-if="$slots.arrow" class="arrow-row">
      →&nbsp;<span class="svc"><slot name="arrow" /></span>
    </div>
  </div>
</template>

<style scoped>
.oss-card {
  background: white;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 1rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 1rem;
}

.oss-card.dense {
  padding: 0.75rem 0.8rem;
  gap: 0.25rem;
  border-radius: 10px;
}

.card-head {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.svc-icon {
  width: 48px;
  height: 48px;
  border-radius: 9px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-family: 'Inter', 'Noto Sans JP', sans-serif;
  font-weight: 700;
  font-size: 1.2rem;
  letter-spacing: -0.02em;
  flex-shrink: 0;
}

.svc-icon.dense {
  width: 36px;
  height: 36px;
  font-size: 0.9rem;
  border-radius: 7px;
}

.badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: var(--brand);
  font-weight: 600;
  letter-spacing: 0.06em;
}

.badge.aws {
  color: var(--accent-warm);
}

h4 {
  font-size: 1.15rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
  color: var(--ink);
}

.oss-card.dense h4 {
  font-size: 1rem;
}

.desc {
  font-size: 0.85rem;
  color: var(--ink-soft);
  line-height: 1.45;
  margin: 0;
}

.arrow-row {
  margin-top: auto;
  padding-top: 0.5rem;
  border-top: 1px solid var(--line);
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  color: var(--brand-deep);
  font-weight: 600;
}

.svc {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  flex-wrap: wrap;
  color: var(--ink);
}
</style>
