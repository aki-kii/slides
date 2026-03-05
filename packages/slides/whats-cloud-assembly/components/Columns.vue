<script setup>
const props = defineProps({
  ratio: {
    type: String,
    default: '1:1' // '1:1', '2:1', '3:1', '1:2' など
  }
})

const ratioMap = {
  '1:1': 'grid-cols-2',
  '2:1': 'grid-cols-[2fr_1fr]',
  '1:2': 'grid-cols-[1fr_2fr]',
  '3:1': 'grid-cols-[3fr_1fr]',
  '1:3': 'grid-cols-[1fr_3fr]',
}

const gridClass = ratioMap[props.ratio] || 'grid-cols-2'
</script>

<template>
  <div :class="['grid gap-6 items-start', gridClass]">
    <div>
      <slot name="left" />
    </div>
    <div>
      <slot name="right" />
    </div>
  </div>
</template>