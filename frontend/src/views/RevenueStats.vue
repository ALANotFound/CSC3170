<template>
  <div class="revenue-stats">
    <div class="page-header">
      <h2>流水统计</h2>
    </div>
    
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-row :gutter="20" class="stats-cards">
      <el-col :span="24">
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
        <el-table-column prop="total" label="收入" width="120">
          <template #default="scope">
            ¥{{ scope.row.total }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getRevenueStats } from '@/api/report'

const searchForm = reactive({})

const stats = reactive({
  totalRevenue: 0
})

const revenueList = ref([])

// 获取统计数据
const fetchStats = async () => {
  try {
    const res = await getRevenueStats()
    if (res.data) {
      stats.totalRevenue = res.data.Total || 0
      
      // 处理收入明细数据
      revenueList.value = res.data.Details.map(item => ({
        date: item.Period,
        total: item.Revenue
      }))
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
  fetchStats()
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