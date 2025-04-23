<template>
  <div class="not-found">
    <h1>404</h1>
    <h2>页面未找到</h2>
    <p>抱歉，您访问的页面不存在</p>
    <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
  </div>
</template>

<script setup>
// NotFound.vue
</script>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
}

h1 {
  font-size: 120px;
  margin: 0;
  color: #409EFF;
}

h2 {
  font-size: 30px;
  margin: 20px 0;
}

p {
  color: #909399;
  margin-bottom: 30px;
}
</style> 