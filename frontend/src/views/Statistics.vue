<template>
  <div class="statistics">
    <div class="page-header">
      <h2>统计分析</h2>
    </div>
    
    <!-- 搜索表单 -->
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
    
    <!-- 基础统计卡片 -->
    <el-row :gutter="20" class="stats-cards">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon patient">
              <el-icon><el-icon-user /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">门诊人次</div>
              <div class="stat-value">{{ stats.outpatientCount || 0 }}</div>
            </div>
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
              <div class="stat-title">住院人次</div>
              <div class="stat-value">{{ stats.inpatientCount || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon surgery">
              <el-icon><el-icon-first-aid-kit /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">手术台次</div>
              <div class="stat-value">{{ stats.totalPatients || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon revenue">
              <el-icon><el-icon-money /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">总收入</div>
              <div class="stat-value">¥{{ stats.totalRevenue || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 医师工作量统计 -->
    <el-card class="section-card" v-if="searchForm.DeptID">
      <template #header>
        <div class="card-header">
          <span>医师工作量统计</span>
        </div>
      </template>
      <el-table
        :data="departmentDoctorsStats"
        border
        style="width: 100%"
      >
        <el-table-column prop="doctorName" label="医师姓名" align="center" width="180" />
        <el-table-column prop="visitCount" label="门诊人次" align="right" width="180" />
        <el-table-column prop="admissionCount" label="住院人次" align="right" width="180" />
        <el-table-column prop="totalPatients" label="手术台次" align="right" width="180" />
        <el-table-column prop="avgWorkHours" label="平均工作时长" align="right">
          <template #default="scope">
            {{ scope.row.avgWorkHours }}h
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 收入明细表格 -->
    <el-card class="section-card">
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
        <el-table-column prop="date" label="日期" align="center" width="180" />
        <el-table-column prop="deptName" label="科室" align="center" width="180" v-if="!searchForm.DeptID" />
        <el-table-column prop="outpatientRevenue" label="门诊收入" align="right" width="180">
          <template #default="scope">
            ¥{{ scope.row.outpatientRevenue.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="inpatientRevenue" label="住院收入" align="right" width="180">
          <template #default="scope">
            ¥{{ scope.row.inpatientRevenue.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="total" label="总收入" align="right" width="180">
          <template #default="scope">
            ¥{{ scope.row.total.toFixed(2) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getDepartmentList, getDepartmentDetail } from '@/api/department'
import { getDoctorList } from '@/api/doctor'
import { getDepartmentStats, getDoctorWorkload, getRevenueStats } from '@/api/report'

const searchForm = reactive({
  DeptID: '',
  dateRange: []
})

const departmentList = ref([])
const departmentDoctorsStats = ref([])
const currentDepartment = ref('')

const stats = reactive({
  outpatientCount: 0,
  inpatientCount: 0,
  totalPatients: 0,
  totalRevenue: 0
})

const revenueList = ref([])

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
    await fetchDepartmentDoctorsStats()
  } else {
    currentDepartment.value = ''
    departmentDoctorsStats.value = []
  }
  fetchStats()
}

// 获取科室内所有医师工作量统计的函数
const fetchDepartmentDoctorsStats = async () => {
  try {
    const params = {
      startDate: searchForm.dateRange?.[0],
      endDate: searchForm.dateRange?.[1]
    }
    
    // 获取科室内的医师列表
    const doctorRes = await getDoctorList()
    const doctors = (doctorRes.data.list || doctorRes.data).filter(
      doctor => doctor.DeptID === searchForm.DeptID
    )
    
    const statsPromises = doctors.map(async doctor => {
      const res = await getDoctorWorkload(doctor.DoctorID, params)
      return {
        doctorId: doctor.DoctorID,
        doctorName: doctor.Name,
        ...res.data
      }
    })
    
    const allStats = await Promise.all(statsPromises)
    departmentDoctorsStats.value = allStats.map(stat => ({
      doctorName: stat.doctorName,
      visitCount: stat.visitCount || 0,
      admissionCount: stat.admissionCount || 0,
      totalPatients: stat.totalPatients || 0,
      avgWorkHours: stat.avgWorkHours || 0
    }))
  } catch (error) {
    console.error('获取科室医师工作量统计失败:', error)
    ElMessage.error('获取科室医师工作量统计失败')
  }
}

// 获取统计数据
const fetchStats = async () => {
  try {
    const params = {
      startDate: searchForm.dateRange?.[0],
      endDate: searchForm.dateRange?.[1]
    }
    
    // 获取科室统计数据
    if (searchForm.DeptID) {
      const deptRes = await getDepartmentStats(searchForm.DeptID)
      if (deptRes.data && deptRes.data.length > 0) {
        const deptStats = deptRes.data[0]
        stats.outpatientCount = deptStats.outpatientCount || 0
        stats.inpatientCount = deptStats.inpatientCount || 0
        stats.totalRevenue = deptStats.totalRevenue || 0
        
        // 获取选中科室的收入明细
        const revenueRes = await getRevenueStats({ deptId: searchForm.DeptID, ...params })
        if (revenueRes.data && revenueRes.data.Details) {
          revenueList.value = revenueRes.data.Details.map(item => ({
            date: item.Period,
            outpatientRevenue: item.OutpatientRevenue || 0,
            inpatientRevenue: item.InpatientRevenue || 0,
            total: item.Revenue || 0
          }))
        }
      }
    } else {
      // 获取所有科室的汇总数据
      const allDepts = departmentList.value
      const allStats = await Promise.all(
        allDepts.map(dept => getDepartmentStats(dept.DeptID))
      )
      
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
      
      // 获取所有科室的收入明细
      const revenueRes = await getRevenueStats(params)
      if (revenueRes.data && revenueRes.data.Details) {
        revenueList.value = revenueRes.data.Details.map(item => ({
          date: item.Period,
          deptName: item.DeptName,
          outpatientRevenue: item.OutpatientRevenue || 0,
          inpatientRevenue: item.InpatientRevenue || 0,
          total: item.Revenue || 0
        }))
      }
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  }
}

// 搜索
const handleSearch = () => {
  fetchStats()
  if (searchForm.DeptID) {
    fetchDepartmentDoctorsStats()
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchDepartmentList()
  fetchStats()
})
</script>

<style scoped>
.statistics {
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

.stat-card {
  height: 100px;
}

.stat-card-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
  color: #fff;
}

.stat-icon.patient {
  background-color: #409EFF;
}

.stat-icon.hospitalization {
  background-color: #F56C6C;
}

.stat-icon.surgery {
  background-color: #E6A23C;
}

.stat-icon.revenue {
  background-color: #67C23A;
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

.section-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-card {
  height: 100%;
}

.card-content {
  text-align: center;
}

.number {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}
</style> 