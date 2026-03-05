<script setup>
const props = defineProps({
  clickStart: {
    type: Number,
    required: true
  },
  clickEnd: {
    type: Number,
    required: true
  },
  position: {
    type: [Object, String],
    default: () => ({})
  },
  title: {
    type: String,
    required: true
  },
  maxWidth: {
    type: String,
    default: '22rem'
  }
})

// プリセット位置
const presetPositions = {
  'top-left': { left: '2rem', top: '2rem' },
  'top-right': { right: '2rem', top: '2rem' },
  'bottom-left': { left: '2rem', bottom: '2rem' },
  'bottom-right': { right: '2rem', bottom: '2rem' },
  'center': { left: '50%', top: '50%', transform: 'translate(-50%, -50%)' },
  'center-left': { left: '15rem', top: '5rem' },
  'center-right': { right: '12rem', top: '5rem' }
}

// 位置スタイルを生成
const getPositionStyle = () => {
  const basePosition = typeof props.position === 'string' 
    ? presetPositions[props.position] 
    : props.position

  return {
    position: 'absolute',
    ...basePosition,
    background: 'rgba(0,0,0,0.75)',
    color: 'white',
    padding: '1rem',
    borderRadius: '1rem',
    maxWidth: props.maxWidth,
    zIndex: 100
  }
}
</script>

<template>
  <div v-click.hide="clickEnd">
    <div
      v-click="clickStart"
      :style="getPositionStyle()"
    >
      <div style="font-weight: 600;">{{ title }}</div>
      <div style="font-size: 14px; margin-top: 6px;">
        <slot />
      </div>
    </div>
  </div>
</template>