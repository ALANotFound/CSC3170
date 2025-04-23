<template>
  <div class="revenue-stats">
    <div class="page-header">
      <h2>流水统计</h2>
    </div>
    
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
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
              <span>总收入</span>
            </div>
          </template>
          <div class="card-content">
            <div class="number">¥{{ stats.totalRevenue || 0 }}</div>
            <div class="trend" :class="stats.revenueTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.revenueTrend) }}%
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>门诊收入</span>
            </div>
          </template>
          <div class="card-content">
            <div class="number">¥{{ stats.outpatientRevenue || 0 }}</div>
            <div class="trend" :class="stats.outpatientTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.outpatientTrend) }}%
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>住院收入</span>
            </div>
          </template>
          <div class="card-content">
            <div class="number">¥{{ stats.inpatientRevenue || 0 }}</div>
            <div class="trend" :class="stats.inpatientTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.inpatientTrend) }}%
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card class="chart-card">
      <template #header>
        <div class="card-header">
          <span>收入趋势</span>
        </div>
      </template>
      <div class="chart-container">
        <div ref="revenueChart" style="width: 100%; height: 400px;"></div>
      </div>
    </el-card>
    
    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>收入明细</span>
        </div>
      </template>
      <el-table
        :data="revenueList"
        border
        style="width: 100%"
      >
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="outpatient" label="门诊收入" width="120">
          <template #default="scope">
            ¥{{ scope.row.outpatient }}
          </template>
        </el-table-column>
        <el-table-column prop="inpatient" label="住院收入" width="120">
          <template #default="scope">
            ¥{{ scope.row.inpatient }}
          </template>
        </el-table-column>
        <el-table-column prop="total" label="总收入" width="120">
          <template #default="scope">
            ¥{{ scope.row.total }}
          </template>
        </el-table-column>
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

const searchForm = reactive({
  dateRange: []
})

const stats = reactive({
  totalRevenue: 0,
  revenueTrend: 0,
  outpatientRevenue: 0,
  outpatientTrend: 0,
  inpatientRevenue: 0,
  inpatientTrend: 0
})

const revenueList = ref([])
let revenueChart = null

// 获取统计数据
const fetchStats = async () => {
  try {
    const params = {
      startDate: searchForm.dateRange?.[0],
      endDate: searchForm.dateRange?.[1]
    }
    // 暂时使用模拟数据
    const mockData = {
      stats: {
        totalRevenue: 100000,
        revenueTrend: 5,
        outpatientRevenue: 60000,
        outpatientTrend: 3,
        inpatientRevenue: 40000,
        inpatientTrend: 8
      },
      details: [
        { date: '2024-01', outpatient: 20000, inpatient: 15000, total: 35000, trend: 5 },
        { date: '2024-02', outpatient: 22000, inpatient: 16000, total: 38000, trend: 8 },
        { date: '2024-03', outpatient: 18000, inpatient: 9000, total: 27000, trend: -3 }
      ],
      trendData: [
        { date: '2024-01', total: 35000, outpatient: 20000, inpatient: 15000 },
        { date: '2024-02', total: 38000, outpatient: 22000, inpatient: 16000 },
        { date: '2024-03', total: 27000, outpatient: 18000, inpatient: 9000 }
      ]
    }
    Object.assign(stats, mockData.stats)
    revenueList.value = mockData.details
    initRevenueChart(mockData.trendData)
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  }
}

// 初始化收入趋势图表
const initRevenueChart = (data) => {
  if (!revenueChart) {
    revenueChart = echarts.init(document.querySelector('.chart-container .chart'))
  }
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        let result = params[0].axisValue + '<br/>'
        params.forEach(param => {
          result += param.seriesName + ': ¥' + param.value + '<br/>'
        })
        return result
      }
    },
    legend: {
      data: ['总收入', '门诊收入', '住院收入']
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.date)
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '¥{value}'
      }
    },
    series: [
      {
        name: '总收入',
        type: 'line',
        data: data.map(item => item.total)
      },
      {
        name: '门诊收入',
        type: 'line',
        data: data.map(item => item.outpatient)
      },
      {
        name: '住院收入',
        type: 'line',
        data: data.map(item => item.inpatient)
      }
    ]
  }
  
  revenueChart.setOption(option)
}

// 搜索
const handleSearch = () => {
  fetchStats()
}

// 组件挂载时获取数据
onMounted(() => {
  fetchStats()
  
  // 监听窗口大小变化，调整图表大小
  window.addEventListener('resize', () => {
    revenueChart?.resize()
  })
})
</script>

<style scoped>
.revenue-stats {
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