<template>
  <div class="department-stats">
    <div class="page-header">
      <h2>科室统计</h2>
    </div>
    
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="科室">
          <el-select
            v-model="searchForm.DeptID"
            placeholder="请选择科室"
            filterable
            clearable
            style="width: 200px"
            @change="handleDepartmentChange"
          >
            <el-option
              v-for="dept in departmentList"
              :key="dept.DeptID"
              :label="dept.DeptName"
              :value="dept.DeptID"
            >
              <span>{{ dept.DeptName }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
      </el-form>
      <div v-if="currentDepartment" class="department-info">
        当前选择：{{ currentDepartment }}
      </div>
    </el-card>
    
    <el-row :gutter="20" class="stats-cards">
      <el-col :span="8">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>门诊人次</span>
            </div>
          </template>
          <div class="card-content">
            <div class="number">{{ stats.outpatientCount || 0 }}</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>住院人次</span>
            </div>
          </template>
          <div class="card-content">
            <div class="number">{{ stats.inpatientCount || 0 }}</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>总收入</span>
            </div>
          </template>
          <div class="card-content">
            <div class="number">¥{{ stats.totalRevenue || 0 }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getDepartmentList, getDepartmentDetail } from '@/api/department'
import { getDepartmentStats } from '@/api/report'

const searchForm = reactive({
  DeptID: ''
})

const departmentList = ref([])
const currentDepartment = ref('')
const stats = reactive({
  outpatientCount: 0,
  inpatientCount: 0,
  totalRevenue: 0
})

// 获取科室列表
const fetchDepartmentList = async () => {
  try {
    const res = await getDepartmentList()
    departmentList.value = res.data.list || []
  } catch (error) {
    console.error('获取科室列表失败:', error)
    ElMessage.error('获取科室列表失败')
  }
}

// 获取科室详情
const fetchDepartmentDetail = async (id) => {
  try {
    const res = await getDepartmentDetail(id)
    if (res.data) {
      currentDepartment.value = res.data.DeptName
    }
  } catch (error) {
    console.error('获取科室详情失败:', error)
    ElMessage.error('获取科室详情失败')
  }
}

// 处理科室选择变化
const handleDepartmentChange = async (value) => {
  if (value) {
    await fetchDepartmentDetail(value)
  } else {
    currentDepartment.value = ''
  }
  fetchStats()
}

// 获取统计数据
const fetchStats = async () => {
  try {
    if (searchForm.DeptID) {
      const res = await getDepartmentStats(searchForm.DeptID)
      if (res.data && res.data.length > 0) {
        const deptStats = res.data[0]
        stats.outpatientCount = deptStats.outpatientCount || 0
        stats.inpatientCount = deptStats.inpatientCount || 0
        stats.totalRevenue = deptStats.totalRevenue || 0
      }
    } else {
      // 如果没有选择科室，显示所有科室的汇总数据
      const allDepts = departmentList.value
      const allStats = await Promise.all(
        allDepts.map(dept => getDepartmentStats(dept.DeptID))
      )
      
      // 汇总所有科室的数据
      const totalStats = allStats.reduce((acc, curr) => {
        if (curr.data && curr.data.length > 0) {
          const deptStats = curr.data[0]
          acc.outpatientCount += deptStats.outpatientCount || 0
          acc.inpatientCount += deptStats.inpatientCount || 0
          acc.totalRevenue += deptStats.totalRevenue || 0
        }
        return acc
      }, {
        outpatientCount: 0,
        inpatientCount: 0,
        totalRevenue: 0
      })
      
      Object.assign(stats, totalStats)
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  }
}

// 搜索
const handleSearch = () => {
  fetchStats()
}

// 组件挂载时获取数据
onMounted(() => {
  fetchDepartmentList()
  fetchStats()
})
</script>

<style scoped>
.department-stats {
  width: 100%;
}

.page-header {
  margin-bottom: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.department-info {
  margin-top: 10px;
  font-size: 14px;
  color: #606266;
}

.stats-cards {
  margin-bottom: 20px;
}

.stats-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  text-align: center;
}

.number {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.trend {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.trend.up {
  color: #67c23a;
}

.trend.down {
  color: #f56c6c;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-container {
  width: 100%;
  height: 400px;
}
</style> 