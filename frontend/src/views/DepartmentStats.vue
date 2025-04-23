<template>
  <div class="department-stats">
    <div class="page-header">
      <h2>科室统计</h2>
    </div>
    
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="科室">
          <el-select v-model="searchForm.DepartmentID" placeholder="请选择科室" clearable>
            <el-option
              v-for="dept in departmentList"
              :key="dept.DepartmentID"
              :label="dept.DepartmentName"
              :value="dept.DepartmentID"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="统计时间">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-row :gutter="20" class="stats-cards">
      <el-col :span="8">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>就诊人次</span>
            </div>
          </template>
          <div class="card-content">
            <div class="number">{{ stats.visitCount || 0 }}</div>
            <div class="trend" :class="stats.visitTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.visitTrend) }}%
            </div>
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
            <div class="number">{{ stats.admissionCount || 0 }}</div>
            <div class="trend" :class="stats.admissionTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.admissionTrend) }}%
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>平均住院天数</span>
            </div>
          </template>
          <div class="card-content">
            <div class="number">{{ stats.avgStayDays || 0 }}</div>
            <div class="trend" :class="stats.stayDaysTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.stayDaysTrend) }}%
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card class="chart-card">
      <template #header>
        <div class="card-header">
          <span>就诊趋势</span>
        </div>
      </template>
      <div class="chart-container">
        <div ref="visitChart" style="width: 100%; height: 400px;"></div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { getDepartmentList } from '@/api/department'

const searchForm = reactive({
  DepartmentID: '',
  dateRange: []
})

const departmentList = ref([])
const stats = reactive({
  visitCount: 0,
  visitTrend: 0,
  admissionCount: 0,
  admissionTrend: 0,
  avgStayDays: 0,
  stayDaysTrend: 0
})

let visitChart = null

// 获取科室列表
const fetchDepartmentList = async () => {
  try {
    const res = await getDepartmentList()
    departmentList.value = res.data.list || res.data
  } catch (error) {
    console.error('获取科室列表失败:', error)
    ElMessage.error('获取科室列表失败')
  }
}

// 获取统计数据
const fetchStats = async () => {
  try {
    const params = {
      id: searchForm.DepartmentID,
      startDate: searchForm.dateRange?.[0],
      endDate: searchForm.dateRange?.[1]
    }
    // 暂时使用模拟数据
    const mockData = {
      visitCount: 1200,
      visitTrend: 5,
      admissionCount: 300,
      admissionTrend: 3,
      avgStayDays: 7,
      stayDaysTrend: -2,
      visitTrendData: [
        { date: '2024-01', visitCount: 350, admissionCount: 90 },
        { date: '2024-02', visitCount: 420, admissionCount: 110 },
        { date: '2024-03', visitCount: 430, admissionCount: 100 }
      ]
    }
    Object.assign(stats, mockData)
    initVisitChart(mockData.visitTrendData)
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  }
}

// 初始化就诊趋势图表
const initVisitChart = (data) => {
  if (!visitChart) {
    visitChart = echarts.init(document.querySelector('.chart-container .chart'))
  }
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['就诊人次', '住院人次']
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.date)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '就诊人次',
        type: 'line',
        data: data.map(item => item.visitCount)
      },
      {
        name: '住院人次',
        type: 'line',
        data: data.map(item => item.admissionCount)
      }
    ]
  }
  
  visitChart.setOption(option)
}

// 搜索
const handleSearch = () => {
  fetchStats()
}

// 组件挂载时获取数据
onMounted(() => {
  fetchDepartmentList()
  fetchStats()
  
  // 监听窗口大小变化，调整图表大小
  window.addEventListener('resize', () => {
    visitChart?.resize()
  })
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