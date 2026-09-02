<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  repo: {
    type: String,
    required: true,
  },
  width: {
    type: String,
    default: '480px',
  },
});

const ogImageUrl = computed(() => {
  return `https://opengraph.githubassets.com/1/${props.repo}`;
});
</script>

<template>
  <a
    :href="`https://github.com/${repo}`"
    target="_blank"
    class="!border-none !no-underline inline-block"
  >
    <img
      :src="ogImageUrl"
      :alt="repo"
      class="rounded-lg shadow-lg"
      :style="{ width: width }"
    />
  </a>
</template>
