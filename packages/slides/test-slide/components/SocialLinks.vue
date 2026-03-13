<script setup lang="ts">
defineProps({
  links: {
    type: Array as () => { icon?: string; label: string; url: string }[],
    default: () => [],
  },
});

const builtinIcons: Record<string, string> = {
  x: 'i-carbon-logo-x',
  github: 'i-carbon-logo-github',
};
</script>

<template>
  <div class="flex flex-col items-start gap-2">
    <a
      v-for="link in links"
      :key="link.url"
      :href="link.url"
      target="_blank"
      class="flex items-center gap-1.5 text-sm opacity-70 hover:opacity-100 transition-opacity !border-none"
    >
      <!-- ビルトインアイコン (carbon) -->
      <div
        v-if="link.icon && builtinIcons[link.icon]"
        :class="builtinIcons[link.icon]"
        class="text-lg"
      />
      <!-- カスタム画像アイコン -->
      <img v-else-if="link.icon" :src="link.icon" class="h-4" />
      <span>{{ link.label }}</span>
    </a>
  </div>
</template>
