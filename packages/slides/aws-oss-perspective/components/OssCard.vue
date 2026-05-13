<script setup lang="ts">
defineProps<{
  color: string
  icon: string
  iconUrl?: string
  isAws?: boolean
  name: string
  desc: string
  dense?: boolean
}>()
</script>

<template>
  <div class="oss-card" :class="{ dense }">
    <span class="badge" :class="{ aws: isAws }">{{ isAws ? 'AWS OSS' : 'Community OSS' }}</span>
    <div class="card-head">
      <div class="svc-icon" :class="{ dense, 'has-image': iconUrl }" :style="iconUrl ? {} : { background: color }">
        <img v-if="iconUrl" :src="iconUrl" class="icon-img" />
        <template v-else>{{ icon }}</template>
      </div>
      <h4>{{ name }}</h4>
    </div>
    <p class="desc">{{ desc }}</p>
    <div v-if="$slots.arrow" class="arrow-row">
      <span class="svc"><slot name="arrow" /></span>
    </div>
  </div>
</template>

<style scoped>
.oss-card {
  background: white;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 0.7rem 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 1rem;
  min-width: 0;
  box-sizing: border-box;
}

.oss-card.dense {
  padding: 0.55rem 0.75rem;
  gap: 0.15rem;
  border-radius: 10px;
}

.card-head {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.svc-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-family: 'Inter', 'Noto Sans JP', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: -0.02em;
  flex-shrink: 0;
}

.svc-icon.has-image {
  border: 1px solid var(--line);
  background: white !important;
  padding: 3px;
}

.icon-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.svc-icon.dense {
  width: 30px;
  height: 30px;
  font-size: 0.8rem;
  border-radius: 6px;
}

.badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  color: var(--brand);
  font-weight: 600;
  letter-spacing: 0.06em;
}

.badge.aws {
  color: var(--accent-warm);
}

h4 {
  font-size: 0.88rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
  color: var(--ink);
}

.oss-card.dense h4 {
  font-size: 0.82rem;
}

.desc {
  font-size: 0.78rem;
  color: var(--ink-soft);
  line-height: 1.4;
  margin: 0;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.arrow-row {
  margin-top: 0.35rem;
  padding-top: 0.35rem;
  border-top: 1px solid var(--line);
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.3rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--brand-deep);
  font-weight: 600;
}

.svc {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  flex-wrap: wrap;
  color: var(--ink);
}
</style>
