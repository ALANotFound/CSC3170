<template>
  <div class="doctor-form">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑医师' : '新增医师' }}</h2>
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
              <el-input v-model="form.Name" placeholder="请输入医师姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="科室" prop="DeptName">
              <el-select 
                v-model="form.DeptName" 
                placeholder="请选择科室" 
                style="width: 200px"
                filterable
              >
                <el-option 
                  v-for="dept in departmentList" 
                  :key="dept.DeptID" 
                  :label="dept.DeptName" 
                  :value="dept.DeptName" 
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="职称" prop="Title">
              <el-input v-model="form.Title" placeholder="请输入职称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="Phone">
              <el-input v-model="form.Phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>
        
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
import { getDoctorDetail, addDoctor, updateDoctor } from '@/api/doctor'
import { getDepartmentList } from '@/api/department'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const departmentList = ref([])

// 是否为编辑模式
const isEdit = computed(() => {
  return route.params.id !== undefined
})

// 表单数据
const form = reactive({
  Name: '',
  DeptName: '',
  Title: '',
  Phone: ''
})

// 表单验证规则
const rules = reactive({
  Name: [
    { required: true, message: '请输入医师姓名', trigger: 'blur' },
    { max: 50, message: '姓名长度不能超过50个字符', trigger: 'blur' }
  ],
  DeptName: [{ required: true, message: '请选择科室', trigger: 'change' }],
  Phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
})

// 获取科室列表
const fetchDepartmentList = async () => {
  try {
    const res = await getDepartmentList()
    departmentList.value = res.data.list || res.data || []
  } catch (error) {
    console.error('获取科室列表失败:', error)
    ElMessage.error('获取科室列表失败')
    departmentList.value = []
  }
}

// 如果是编辑模式，获取医师详情
const fetchDoctorDetail = async () => {
  if (!isEdit.value) return
  
  loading.value = true
  try {
    const res = await getDoctorDetail(route.params.id)
    // 映射API返回的数据到表单字段
    const doctorData = res.data
    Object.assign(form, doctorData)
  } catch (error) {
    console.error('获取医师详情失败:', error)
    ElMessage.error('获取医师详情失败')
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
      // 准备提交的数据
      const submitData = {
        Name: form.Name,
        DeptName: form.DeptName,
        Title: form.Title,
        Phone: form.Phone
      }
      
      if (isEdit.value) {
        await updateDoctor(route.params.id, submitData)
        ElMessage.success('更新成功')
      } else {
        try {
          const response = await addDoctor(submitData)
          // 如果返回状态码是201，表示创建成功
          ElMessage.success('添加成功')
        } catch (error) {
          // 检查是否是201状态码（创建成功）
          if (error.response && error.response.status === 201) {
            ElMessage.success('添加成功')
            router.push('/doctors')
            return
          }
          // 其他错误正常抛出
          throw error
        }
      }
      router.push('/doctors')
    } catch (error) {
      console.error('保存医师信息失败:', error)
      ElMessage.error('保存医师信息失败')
    } finally {
      loading.value = false
    }
  })
}

// 重置表单
const resetForm = () => {
  if (isEdit.value) {
    fetchDoctorDetail()
  } else {
    formRef.value.resetFields()
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchDepartmentList()
  fetchDoctorDetail()
})
</script>

<style scoped>
.doctor-form {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 