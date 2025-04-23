<template>
  <div class="department-form">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑科室' : '新增科室' }}</h2>
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
            <el-form-item label="科室名称" prop="DeptName">
              <el-input v-model="form.DeptName" placeholder="请输入科室名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="位置" prop="Location">
              <el-input v-model="form.Location" placeholder="请输入科室位置" />
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
import { getDepartmentDetail, addDepartment, updateDepartment } from '@/api/department'

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
  DeptName: '',
  Location: ''
})

// 表单验证规则
const rules = reactive({
  DeptName: [{ required: true, message: '请输入科室名称', trigger: 'blur' }],
  Location: [{ required: true, message: '请输入科室位置', trigger: 'blur' }]
})

// 如果是编辑模式，获取科室详情
const fetchDepartmentDetail = async () => {
  if (!isEdit.value) return
  
  loading.value = true
  try {
    const res = await getDepartmentDetail(route.params.id)
    Object.assign(form, res.data)
  } catch (error) {
    console.error('获取科室详情失败:', error)
    ElMessage.error('获取科室详情失败')
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
      const submitData = {
        DeptName: form.DeptName,
        Location: form.Location
      }
      
      if (isEdit.value) {
        await updateDepartment(route.params.id, submitData)
        ElMessage.success('更新成功')
      } else {
        try {
          const response = await addDepartment(submitData)
          ElMessage.success('添加成功')
        } catch (error) {
          // 检查是否是201状态码（创建成功）
          if (error.response && error.response.status === 201) {
            ElMessage.success('添加成功')
            router.push('/departments')
            return
          }
          // 其他错误正常抛出
          throw error
        }
      }
      router.push('/departments')
    } catch (error) {
      console.error('保存科室信息失败:', error)
      ElMessage.error('保存科室信息失败')
    } finally {
      loading.value = false
    }
  })
}

// 重置表单
const resetForm = () => {
  if (isEdit.value) {
    fetchDepartmentDetail()
  } else {
    formRef.value.resetFields()
  }
}

// 页面加载时获取科室详情（如果是编辑模式）
onMounted(() => {
  fetchDepartmentDetail()
})
</script>

<style scoped>
.department-form {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 