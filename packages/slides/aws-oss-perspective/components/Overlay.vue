<script setup>
const props = defineProps({
  clickStart: {
    type: Number,
  },
  clickEnd: {
    type: Number,
  },
  position: {
    type: [Object, String],
    default: 'center',
  },
  fontSize: {
    type: String,
    default: '1.25rem',
  },
});

const presetPositions = {
  'top-left': { left: '2rem', top: '2rem' },
  'top-right': { right: '2rem', top: '2rem' },
  'bottom-left': { left: '2rem', bottom: '2rem' },
  'bottom-right': { right: '2rem', bottom: '2rem' },
  center: { left: '50%', top: '50%', transform: 'translate(-50%, -50%)' },
  'center-left': { left: '15rem', top: '5rem' },
  'center-right': { right: '12rem', top: '5rem' },
};

const getPositionStyle = () => {
  const basePosition =
    typeof props.position === 'string'
      ? presetPositions[props.position]
      : props.position;

  return {
    position: 'absolute',
    ...basePosition,
    background: 'rgba(180, 180, 180, 0.9)',
    backdropFilter: 'blur(12px)',
    WebkitBackdropFilter: 'blur(12px)',
    color: '#1a1a1a',
    padding: '1rem 3rem',
    borderRadius: '1rem',
    width: 'fit-content',
    whiteSpace: 'nowrap',
    zIndex: 100,
    lineHeight: '2rem',
  };
};
</script>

<template>
  <template v-if="clickEnd !== undefined">
    <div v-click.hide="clickEnd">
      <div v-click="clickStart" :style="getPositionStyle()">
        <slot />
      </div>
    </div>
  </template>
  <template v-else>
    <div v-click="clickStart" :style="getPositionStyle()">
      <slot />
    </div>
  </template>
</template>

<style scoped>
div :deep(*) {
  font-size: v-bind(fontSize) !important;
}
</style>
