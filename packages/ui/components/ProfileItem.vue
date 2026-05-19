<script setup lang="ts">
defineProps({
  title: {
    type: String,
    default: '',
  },
  icon: {
    type: String,
    default: '',
  },
  name: {
    type: String,
    required: true,
  },
  titleSize: {
    type: String,
    default: 'text-sm',
  },
  nameSize: {
    type: String,
    default: 'text-xl',
  },
  gap: {
    type: String,
    default: 'gap-2',
  },
});
</script>

<template>
  <div>
    <div :class="['flex flex-col', gap]">
      <span v-if="title" :class="[titleSize, 'text-gray-400']">{{
        title
      }}</span>
      <div :class="['flex items-center gap-2 font-bold', nameSize]">
        <img v-if="icon" :src="icon" class="h-6" />
        <span>{{ name }}</span>
      </div>
    </div>
    <div v-if="$slots.default" class="mt-1 text-base text-gray-300 pl-4">
      <slot />
    </div>
  </div>
</template>
