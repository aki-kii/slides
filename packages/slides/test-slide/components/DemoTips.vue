<template>
  <span>💡 {{ steps[Math.min(clicks, steps.length - 1)].tips }}</span>
</template>

<script setup lang="ts">
import { useNav } from '@slidev/client';

const { clicks } = useNav();

defineProps<{
  steps: { label: string; tips: string }[]
}>();
</script>
