<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2>医院管理系统</h2>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            prefix-icon="el-icon-user"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            placeholder="密码"
            type="password"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为6位', trigger: 'blur' }
  ]
})

const handleLogin = () => {
  loginFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    
    try {
      // 这里应该调用登录API
      // 模拟登录成功
      setTimeout(() => {
        // 保存token到localStorage
        localStorage.setItem('token', 'mock-token')
        
        ElMessage.success('登录成功')
        // 跳转到首页
        router.push('/')
        
        loading.value = false
      }, 1000)
    } catch (error) {
      console.error('登录失败:', error)
      ElMessage.error('登录失败，请检查用户名和密码')
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}

.login-card {
  width: 400px;
  padding: 40px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  color: #409EFF;
}

.login-form {
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  padding: 12px 15px;
}
</style> 