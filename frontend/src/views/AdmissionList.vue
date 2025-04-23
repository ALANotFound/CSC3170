<template>
  <div class="admission-list">
    <div class="page-header">
      <h2>在院患者管理</h2>
      <el-button type="primary" @click="$router.push('/admissions/add')">办理入院</el-button>
    </div>
    
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="病房">
          <el-select v-model="searchForm.WardID" placeholder="请选择病房" clearable>
            <el-option v-for="ward in wardList" :key="ward.WardID" :label="ward.WardName" :value="ward.WardID" />
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
        :data="admissionList"
        border
        style="width: 100%"
        :header-cell-style="{textAlign: 'center'}"
        :cell-style="{textAlign: 'center'}"
      >
        <el-table-column prop="AdmissionID" label="ID" width="80" align="center" />
        <el-table-column label="患者" min-width="120" align="center">
          <template #default="scope">
            {{ getPatientName(scope.row.VisitID) }}
          </template>
        </el-table-column>
        <el-table-column label="病房" min-width="120" align="center">
          <template #default="scope">
            {{ getWardName(scope.row.WardID) }}
          </template>
        </el-table-column>
        <el-table-column prop="BedNo" label="床位号" width="100" align="center" />
        <el-table-column prop="AdmissionDate" label="入院日期" width="120" align="center" />
        <el-table-column prop="AdmissionReason" label="入院原因" min-width="150" align="center" />
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
import { getVisitList } from '@/api/visit'

const loading = ref(false)
const admissionList = ref([])
const wardList = ref([])
const visitList = ref([])

// 搜索表单
const searchForm = reactive({
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
    const params = {
      page: pagination.current,
      pageSize: pagination.pageSize,
      ...searchForm
    }
    
    const res = await getActiveAdmissions(params)
    admissionList.value = res.data.list || res.data
    pagination.total = res.data.total || res.data.length
    if (res.data.page) {
      pagination.current = res.data.page
    }
    if (res.data.pageSize) {
      pagination.pageSize = res.data.pageSize
    }
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
  } catch (error) {
    console.error('获取病房列表失败:', error)
  }
}

// 获取就诊记录列表
const fetchVisitList = async () => {
  try {
    const res = await getVisitList()
    visitList.value = res.data.list || res.data
  } catch (error) {
    console.error('获取就诊记录失败:', error)
  }
}

// 根据就诊ID获取患者姓名
const getPatientName = (visitId) => {
  const visit = visitList.value.find(item => item.VisitID === visitId)
  return visit ? visit.PatientName : '未知'
}

// 根据病房ID获取病房名称
const getWardName = (wardId) => {
  const ward = wardList.value.find(item => item.WardID === wardId)
  return ward ? ward.WardName : '未知'
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  fetchAdmissionList()
}

// 重置搜索
const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  pagination.current = 1
  fetchAdmissionList()
}

// 办理出院
const handleDischarge = (row) => {
  ElMessageBox.confirm(
    `确定要为患者 "${getPatientName(row.VisitID)}" 办理出院吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const dischargeData = {
        DischargeDate: new Date().toISOString().split('T')[0] // 格式化为 YYYY-MM-DD
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
  fetchAdmissionList()
}

// 当前页变化
const handleCurrentChange = (page) => {
  pagination.current = page
  fetchAdmissionList()
}

// 组件挂载时获取数据
onMounted(() => {
  fetchWardList()
  fetchVisitList()
  fetchAdmissionList()
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