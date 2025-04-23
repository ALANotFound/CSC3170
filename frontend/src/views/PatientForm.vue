<template>
  <div class="patient-form">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑患者' : '新增患者' }}</h2>
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
            <el-form-item label="姓名" prop="Name">
              <el-input v-model="form.Name" placeholder="请输入患者姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="Gender">
              <el-radio-group v-model="form.Gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="出生日期" prop="BirthDate">
              <el-date-picker
                v-model="form.BirthDate"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="身份证号" prop="IdentityNo">
              <el-input v-model="form.IdentityNo" placeholder="请输入身份证号" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号码" prop="Phone">
              <el-input v-model="form.Phone" placeholder="请输入手机号码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="紧急联系人" prop="emergencyContact">
              <el-input v-model="form.emergencyContact" placeholder="请输入紧急联系人" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系人电话" prop="emergencyPhone">
              <el-input v-model="form.emergencyPhone" placeholder="请输入联系人电话" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="血型" prop="bloodType">
              <el-select v-model="form.bloodType" placeholder="请选择血型" style="width: 100%">
                <el-option label="A型" value="A" />
                <el-option label="B型" value="B" />
                <el-option label="AB型" value="AB" />
                <el-option label="O型" value="O" />
                <el-option label="未知" value="Unknown" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="过敏史" prop="allergies">
          <el-input
            type="textarea"
            v-model="form.allergies"
            placeholder="请输入过敏史"
            :rows="2"
          />
        </el-form-item>
        
        <el-form-item label="家庭住址" prop="address">
          <el-input
            type="textarea"
            v-model="form.address"
            placeholder="请输入家庭住址"
            :rows="2"
          />
        </el-form-item>
        
        <el-form-item label="备注" prop="remarks">
          <el-input
            type="textarea"
            v-model="form.remarks"
            placeholder="请输入备注"
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getPatientDetail, addPatient, updatePatient } from '@/api/patient'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

// 是否为编辑模式
const isEdit = computed(() => {
  return route.params.id !== undefined
})

// 表单数据
const form = reactive({
  Name: '',
  Gender: '男',
  BirthDate: '',
  IdentityNo: '',
  Phone: '',
  emergencyContact: '',
  emergencyPhone: '',
  bloodType: '',
  allergies: '',
  address: '',
  remarks: ''
})

// 表单验证规则
const rules = reactive({
  Name: [{ required: true, message: '请输入患者姓名', trigger: 'blur' }],
  Gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  BirthDate: [{ required: true, message: '请选择出生日期', trigger: 'change' }],
  IdentityNo: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/, message: '请输入正确的身份证号', trigger: 'blur' }
  ],
  Phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
})

// 如果是编辑模式，获取患者详情
const fetchPatientDetail = async () => {
  if (!isEdit.value) return
  
  loading.value = true
  try {
    const res = await getPatientDetail(route.params.id)
    // 映射API返回的数据到表单字段
    const patientData = res.data
    form.Name = patientData.Name || patientData.name || ''
    form.Gender = patientData.Gender || (patientData.gender === 'M' ? '男' : '女') || '男'
    form.BirthDate = patientData.BirthDate || patientData.birthDate || ''
    form.IdentityNo = patientData.IdentityNo || patientData.idCard || ''
    form.Phone = patientData.Phone || patientData.phone || ''
    form.emergencyContact = patientData.emergencyContact || ''
    form.emergencyPhone = patientData.emergencyPhone || ''
    form.bloodType = patientData.bloodType || ''
    form.allergies = patientData.allergies || ''
    form.address = patientData.address || ''
    form.remarks = patientData.remarks || ''
  } catch (error) {
    console.error('获取患者详情失败:', error)
    ElMessage.error('获取患者详情失败')
  } finally {
    loading.value = false
  }
}

// 提交表单
const submitForm = () => {
  formRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      // 准备提交的数据，确保字段名称与API一致
      const submitData = {
        Name: form.Name,
        Gender: form.Gender,
        // 格式化日期为 YYYY-MM-DD
        BirthDate: form.BirthDate ? new Date(form.BirthDate).toISOString().split('T')[0] : '',
        IdentityNo: form.IdentityNo,
        Phone: form.Phone,
        emergencyContact: form.emergencyContact,
        emergencyPhone: form.emergencyPhone,
        bloodType: form.bloodType,
        allergies: form.allergies,
        address: form.address,
        remarks: form.remarks
      }
      
      if (isEdit.value) {
        await updatePatient(route.params.id, submitData)
        ElMessage.success('更新成功')
      } else {
        try {
          const response = await addPatient(submitData)
          // 如果返回状态码是201，表示创建成功
          ElMessage.success('添加成功')
        } catch (error) {
          // 检查是否是201状态码（创建成功）
          if (error.response && error.response.status === 201) {
            ElMessage.success('添加成功')
            router.push('/patients')
            return
          }
          // 其他错误正常抛出
          throw error
        }
      }
      router.push('/patients')
    } catch (error) {
      console.error('保存患者信息失败:', error)
      ElMessage.error('保存患者信息失败')
    } finally {
      loading.value = false
    }
  })
}

// 重置表单
const resetForm = () => {
  if (isEdit.value) {
    fetchPatientDetail()
  } else {
    formRef.value.resetFields()
  }
}

// 页面加载时获取患者详情（如果是编辑模式）
onMounted(() => {
  fetchPatientDetail()
})
</script>

<style scoped>
.patient-form {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 