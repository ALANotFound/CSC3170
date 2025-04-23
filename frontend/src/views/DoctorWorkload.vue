<template>
  <div class="doctor-workload">
    <div class="page-header">
      <h2>医师工作量</h2>
    </div>
    
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="医师">
          <el-select
            v-model="searchForm.DoctorID"
            placeholder="请选择医师"
            filterable
            clearable
            style="width: 200px"
          >
            <el-option
              v-for="doctor in doctorList"
              :key="doctor.DoctorID"
              :label="doctor.DoctorName"
              :value="doctor.DoctorID"
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
      <el-col :span="6">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>门诊人次</span>
            </div>
          </template>
          <div class="card-content">
            <div class="number">{{ stats.outpatientCount || 0 }}</div>
            <div class="trend" :class="stats.outpatientTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.outpatientTrend) }}%
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>住院人次</span>
            </div>
          </template>
          <div class="card-content">
            <div class="number">{{ stats.inpatientCount || 0 }}</div>
            <div class="trend" :class="stats.inpatientTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.inpatientTrend) }}%
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>手术台次</span>
            </div>
          </template>
          <div class="card-content">
            <div class="number">{{ stats.surgeryCount || 0 }}</div>
            <div class="trend" :class="stats.surgeryTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.surgeryTrend) }}%
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>平均工作时长</span>
            </div>
          </template>
          <div class="card-content">
            <div class="number">{{ stats.avgWorkHours || 0 }}h</div>
            <div class="trend" :class="stats.workHoursTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.workHoursTrend) }}%
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card class="chart-card">
      <template #header>
        <div class="card-header">
          <span>工作量趋势</span>
        </div>
      </template>
      <div class="chart-container">
        <div ref="workloadChart" style="width: 100%; height: 400px;"></div>
      </div>
    </el-card>
    
    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>工作量明细</span>
        </div>
      </template>
      <el-table
        :data="workloadList"
        border
        style="width: 100%"
      >
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="outpatient" label="门诊人次" width="120" />
        <el-table-column prop="inpatient" label="住院人次" width="120" />
        <el-table-column prop="surgery" label="手术台次" width="120" />
        <el-table-column prop="workHours" label="工作时长(h)" width="120" />
        <el-table-column prop="trend" label="环比变化" width="120">
          <template #default="scope">
            <span :class="scope.row.trend >= 0 ? 'up' : 'down'">
              {{ scope.row.trend >= 0 ? '+' : '' }}{{ scope.row.trend }}%
            </span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { getDoctorList } from '@/api/doctor'

const searchForm = reactive({
  DoctorID: '',
  dateRange: []
})

const doctorList = ref([])
const stats = reactive({
  outpatientCount: 0,
  outpatientTrend: 0,
  inpatientCount: 0,
  inpatientTrend: 0,
  surgeryCount: 0,
  surgeryTrend: 0,
  avgWorkHours: 0,
  workHoursTrend: 0
})

const workloadList = ref([])
let workloadChart = null

// 获取医师列表
const fetchDoctorList = async () => {
  try {
    const res = await getDoctorList()
    doctorList.value = res.data.list || res.data
  } catch (error) {
    console.error('获取医师列表失败:', error)
    ElMessage.error('获取医师列表失败')
  }
}

// 获取统计数据
const fetchStats = async () => {
  try {
    const params = {
      id: searchForm.DoctorID,
      startDate: searchForm.dateRange?.[0],
      endDate: searchForm.dateRange?.[1]
    }
    // 暂时使用模拟数据
    const mockData = {
      stats: {
        outpatientCount: 150,
        outpatientTrend: 8,
        inpatientCount: 45,
        inpatientTrend: 5,
        surgeryCount: 20,
        surgeryTrend: 3,
        avgWorkHours: 8.5,
        workHoursTrend: -1
      },
      details: [
        { date: '2024-01', outpatient: 45, inpatient: 15, surgery: 6, workHours: 8.2, trend: 5 },
        { date: '2024-02', outpatient: 50, inpatient: 18, surgery: 8, workHours: 8.8, trend: 8 },
        { date: '2024-03', outpatient: 55, inpatient: 12, surgery: 6, workHours: 8.0, trend: -3 }
      ],
      trendData: [
        { date: '2024-01', outpatient: 45, inpatient: 15, surgery: 6, workHours: 8.2 },
        { date: '2024-02', outpatient: 50, inpatient: 18, surgery: 8, workHours: 8.8 },
        { date: '2024-03', outpatient: 55, inpatient: 12, surgery: 6, workHours: 8.0 }
      ]
    }
    Object.assign(stats, mockData.stats)
    workloadList.value = mockData.details
    initWorkloadChart(mockData.trendData)
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  }
}

// 初始化工作量趋势图表
const initWorkloadChart = (data) => {
  if (!workloadChart) {
    workloadChart = echarts.init(document.querySelector('.chart-container .chart'))
  }
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['门诊人次', '住院人次', '手术台次', '工作时长']
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.date)
    },
    yAxis: [
      {
        type: 'value',
        name: '人次/台次'
      },
      {
        type: 'value',
        name: '小时',
        position: 'right'
      }
    ],
    series: [
      {
        name: '门诊人次',
        type: 'line',
        data: data.map(item => item.outpatient)
      },
      {
        name: '住院人次',
        type: 'line',
        data: data.map(item => item.inpatient)
      },
      {
        name: '手术台次',
        type: 'line',
        data: data.map(item => item.surgery)
      },
      {
        name: '工作时长',
        type: 'line',
        yAxisIndex: 1,
        data: data.map(item => item.workHours)
      }
    ]
  }
  
  workloadChart.setOption(option)
}

// 搜索
const handleSearch = () => {
  fetchStats()
}

// 组件挂载时获取数据
onMounted(() => {
  fetchDoctorList()
  fetchStats()
  
  // 监听窗口大小变化，调整图表大小
  window.addEventListener('resize', () => {
    workloadChart?.resize()
  })
})
</script>

<style scoped>
.doctor-workload {
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

.table-card {
  margin-bottom: 20px;
}

.up {
  color: #67c23a;
}

.down {
  color: #f56c6c;
}
</style> 