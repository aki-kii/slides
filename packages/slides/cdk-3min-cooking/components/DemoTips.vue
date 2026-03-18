<template>
  <div class="tips-content">
    <img v-if="currentImage" :src="currentImage" class="tips-image" />
    <span>{{ currentTips }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useNav } from '@slidev/client';

const { clicks } = useNav();

const props = defineProps<{
  steps: { label: string; tips: string; image?: string; code?: string | string[] }[];
  initialTips?: string;
  initialImage?: string;
}>();

const currentTips = computed(() =>
  clicks.value === 0
    ? (props.initialTips ?? '')
    : props.steps[Math.min(clicks.value - 1, props.steps.length - 1)].tips
);

const currentImage = computed(() =>
  clicks.value === 0
    ? props.initialImage
    : props.steps[Math.min(clicks.value - 1, props.steps.length - 1)].image
);
</script>

<style scoped>
.tips-content {
  display: flex;
  align-items: center;
  gap: 16px;
  height: 100%;
}

.tips-image {
  max-height: 3rem;
  width: auto;
  object-fit: contain;
  flex-shrink: 0;
}
</style>
