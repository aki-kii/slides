<template>
  <ul class="plain-list"><slot /></ul>
</template>

<style scoped>
.plain-list {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.plain-list :deep(li) {
  padding-left: 0;
  margin-left: 0;
}
</style>
