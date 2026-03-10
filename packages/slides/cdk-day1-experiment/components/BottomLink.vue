<script setup>
import { inject } from 'vue'

defineProps({
  href: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    default: null,
  },
  title: {
    type: String,
    default: null,
  },
});

const insideBottomLinks = inject('insideBottomLinks', false)
</script>

<template>
  <div :class="['bottom-link-wrapper', { standalone: !insideBottomLinks }]">
    <span v-if="title" class="bottom-link-title">{{ title }}</span>
    <a :href="href" target="_blank" rel="noopener noreferrer" class="bottom-link">
      {{ label ?? href }}
    </a>
  </div>
</template>

<style scoped>
.bottom-link-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.15rem;
  white-space: nowrap;
}

.bottom-link-wrapper.standalone {
  position: absolute;
  bottom: 0.85rem;
  left: 1.5rem;
  z-index: 100;
}

.bottom-link-title {
  font-size: 0.6rem;
  color: rgba(120, 120, 120, 0.7);
  line-height: 1;
}

.bottom-link {
  font-size: 0.7rem;
  color: deepskyblue;
  text-decoration: none;
  line-height: 1;
  white-space: nowrap;
}

.bottom-link:hover {
  color: rgba(80, 80, 80, 0.9);
  text-decoration: underline;
}
</style>
