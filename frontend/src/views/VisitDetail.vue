<template>
  <div class="visit-detail">
    <div class="page-header">
      <h2>就诊记录详情</h2>
      <el-button @click="$router.back()">返回</el-button>
    </div>
    
    <el-card v-loading="loading">
      <template v-if="visit">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="患者姓名">{{ patientName }}</el-descriptions-item>
          <el-descriptions-item label="就诊医师">{{ doctorName }}</el-descriptions-item>
          <el-descriptions-item label="就诊日期">{{ visit.VisitDate }}</el-descriptions-item>
          <el-descriptions-item label="费用">{{ visit.Fee }}元</el-descriptions-item>
          
          <el-descriptions-item label="主诉" :span="2">
            <div class="text-block">{{ visit.Complaint || '无' }}</div>
          </el-descriptions-item>
          
          <el-descriptions-item label="诊断" :span="2">
            <div class="text-block">{{ visit.Diagnosis || '无' }}</div>
          </el-descriptions-item>
          
          <el-descriptions-item label="处方" :span="2">
            <div class="text-block">{{ visit.Prescription || '无' }}</div>
            <el-button 
              type="primary" 
              size="small"
              style="margin-top: 10px;"
              @click="handleEditPrescription"
            >
              编辑处方
            </el-button>
          </el-descriptions-item>
        </el-descriptions>
      </template>
      
      <div v-else class="empty-data">
        <el-empty description="未找到就诊记录" />
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
          <span>{{ patientName }}</span>
        </el-form-item>
        <el-form-item label="诊断">
          <span>{{ visit?.Diagnosis }}</span>
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getVisitDetail, updatePrescription } from '@/api/visit'
import { getPatientList } from '@/api/patient'
import { getDoctorList } from '@/api/doctor'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const visit = ref(null)
const patientList = ref([])
const doctorList = ref([])

// 处方编辑相关
const prescriptionDialogVisible = ref(false)
const prescriptionFormRef = ref(null)
const prescriptionForm = reactive({
  Prescription: ''
})
const prescriptionRules = {
  Prescription: [{ required: true, message: '请输入处方内容', trigger: 'blur' }]
}

// 计算患者姓名
const patientName = computed(() => {
  if (!visit.value || !patientList.value.length) return '未知'
  
  const patient = patientList.value.find(p => p.PatientID === visit.value.PatientID)
  return patient ? patient.Name : '未知'
})

// 计算医师姓名
const doctorName = computed(() => {
  if (!visit.value || !doctorList.value.length) return '未知'
  
  const doctor = doctorList.value.find(d => d.DoctorID === visit.value.DoctorID)
  return doctor ? doctor.Name : '未知'
})

// 获取就诊记录详情
const fetchVisitDetail = async () => {
  const id = route.params.id
  if (!id) return
  
  loading.value = true
  try {
    const res = await getVisitDetail(id)
    visit.value = res.data
  } catch (error) {
    console.error('获取就诊记录详情失败:', error)
    ElMessage.error('获取就诊记录详情失败')
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

// 打开编辑处方对话框
const handleEditPrescription = () => {
  if (!visit.value) return
  
  prescriptionForm.Prescription = visit.value.Prescription || ''
  prescriptionDialogVisible.value = true
}

// 提交处方
const submitPrescription = () => {
  if (!visit.value) return
  
  prescriptionFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      await updatePrescription(visit.value.VisitID, { Prescription: prescriptionForm.Prescription })
      ElMessage.success('处方更新成功')
      prescriptionDialogVisible.value = false
      
      // 更新本地数据
      visit.value.Prescription = prescriptionForm.Prescription
    } catch (error) {
      console.error('更新处方失败:', error)
      ElMessage.error('更新处方失败')
    }
  })
}

// 组件挂载时获取数据
onMounted(() => {
  fetchPatientList()
  fetchDoctorList()
  fetchVisitDetail()
})
</script>

<style scoped>
.visit-detail {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.text-block {
  white-space: pre-wrap;
  line-height: 1.5;
}

.empty-data {
  padding: 30px 0;
}
</style> 