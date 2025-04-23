<template>
  <div class="visit-list">
    <div class="page-header">
      <h2>就诊记录管理</h2>
      <el-button type="primary" @click="$router.push('/visits/add')">新增就诊记录</el-button>
    </div>
    
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="患者">
          <el-select 
            v-model="searchForm.PatientID" 
            placeholder="请选择患者" 
            clearable
            style="width: 200px"
            filterable
          >
            <el-option 
              v-for="patient in patientList" 
              :key="patient.PatientID" 
              :label="patient.Name" 
              :value="patient.PatientID" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="医师">
          <el-select 
            v-model="searchForm.DoctorID" 
            placeholder="请选择医师" 
            clearable
            style="width: 200px"
            filterable
          >
            <el-option 
              v-for="doctor in doctorList" 
              :key="doctor.DoctorID" 
              :label="doctor.Name" 
              :value="doctor.DoctorID" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="就诊日期">
          <el-date-picker
            v-model="searchForm.VisitDate"
            type="date"
            placeholder="选择日期"
            style="width: 200px"
            value-format="YYYY-MM-DD"
          />
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
        :data="getCurrentPageData()"
        border
        style="width: 100%"
        :header-cell-style="{textAlign: 'center'}"
        :cell-style="{textAlign: 'center'}"
      >
        <el-table-column prop="VisitID" label="ID" width="80" align="center" />
        <el-table-column label="患者" min-width="120" align="center">
          <template #default="scope">
            {{ getPatientName(scope.row.PatientID) }}
          </template>
        </el-table-column>
        <el-table-column label="医师" min-width="120" align="center">
          <template #default="scope">
            {{ getDoctorName(scope.row.DoctorID) }}
          </template>
        </el-table-column>
        <el-table-column prop="VisitDate" label="就诊日期" width="120" align="center" />
        <el-table-column prop="Complaint" label="主诉" min-width="150" align="center" />
        <el-table-column prop="Diagnosis" label="诊断" min-width="150" align="center" />
        <el-table-column prop="Fee" label="费用" width="100" align="center">
          <template #default="scope">
            {{ scope.row.Fee }}元
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="handleViewDetails(scope.row)"
              >查看</el-button
            >
            <el-button
              type="warning"
              size="small"
              @click="handleEditPrescription(scope.row)"
              >编辑处方</el-button
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

    <!-- 处方编辑对话框 -->
    <el-dialog
      v-model="prescriptionDialogVisible"
      title="编辑处方"
      width="50%"
    >
      <el-form
        ref="prescriptionFormRef"
        :model="prescriptionForm"
        :rules="prescriptionRules"
        label-width="100px"
      >
        <el-form-item label="患者">
          <span>{{ currentPatientName }}</span>
        </el-form-item>
        <el-form-item label="诊断">
          <span>{{ currentVisit.Diagnosis }}</span>
        </el-form-item>
        <el-form-item label="处方" prop="Prescription">
          <el-input
            type="textarea"
            v-model="prescriptionForm.Prescription"
            :rows="4"
            placeholder="请输入处方内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="prescriptionDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitPrescription">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getVisitList, updatePrescription } from '@/api/visit'
import { getPatientList } from '@/api/patient'
import { getDoctorList } from '@/api/doctor'

const router = useRouter()
const loading = ref(false)
const visitList = ref([])
const filteredVisitList = ref([])
const patientList = ref([])
const doctorList = ref([])

// 搜索表单
const searchForm = reactive({
  PatientID: '',
  DoctorID: '',
  VisitDate: ''
})

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0
})

// 处方编辑相关
const prescriptionDialogVisible = ref(false)
const prescriptionFormRef = ref(null)
const prescriptionForm = reactive({
  Prescription: ''
})
const prescriptionRules = {
  Prescription: [{ required: true, message: '请输入处方内容', trigger: 'blur' }]
}
const currentVisit = ref({})
const currentPatientName = ref('')

// 获取就诊记录列表
const fetchVisitList = async () => {
  loading.value = true
  try {
    const res = await getVisitList()
    visitList.value = res.data.list || res.data
    filteredVisitList.value = visitList.value
    pagination.total = visitList.value.length
    handleSearch() // 获取数据后立即应用筛选
  } catch (error) {
    console.error('获取就诊记录失败:', error)
    ElMessage.error('获取就诊记录失败')
  } finally {
    loading.value = false
  }
}

// 获取患者列表
const fetchPatientList = async () => {
  try {
    const res = await getPatientList()
    patientList.value = res.data.list || res.data
  } catch (error) {
    console.error('获取患者列表失败:', error)
  }
}

// 获取医师列表
const fetchDoctorList = async () => {
  try {
    const res = await getDoctorList()
    doctorList.value = res.data.list || res.data
  } catch (error) {
    console.error('获取医师列表失败:', error)
  }
}

// 根据患者ID获取患者姓名
const getPatientName = (patientId) => {
  const patient = patientList.value.find(item => item.PatientID === patientId)
  return patient ? patient.Name : '未知患者'
}

// 根据医师ID获取医师姓名
const getDoctorName = (doctorId) => {
  const doctor = doctorList.value.find(item => item.DoctorID === doctorId)
  return doctor ? doctor.Name : '未知医师'
}

// 搜索
const handleSearch = () => {
  // 根据搜索条件筛选数据
  filteredVisitList.value = visitList.value.filter(item => {
    const patientMatch = !searchForm.PatientID || 
      item.PatientID === searchForm.PatientID
    const doctorMatch = !searchForm.DoctorID || 
      item.DoctorID === searchForm.DoctorID
    const dateMatch = !searchForm.VisitDate || 
      item.VisitDate === searchForm.VisitDate
    return patientMatch && doctorMatch && dateMatch
  })
  
  // 更新分页信息
  pagination.total = filteredVisitList.value.length
  pagination.current = 1
}

// 重置搜索
const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  handleSearch()
}

// 获取当前页的数据
const getCurrentPageData = () => {
  const start = (pagination.current - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  return filteredVisitList.value.slice(start, end)
}

// 查看详情
const handleViewDetails = (row) => {
  router.push(`/visits/details/${row.VisitID}`)
}

// 编辑处方
const handleEditPrescription = (row) => {
  currentVisit.value = row
  prescriptionForm.Prescription = row.Prescription || ''
  currentPatientName.value = getPatientName(row.PatientID)
  prescriptionDialogVisible.value = true
}

// 提交处方
const submitPrescription = () => {
  prescriptionFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      await updatePrescription(currentVisit.value.VisitID, { Prescription: prescriptionForm.Prescription })
      ElMessage.success('处方更新成功')
      prescriptionDialogVisible.value = false
      fetchVisitList() // 刷新列表
    } catch (error) {
      console.error('更新处方失败:', error)
      ElMessage.error('更新处方失败')
    }
  })
}

// 页面大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.current = 1
}

// 当前页变化
const handleCurrentChange = (page) => {
  pagination.current = page
}

// 组件挂载时获取数据
onMounted(() => {
  fetchPatientList()
  fetchDoctorList()
  fetchVisitList()
})
</script>

<style scoped>
.visit-list {
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