<template>
  <div class="ward-form">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑病房' : '新增病房' }}</h2>
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
            <el-form-item label="病房名称" prop="WardName">
              <el-input v-model="form.WardName" placeholder="请输入病房名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属科室" prop="DeptID">
              <el-select 
                v-model="form.DeptID" 
                placeholder="请选择科室" 
                style="width: 200px"
                filterable
              >
                <el-option 
                  v-for="dept in departmentList" 
                  :key="dept.DeptID" 
                  :label="dept.DeptName" 
                  :value="dept.DeptID"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="床位数" prop="Capacity">
              <el-input-number 
                v-model="form.Capacity" 
                :min="1" 
                :max="100" 
                placeholder="请输入床位数"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="楼层" prop="Floor">
              <el-input-number 
                v-model="form.Floor" 
                :min="1" 
                :max="50" 
                placeholder="请输入楼层"
                style="width: 100%"
              />
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
import { getWardDetail, addWard, updateWard } from '@/api/ward'
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
  WardName: '',
  DeptID: null,
  Capacity: 1,
  Floor: 1
})

// 表单验证规则
const rules = reactive({
  WardName: [{ required: true, message: '请输入病房名称', trigger: 'blur' }],
  DeptID: [{ required: true, message: '请选择科室', trigger: 'change' }],
  Capacity: [{ required: true, message: '请输入床位数', trigger: 'blur' }],
  Floor: [{ required: true, message: '请输入楼层', trigger: 'blur' }]
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

// 如果是编辑模式，获取病房详情
const fetchWardDetail = async () => {
  if (!isEdit.value) return
  
  loading.value = true
  try {
    const res = await getWardDetail(route.params.id)
    // 映射API返回的数据到表单字段
    const wardData = res.data
    Object.assign(form, {
      WardName: wardData.WardName,
      DeptID: wardData.DeptID,
      Capacity: wardData.Capacity,
      Floor: wardData.Floor
    })
  } catch (error) {
    console.error('获取病房详情失败:', error)
    ElMessage.error('获取病房详情失败')
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
        WardName: form.WardName,
        DeptID: form.DeptID,
        Capacity: form.Capacity,
        Floor: form.Floor
      }
      
      if (isEdit.value) {
        await updateWard(route.params.id, submitData)
        ElMessage.success('更新成功')
      } else {
        try {
          const response = await addWard(submitData)
          // 如果返回状态码是201，表示创建成功
          ElMessage.success('添加成功')
        } catch (error) {
          // 检查是否是201状态码（创建成功）
          if (error.response && error.response.status === 201) {
            ElMessage.success('添加成功')
            router.push('/wards')
            return
          }
          // 其他错误正常抛出
          throw error
        }
      }
      router.push('/wards')
    } catch (error) {
      console.error('保存病房信息失败:', error)
      ElMessage.error('保存病房信息失败')
    } finally {
      loading.value = false
    }
  })
}

// 重置表单
const resetForm = () => {
  if (isEdit.value) {
    fetchWardDetail()
  } else {
    formRef.value.resetFields()
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchDepartmentList()
  fetchWardDetail()
})
</script>

<style scoped>
.ward-form {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 