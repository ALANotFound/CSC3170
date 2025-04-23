<template>
  <div class="admission-list">
    <div class="page-header">
      <h2>在院患者管理</h2>
      <el-button type="primary" @click="$router.push('/admissions/add')">办理入院</el-button>
    </div>
    
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="患者姓名">
          <el-input v-model="searchForm.PatientName" placeholder="请输入患者姓名" clearable />
        </el-form-item>
        <el-form-item label="病房">
          <el-select 
            v-model="searchForm.WardID" 
            placeholder="请选择病房" 
            clearable
            style="width: 200px"
            filterable
            :filter-method="filterWard"
          >
            <el-option 
              v-for="ward in filteredWardList" 
              :key="ward.WardID" 
              :label="ward.WardName" 
              :value="ward.WardID"
            >
              <span>{{ ward.WardName }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">
                {{ ward.WardType || '普通病房' }}
              </span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="床位号">
          <el-input v-model="searchForm.BedNo" placeholder="请输入床位号" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="table-card">
      <el-table
        v-loading="loading"
        :data="filteredAdmissionList"
        border
        style="width: 100%"
        :header-cell-style="{textAlign: 'center'}"
        :cell-style="{textAlign: 'center'}"
      >
        <el-table-column prop="AdmissionID" label="ID" width="80" align="center" />
        <el-table-column label="患者姓名" min-width="120" align="center">
          <template #default="scope">
            {{ scope.row.patientName || '加载中...' }}
          </template>
        </el-table-column>
        <el-table-column label="病房" min-width="120" align="center">
          <template #default="scope">
            {{ getWardName(scope.row.WardID) }}
          </template>
        </el-table-column>
        <el-table-column prop="BedNo" label="床位号" width="100" align="center" />
        <el-table-column prop="AdmissionDate" label="入院日期" width="120" align="center" />
        <el-table-column label="操作" width="150" fixed="right" align="center">
          <template #default="scope">
            <el-button
              type="danger"
              size="small"
              @click="handleDischarge(scope.row)"
              >办理出院</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getActiveAdmissions, dischargePatient } from '@/api/admission'
import { getWardList } from '@/api/ward'
import { getPatientDetail } from '@/api/patient'

const loading = ref(false)
const admissionList = ref([])
const filteredAdmissionList = ref([])
const wardList = ref([])
const filteredWardList = ref([])

// 搜索表单
const searchForm = reactive({
  PatientName: '',
  WardID: '',
  BedNo: ''
})

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0
})

// 获取在院患者列表
const fetchAdmissionList = async () => {
  loading.value = true
  try {
    const res = await getActiveAdmissions()
    admissionList.value = res.data.list || []
    pagination.total = res.data.total || 0
    
    // 获取每个入院记录的患者信息
    for (const admission of admissionList.value) {
      try {
        const patientRes = await getPatientDetail(admission.PatientID)
        if (patientRes.data) {
          admission.patientName = patientRes.data.Name
        } else {
          admission.patientName = '未知患者'
        }
      } catch (error) {
        console.error(`获取患者 ${admission.PatientID} 信息失败:`, error)
        admission.patientName = '未知患者'
      }
    }
    
    filterAndPaginateAdmissions()
  } catch (error) {
    console.error('获取在院患者列表失败:', error)
    ElMessage.error('获取在院患者列表失败')
  } finally {
    loading.value = false
  }
}

// 获取病房列表
const fetchWardList = async () => {
  try {
    const res = await getWardList()
    wardList.value = res.data.list || res.data
    filteredWardList.value = wardList.value
  } catch (error) {
    console.error('获取病房列表失败:', error)
  }
}

// 根据病房ID获取病房名称
const getWardName = (wardId) => {
  const ward = wardList.value.find(item => item.WardID === wardId)
  return ward ? ward.WardName : '未知'
}

// 病房过滤方法
const filterWard = (query) => {
  if (query) {
    filteredWardList.value = wardList.value.filter(ward => 
      ward.WardName.toLowerCase().includes(query.toLowerCase()) ||
      (ward.WardType && ward.WardType.toLowerCase().includes(query.toLowerCase()))
    )
  } else {
    filteredWardList.value = wardList.value
  }
}

// 过滤和分页处理
const filterAndPaginateAdmissions = () => {
  // 先进行过滤
  let filtered = [...admissionList.value]
  
  if (searchForm.PatientName) {
    filtered = filtered.filter(item => 
      item.patientName.toLowerCase().includes(searchForm.PatientName.toLowerCase())
    )
  }
  
  if (searchForm.WardID) {
    filtered = filtered.filter(item => item.WardID === searchForm.WardID)
  }
  
  if (searchForm.BedNo) {
    filtered = filtered.filter(item => item.BedNo === searchForm.BedNo)
  }
  
  // 更新总数
  pagination.total = filtered.length
  
  // 计算分页
  const start = (pagination.current - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  filteredAdmissionList.value = filtered.slice(start, end)
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  filterAndPaginateAdmissions()
}

// 重置搜索
const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  pagination.current = 1
  filterAndPaginateAdmissions()
}

// 办理出院
const handleDischarge = (row) => {
  ElMessageBox.confirm(
    `确定要为患者 "${row.patientName}" 办理出院吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const dischargeData = {
        DischargeDate: new Date().toISOString().split('T')[0]
      }
      await dischargePatient(row.AdmissionID, dischargeData)
      ElMessage.success('出院办理成功')
      fetchAdmissionList()
    } catch (error) {
      console.error('办理出院失败:', error)
      ElMessage.error('办理出院失败')
    }
  }).catch(() => {
    // 取消操作
  })
}

// 页面大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  filterAndPaginateAdmissions()
}

// 当前页变化
const handleCurrentChange = (page) => {
  pagination.current = page
  filterAndPaginateAdmissions()
}

// 组件挂载时获取数据
onMounted(async () => {
  await fetchWardList()
  await fetchAdmissionList()
})
</script>

<style scoped>
.admission-list {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 