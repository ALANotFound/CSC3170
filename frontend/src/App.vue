<script setup>
// App.vue
</script>

<template>
  <router-view />
</template>

<style>
/* 重置所有元素的默认样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100vh;
  width: 100%;
  font-family: Arial, Helvetica, sans-serif;
  overflow-x: hidden; /* 只隐藏横向滚动条 */
}

body {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

#app {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
</style>
