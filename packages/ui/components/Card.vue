<script setup lang="ts">
defineProps({
  title: { type: String, default: '' },
  date: { type: String, default: '' },
  variant: {
    type: String,
    default: 'default',
    // 'default' | 'danger' | 'warning' | 'info'
  },
});
</script>

<template>
  <div class="card" :class="`card--${variant}`">
    <div class="card-header">
      <span class="card-title">{{ title }}</span>
      <span v-if="date" class="card-date">{{ date }}</span>
    </div>
    <div class="card-body">
      <slot />
    </div>
  </div>
</template>

