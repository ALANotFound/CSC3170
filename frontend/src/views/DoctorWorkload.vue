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
            @change="handleDoctorChange"
          >
            <el-option
              v-for="doctor in doctorList"
              :key="doctor.DoctorID"
              :label="doctor.Name"
              :value="doctor.DoctorID"
            >
              <span>{{ doctor.Name }}</span>
            </el-option>
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
      <div v-if="currentDoctor" class="doctor-info">
        当前选择：{{ currentDoctor }}
      </div>
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
            <div class="number">{{ stats.visitCount || 0 }}</div>
            <div class="trend" :class="stats.visitTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.visitTrend) }}%
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
            <div class="number">{{ stats.admissionCount || 0 }}</div>
            <div class="trend" :class="stats.admissionTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.admissionTrend) }}%
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
            <div class="number">{{ stats.totalPatients || 0 }}</div>
            <div class="trend" :class="stats.patientsTrend >= 0 ? 'up' : 'down'">
              <el-icon><el-icon-caret-top /></el-icon>
              {{ Math.abs(stats.patientsTrend) }}%
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getDoctorList, getDoctorDetail } from '@/api/doctor'
import { getDoctorWorkload } from '@/api/report'

const searchForm = reactive({
  DoctorID: '',
  dateRange: []
})

const doctorList = ref([])
const currentDoctor = ref('')
const stats = reactive({
  visitCount: 0,
  visitTrend: 0,
  admissionCount: 0,
  admissionTrend: 0,
  totalPatients: 0,
  patientsTrend: 0,
  avgWorkHours: 0,
  workHoursTrend: 0
})

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

// 获取医师详情
const fetchDoctorDetail = async (id) => {
  try {
    const res = await getDoctorDetail(id)
    if (res.data) {
      currentDoctor.value = res.data.DoctorName
    }
  } catch (error) {
    console.error('获取医师详情失败:', error)
    ElMessage.error('获取医师详情失败')
  }
}

// 处理医师选择变化
const handleDoctorChange = async (value) => {
  if (value) {
    await fetchDoctorDetail(value)
  } else {
    currentDoctor.value = ''
  }
  fetchStats()
}

// 获取统计数据
const fetchStats = async () => {
  try {
    const params = {
      startDate: searchForm.dateRange?.[0],
      endDate: searchForm.dateRange?.[1]
    }
    
    if (searchForm.DoctorID) {
      const res = await getDoctorWorkload(searchForm.DoctorID, params)
      if (res.data) {
        stats.visitCount = res.data.visitCount || 0
        stats.admissionCount = res.data.admissionCount || 0
        stats.totalPatients = res.data.totalPatients || 0
        stats.avgWorkHours = res.data.avgWorkHours || 0
        // 由于后端没有提供趋势数据，这里设置为0
        stats.visitTrend = 0
        stats.admissionTrend = 0
        stats.patientsTrend = 0
        stats.workHoursTrend = 0
      }
    } else {
      // 如果没有选择医生，显示所有医生的汇总数据
      const allDoctors = doctorList.value
      const allStats = await Promise.all(
        allDoctors.map(doctor => getDoctorWorkload(doctor.DoctorID, params))
      )
      
      // 汇总所有医生的数据
      const totalStats = allStats.reduce((acc, curr) => {
        if (curr.data) {
          acc.visitCount += curr.data.visitCount || 0
          acc.admissionCount += curr.data.admissionCount || 0
          acc.totalPatients += curr.data.totalPatients || 0
          acc.avgWorkHours += curr.data.avgWorkHours || 0
        }
        return acc
      }, {
        visitCount: 0,
        admissionCount: 0,
        totalPatients: 0,
        avgWorkHours: 0
      })
      
      // 计算平均工作时长
      if (allDoctors.length > 0) {
        totalStats.avgWorkHours = totalStats.avgWorkHours / allDoctors.length
      }
      
      Object.assign(stats, totalStats)
      // 由于后端没有提供趋势数据，这里设置为0
      stats.visitTrend = 0
      stats.admissionTrend = 0
      stats.patientsTrend = 0
      stats.workHoursTrend = 0
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
  fetchDoctorList()
  fetchStats()
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

.doctor-info {
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

.up {
  color: #67c23a;
}

.down {
  color: #f56c6c;
}
</style> 