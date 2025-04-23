<template>
  <div class="admission-add">
    <div class="page-header">
      <h2>办理入院</h2>
    </div>
    
    <el-card class="form-card">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="admission-form"
      >
        <el-form-item label="就诊记录" prop="VisitID">
          <el-select
            v-model="form.VisitID"
            placeholder="请选择就诊记录"
            style="width: 100%"
            filterable
            @change="handleVisitChange"
          >
            <el-option
              v-for="visit in visitList"
              :key="visit.VisitID"
              :label="`${getPatientName(visit.PatientID)} - ${visit.Diagnosis} - ${visit.VisitDate}`"
              :value="visit.VisitID"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="病房" prop="WardID">
          <el-select
            v-model="form.WardID"
            placeholder="请选择病房"
            style="width: 100%"
            @change="handleWardChange"
          >
            <el-option
              v-for="ward in wardList"
              :key="ward.WardID"
              :label="ward.WardName"
              :value="ward.WardID"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="床位号" prop="BedNo">
          <el-select
            v-model="form.BedNo"
            placeholder="请选择床位号"
            style="width: 100%"
            :disabled="!form.WardID"
          >
            <el-option
              v-for="bed in availableBeds"
              :key="bed"
              :label="bed"
              :value="bed"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="入院日期" prop="AdmissionDate">
          <el-date-picker
            v-model="form.AdmissionDate"
            type="date"
            placeholder="请选择入院日期"
            style="width: 100%"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item label="入院原因" prop="AdmissionReason">
          <el-input
            v-model="form.AdmissionReason"
            type="textarea"
            :rows="3"
            placeholder="请输入入院原因"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { addAdmission } from '@/api/admission'
import { getWardList } from '@/api/ward'
import { getVisitList } from '@/api/visit'
import { getPatientList } from '@/api/patient'

const router = useRouter()
const formRef = ref(null)
const visitList = ref([])
const wardList = ref([])
const availableBeds = ref([])
const patientList = ref([])

// 表单数据
const form = reactive({
  WardID: '',
  VisitID: '',
  BedNo: '',
  AdmissionDate: '',
  DischargeDate: null,
  AdmissionReason: ''
})

// 表单验证规则
const rules = {
  WardID: [
    { required: true, message: '请选择病房', trigger: 'change' }
  ],
  VisitID: [
    { required: true, message: '请选择就诊记录', trigger: 'change' }
  ],
  BedNo: [
    { required: true, message: '请选择床位号', trigger: 'change' }
  ],
  AdmissionDate: [
    { required: true, message: '请选择入院日期', trigger: 'change' }
  ],
  AdmissionReason: [
    { required: true, message: '请输入入院原因', trigger: 'blur' }
  ]
}

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

// 根据患者ID获取患者名称
const getPatientName = (patientId) => {
  const patient = patientList.value.find(item => item.PatientID === patientId)
  return patient ? patient.Name : '未知患者'
}

// 获取就诊记录列表
const fetchVisitList = async () => {
  try {
    const res = await getVisitList()
    visitList.value = res.data.list || res.data
  } catch (error) {
    console.error('获取就诊记录失败:', error)
    ElMessage.error('获取就诊记录失败')
  }
}

// 获取病房列表
const fetchWardList = async () => {
  try {
    const res = await getWardList()
    wardList.value = res.data.list || res.data
  } catch (error) {
    console.error('获取病房列表失败:', error)
    ElMessage.error('获取病房列表失败')
  }
}

// 处理就诊记录选择变化
const handleVisitChange = (visitId) => {
  const visit = visitList.value.find(item => item.VisitID === visitId)
  if (visit) {
    // 可以在这里设置一些默认值，比如入院原因
    form.AdmissionReason = visit.Diagnosis || ''
  }
}

// 处理病房选择变化
const handleWardChange = (wardId) => {
  form.BedNo = ''
  if (wardId) {
    const ward = wardList.value.find(item => item.WardID === wardId)
    if (ward) {
      // 这里假设每个病房有10个床位，实际应该从后端获取
      availableBeds.value = Array.from({ length: 10 }, (_, i) => `${i + 1}`)
    }
  } else {
    availableBeds.value = []
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 准备提交的数据
        const submitData = {
          WardID: form.WardID,
          VisitID: form.VisitID,
          BedNo: form.BedNo,
          AdmissionDate: form.AdmissionDate,
          DischargeDate: null,
          AdmissionReason: form.AdmissionReason
        }
        
        const response = await addAdmission(submitData)
        if (response && response.AdmissionID) {
          ElMessage.success('入院办理成功')
          router.push('/admissions')
        } else {
          throw new Error('办理入院失败：响应数据格式不正确')
        }
      } catch (error) {
        console.error('办理入院失败:', error)
        ElMessage.error(error.message || '办理入院失败')
      }
    }
  })
}

// 组件挂载时获取数据
onMounted(() => {
  fetchPatientList()
  fetchVisitList()
  fetchWardList()
})
</script>

<style scoped>
.admission-add {
  width: 100%;
}

.page-header {
  margin-bottom: 20px;
}

.form-card {
  max-width: 800px;
  margin: 0 auto;
}

.admission-form {
  max-width: 600px;
  margin: 0 auto;
}
</style> 