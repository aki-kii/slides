<script setup>
import { onMounted, ref, watch } from 'vue';
import QRCode from 'qrcode';

const props = defineProps({
  url: {
    type: String,
    required: true,
  },
  size: {
    type: Number,
    default: 200,
  },
});

const canvas = ref(null);

const generate = async () => {
  if (canvas.value) {
    await QRCode.toCanvas(canvas.value, props.url, {
      width: props.size,
      margin: 2,
    });
  }
};

onMounted(generate);
watch(() => props.url, generate);
watch(() => props.size, generate);
</script>

<template>
  <canvas ref="canvas" />
</template>
