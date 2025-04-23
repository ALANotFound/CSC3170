<template>
  <div class="hospital-app">
    <el-container>
      <el-aside width="240px" class="aside">
        <div class="logo">医院管理系统</div>
        <el-menu
          router
          :default-active="activeMenu"
          class="menu"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/dashboard">
            <el-icon><el-icon-monitor /></el-icon>
            <span>首页</span>
          </el-menu-item>
          
          <el-sub-menu index="/patients">
            <template #title>
              <el-icon><el-icon-user /></el-icon>
              <span>患者管理</span>
            </template>
            <el-menu-item index="/patients">患者列表</el-menu-item>
            <el-menu-item index="/patients/add">新增患者</el-menu-item>
          </el-sub-menu>
          
          <el-sub-menu index="/doctors">
            <template #title>
              <el-icon><el-icon-user-filled /></el-icon>
              <span>医师管理</span>
            </template>
            <el-menu-item index="/doctors">医师列表</el-menu-item>
            <el-menu-item index="/doctors/add">新增医师</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/departments">
            <template #title>
              <el-icon><el-icon-user-filled /></el-icon>
              <span>科室管理</span>
            </template>
            <el-menu-item index="/departments">医师列表</el-menu-item>
            <el-menu-item index="/departments/add">新增医师</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/wards">
            <template #title>
              <el-icon><el-icon-user-filled /></el-icon>
              <span>病房管理</span>
            </template>
            <el-menu-item index="/wards">医师列表</el-menu-item>
            <el-menu-item index="/wards/add">新增医师</el-menu-item>
          </el-sub-menu>
          
          <el-sub-menu index="/visits">
            <template #title>
              <el-icon><el-icon-document /></el-icon>
              <span>就诊记录</span>
            </template>
            <el-menu-item index="/visits">记录列表</el-menu-item>
            <el-menu-item index="/visits/add">新增记录</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/admissions">
            <template #title>
              <el-icon><el-icon-hospital /></el-icon>
              <span>住院记录</span>
            </template>
            <el-menu-item index="/admissions">在院患者</el-menu-item>
            <el-menu-item index="/admissions/add">办理入院</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/statistics">
            <template #title>
              <el-icon><el-icon-data-analysis /></el-icon>
              <span>统计分析</span>
            </template>
            <el-menu-item index="/statistics/department">科室统计</el-menu-item>
            <el-menu-item index="/statistics/revenue">流水统计</el-menu-item>
            <el-menu-item index="/statistics/doctor">医师工作量</el-menu-item>
          </el-sub-menu>
    
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header height="60px" class="header">
          <div class="header-left">
            <el-icon class="toggle-icon" @click="toggleSidebar"><el-icon-fold /></el-icon>
          </div>
          <div class="header-right">
            <el-dropdown>
              <span class="user-info">
                管理员 <el-icon><el-icon-arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>个人中心</el-dropdown-item>
                  <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <el-main class="main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const activeMenu = computed(() => {
  return route.path
})

const logout = () => {
  // 清除登录信息
  localStorage.removeItem('token')
  // 跳转到登录页
  router.push('/login')
}

const toggleSidebar = () => {
  // 侧边栏收缩功能可在这里实现
}
</script>

<style scoped>
.hospital-app {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.el-container {
  height: 100%;
  width: 100%;
}

.aside {
  background-color: #304156;
  height: 100%;
  overflow: hidden;
}

.logo {
  color: #fff;
  font-size: 20px;
  font-weight: bold;
  height: 60px;
  line-height: 60px;
  text-align: center;
}

.menu {
  height: calc(100% - 60px);
  border-right: none;
}

.header {
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #dcdfe6;
  padding: 0 20px;
}

.header-left, .header-right {
  display: flex;
  align-items: center;
}

.toggle-icon {
  font-size: 20px;
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.main {
  background-color: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
  flex: 1;
  height: calc(100% - 60px);
}
</style> 