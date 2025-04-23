<template>
  <div class="visit-form">
    <div class="page-header">
      <h2>新增就诊记录</h2>
      <el-button @click="$router.back()">返回</el-button>
    </div>
    
    <el-card>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        v-loading="loading"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="患者" prop="PatientID">
              <el-select v-model="form.PatientID" placeholder="请选择患者" style="width: 100%">
                <el-option 
                  v-for="patient in patientList" 
                  :key="patient.PatientID" 
                  :label="patient.Name" 
                  :value="patient.PatientID" 
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="医师" prop="DoctorID">
              <el-select v-model="form.DoctorID" placeholder="请选择医师" style="width: 100%">
                <el-option 
                  v-for="doctor in doctorList" 
                  :key="doctor.DoctorID" 
                  :label="doctor.Name" 
                  :value="doctor.DoctorID" 
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="就诊日期" prop="VisitDate">
              <el-date-picker
                v-model="form.VisitDate"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="费用" prop="Fee">
              <el-input-number v-model="form.Fee" :min="0" placeholder="请输入费用" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="主诉" prop="Complaint">
          <el-input
            type="textarea"
            v-model="form.Complaint"
            placeholder="请输入患者主诉"
            :rows="2"
          />
        </el-form-item>
        
        <el-form-item label="诊断" prop="Diagnosis">
          <el-input
            type="textarea"
            v-model="form.Diagnosis"
            placeholder="请输入诊断结果"
            :rows="2"
          />
        </el-form-item>
        
        <el-form-item label="处方" prop="Prescription">
          <el-input
            type="textarea"
            v-model="form.Prescription"
            placeholder="请输入处方内容"
            :rows="3"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm">保存</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { addVisit } from '@/api/visit'
import { getPatientList } from '@/api/patient'
import { getDoctorList } from '@/api/doctor'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const patientList = ref([])
const doctorList = ref([])

// 表单数据
const form = reactive({
  PatientID: '',
  DoctorID: '',
  VisitDate: new Date().toISOString().split('T')[0], // 默认今天
  Complaint: '',
  Diagnosis: '',
  Prescription: '',
  Fee: 0
})

// 表单验证规则
const rules = reactive({
  PatientID: [{ required: true, message: '请选择患者', trigger: 'change' }],
  DoctorID: [{ required: true, message: '请选择医师', trigger: 'change' }],
  VisitDate: [{ required: true, message: '请选择就诊日期', trigger: 'change' }],
  Complaint: [{ required: true, message: '请输入患者主诉', trigger: 'blur' }],
  Diagnosis: [{ required: true, message: '请输入诊断结果', trigger: 'blur' }],
  Fee: [{ required: true, message: '请输入费用', trigger: 'blur' }]
})

// 获取患者列表
const fetchPatientList = async () => {
  try {
    const res = await getPatientList()
    patientList.value = res.data.list || res.data
  } catch (error) {
    console.error('获取患者列表失败:', error)
    ElMessage.error('获取患者列表失败')
  }
}

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

// 提交表单
const submitForm = () => {
  formRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      await addVisit(form)
      ElMessage.success('新增就诊记录成功')
      router.push('/visits')
    } catch (error) {
      // 检查是否是201状态码（创建成功）
      if (error.response && error.response.status === 201) {
        ElMessage.success('新增就诊记录成功')
        router.push('/visits')
        return
      }
      
      console.error('新增就诊记录失败:', error)
      ElMessage.error('新增就诊记录失败')
    } finally {
      loading.value = false
    }
  })
}

// 重置表单
const resetForm = () => {
  formRef.value.resetFields()
  form.VisitDate = new Date().toISOString().split('T')[0] // 重置日期为今天
}

// 页面加载时获取数据
onMounted(() => {
  fetchPatientList()
  fetchDoctorList()
})
</script>

<style scoped>
.visit-form {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 