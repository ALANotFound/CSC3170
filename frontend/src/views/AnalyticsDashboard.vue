<template>
  <div class="analytics">
    <div class="page-header">
      <h2>统计分析</h2>
    </div>
    
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            :shortcuts="dateShortcuts"
          />
        </el-form-item>
        <el-form-item label="科室">
          <el-select v-model="filterForm.department" placeholder="选择科室" clearable>
            <el-option label="所有科室" value="" />
            <el-option v-for="dept in departments" :key="dept.id" :label="dept.name" :value="dept.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="applyFilter">应用筛选</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <div class="chart-header">
            <h3>就诊人数趋势</h3>
          </div>
          <div class="chart-container" ref="visitTrendChartRef"></div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="chart-card">
          <div class="chart-header">
            <h3>科室就诊分布</h3>
          </div>
          <div class="chart-container" ref="deptDistributionChartRef"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <div class="chart-header">
            <h3>年龄段分布</h3>
          </div>
          <div class="chart-container" ref="ageDistributionChartRef"></div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="chart-card">
          <div class="chart-header">
            <h3>住院天数分布</h3>
          </div>
          <div class="chart-container" ref="stayDistributionChartRef"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card class="data-card">
      <template #header>
        <div class="card-header">
          <span>数据概览</span>
          <el-button type="primary" size="small" @click="exportData">导出数据</el-button>
        </div>
      </template>
      
      <el-table :data="summaryData" style="width: 100%">
        <el-table-column prop="type" label="类型" width="180" />
        <el-table-column prop="totalCount" label="总数" width="120" />
        <el-table-column prop="avgPerDay" label="日均" width="120" />
        <el-table-column prop="increase" label="增长率">
          <template #default="scope">
            <span :class="scope.row.increase >= 0 ? 'increase-up' : 'increase-down'">
              {{ scope.row.increase >= 0 ? '+' : '' }}{{ scope.row.increase }}%
            </span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
// 假设我们会导入echarts
// import * as echarts from 'echarts'

// 科室列表
const departments = ref([
  { id: 1, name: '内科' },
  { id: 2, name: '外科' },
  { id: 3, name: '儿科' },
  { id: 4, name: '妇科' },
  { id: 5, name: '骨科' }
])

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  },
  {
    text: '最近一个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    }
  },
  {
    text: '最近三个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
      return [start, end]
    }
  }
]

// 筛选表单
const filterForm = reactive({
  dateRange: [new Date(new Date().getTime() - 30 * 24 * 60 * 60 * 1000), new Date()],
  department: ''
})

// 图表引用
const visitTrendChartRef = ref(null)
const deptDistributionChartRef = ref(null)
const ageDistributionChartRef = ref(null)
const stayDistributionChartRef = ref(null)

// 概览数据
const summaryData = ref([
  { type: '门诊量', totalCount: 2456, avgPerDay: 82, increase: 5.2 },
  { type: '住院量', totalCount: 431, avgPerDay: 14, increase: -2.1 },
  { type: '手术量', totalCount: 187, avgPerDay: 6, increase: 8.7 },
  { type: '检查量', totalCount: 3254, avgPerDay: 108, increase: 3.4 }
])

// 应用筛选
const applyFilter = () => {
  // 实际项目中会根据筛选条件获取数据并重新渲染图表
  console.log('应用筛选', filterForm)
}

// 重置筛选
const resetFilter = () => {
  filterForm.dateRange = [new Date(new Date().getTime() - 30 * 24 * 60 * 60 * 1000), new Date()]
  filterForm.department = ''
}

// 导出数据
const exportData = () => {
  // 实际项目中会导出数据到CSV或Excel
  console.log('导出数据')
}

// 初始化图表
const initCharts = () => {
  /* 
  实际项目中会使用echarts创建图表，这里仅作示例
  const visitTrendChart = echarts.init(visitTrendChartRef.value)
  visitTrendChart.setOption({
    // 配置
  })
  
  const deptDistributionChart = echarts.init(deptDistributionChartRef.value)
  deptDistributionChart.setOption({
    // 配置
  })
  
  const ageDistributionChart = echarts.init(ageDistributionChartRef.value)
  ageDistributionChart.setOption({
    // 配置
  })
  
  const stayDistributionChart = echarts.init(stayDistributionChartRef.value)
  stayDistributionChart.setOption({
    // 配置
  })
  */
}

onMounted(() => {
  // 初始化图表
  // initCharts()
})
</script>

<style scoped>
.analytics {
  width: 100%;
}

.page-header {
  margin-bottom: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.chart-row {
  margin-bottom: 20px;
}

.chart-card {
  height: 400px;
}

.chart-header {
  margin-bottom: 15px;
}

.chart-container {
  height: 330px;
}

.data-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.increase-up {
  color: #67C23A;
}

.increase-down {
  color: #F56C6C;
}
</style> 