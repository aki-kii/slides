<script setup lang="ts">
import { ref, watch } from 'vue'
import { useIsSlideActive } from '@slidev/client'

const props = defineProps<{ url: string }>()

const isActive = useIsSlideActive()
const src = ref('')

watch(isActive, (active) => {
  if (active) {
    src.value = props.url
  } else {
    src.value = ''
  }
}, { immediate: true })
</script>

<template>
  <iframe
    v-if="src"
    :src="src"
    style="position: absolute; inset: 0; width: 100%; height: 100%; border: none;"
    allow="fullscreen"
  />
</template>
