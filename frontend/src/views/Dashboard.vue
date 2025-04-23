<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h2>医院管理系统仪表盘</h2>
    </div>
    
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon patient">
              <el-icon><el-icon-user /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">患者总数</div>
              <div class="stat-value">{{ stats.patientCount }}</div>
            </div>
          </div>
          <div class="stat-footer">
            <span>今日新增: {{ stats.todayNewPatients }}</span>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon doctor">
              <el-icon><el-icon-user-filled /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">医师总数</div>
              <div class="stat-value">{{ stats.doctorCount }}</div>
            </div>
          </div>
          <div class="stat-footer">
            <span>科室数: {{ stats.departmentCount }}</span>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon consultation">
              <el-icon><el-icon-document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">今日就诊</div>
              <div class="stat-value">{{ stats.todayConsultations }}</div>
            </div>
          </div>
          <div class="stat-footer">
            <span>较昨日: {{ stats.consultationChange >= 0 ? '+' : '' }}{{ stats.consultationChange }}%</span>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon hospitalization">
              <el-icon><el-icon-house /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">住院人数</div>
              <div class="stat-value">{{ stats.currentHospitalizations }}</div>
            </div>
          </div>
          <div class="stat-footer">
            <span>病房使用率: {{ stats.wardOccupancyRate }}%</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <div class="chart-header">
            <h3>各科室就诊情况</h3>
          </div>
          <div class="chart-container" ref="departmentChartRef"></div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="chart-card">
          <div class="chart-header">
            <h3>近7日就诊趋势</h3>
          </div>
          <div class="chart-container" ref="trendChartRef"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="list-row">
      <el-col :span="12">
        <el-card class="list-card">
          <template #header>
            <div class="card-header">
              <span>今日预约</span>
              <el-button class="button" text>查看全部</el-button>
            </div>
          </template>
          <el-table :data="todayAppointments" style="width: 100%">
            <el-table-column prop="time" label="时间" width="120" />
            <el-table-column prop="patientName" label="患者姓名" width="120" />
            <el-table-column prop="doctorName" label="医师" width="120" />
            <el-table-column prop="department" label="科室" />
            <el-table-column prop="status" label="状态">
              <template #default="scope">
                <el-tag :type="scope.row.status === '已完成' ? 'success' : scope.row.status === '待就诊' ? 'warning' : 'info'">
                  {{ scope.row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="list-card">
          <template #header>
            <div class="card-header">
              <span>待处理事项</span>
              <el-button class="button" text>查看全部</el-button>
            </div>
          </template>
          <el-table :data="pendingTasks" style="width: 100%">
            <el-table-column prop="time" label="时间" width="120" />
            <el-table-column prop="type" label="类型" width="120">
              <template #default="scope">
                <el-tag :type="scope.row.type === '入院' ? 'success' : scope.row.type === '出院' ? 'warning' : 'info'">
                  {{ scope.row.type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="patientName" label="患者姓名" width="120" />
            <el-table-column prop="description" label="描述" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
// 假设我们会导入echarts
// import * as echarts from 'echarts'

// 统计数据
const stats = reactive({
  patientCount: 1248,
  todayNewPatients: 32,
  doctorCount: 76,
  departmentCount: 12,
  todayConsultations: 156,
  consultationChange: 5.2,
  currentHospitalizations: 87,
  wardOccupancyRate: 72.5
})

// 今日预约数据
const todayAppointments = ref([
  { time: '09:00', patientName: '张三', doctorName: '李医生', department: '内科', status: '已完成' },
  { time: '10:30', patientName: '李四', doctorName: '王医生', department: '外科', status: '已完成' },
  { time: '13:00', patientName: '王五', doctorName: '赵医生', department: '儿科', status: '待就诊' },
  { time: '14:30', patientName: '赵六', doctorName: '钱医生', department: '妇科', status: '待就诊' },
  { time: '16:00', patientName: '孙七', doctorName: '孙医生', department: '骨科', status: '已取消' }
])

// 待处理事项
const pendingTasks = ref([
  { time: '2023-04-22', type: '入院', patientName: '张三', description: '安排入院手续及病房' },
  { time: '2023-04-23', type: '出院', patientName: '李四', description: '准备出院结算' },
  { time: '2023-04-23', type: '转科', patientName: '王五', description: '从内科转至外科' },
  { time: '2023-04-24', type: '手术', patientName: '赵六', description: '准备手术相关事宜' },
  { time: '2023-04-25', type: '复诊', patientName: '孙七', description: '安排复诊检查' }
])

// 图表引用
const departmentChartRef = ref(null)
const trendChartRef = ref(null)

// 初始化图表
const initCharts = () => {
  /* 
  实际项目中会使用echarts创建图表，这里仅作示例
  const departmentChart = echarts.init(departmentChartRef.value)
  departmentChart.setOption({
    // 饼图配置
  })
  
  const trendChart = echarts.init(trendChartRef.value)
  trendChart.setOption({
    // 折线图配置
  })
  */
}

onMounted(() => {
  // 初始化图表
  // initCharts()
})
</script>

<style scoped>
.dashboard {
  width: 100%;
}

.dashboard-header {
  margin-bottom: 20px;
}

.stat-card {
  height: 130px;
  margin-bottom: 20px;
}

.stat-card-content {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 30px;
  color: #fff;
}

.stat-icon.patient {
  background-color: #409EFF;
}

.stat-icon.doctor {
  background-color: #67C23A;
}

.stat-icon.consultation {
  background-color: #E6A23C;
}

.stat-icon.hospitalization {
  background-color: #F56C6C;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
}

.stat-footer {
  font-size: 12px;
  color: #909399;
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

.list-row {
  margin-bottom: 20px;
}

.list-card {
  height: 320px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 