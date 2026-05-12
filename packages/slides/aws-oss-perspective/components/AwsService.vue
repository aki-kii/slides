<script setup lang="ts">
defineProps<{
  icon: string
  name: string
}>()
</script>

<template>
  <span class="aws-service">
    <img :src="icon" class="aws-service-icon" />
    <span class="aws-service-name">{{ name }}</span>
  </span>
</template>

<style scoped>
.aws-service {
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  white-space: nowrap;
}

.aws-service-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  object-fit: contain;
}

.aws-service-name {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--ink);
}
</style>
